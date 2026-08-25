from __future__ import annotations

import base64
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


APP_VERSION = "1.1.0-dev"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_CHAT_MODEL = "qwen2.5:3b"
DEFAULT_VISION_MODEL = "qwen2.5vl:3b"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class ArlenDatabase:
    """Small, bounded local memory store. Every operation opens its own connection.

    This keeps Qt worker threads safe and avoids holding a SQLite lock while the UI is
    idle. No conversation content is uploaded by this class.
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=8)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=NORMAL")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL CHECK(role IN ('system','user','assistant')),
                    body TEXT NOT NULL,
                    state TEXT NOT NULL DEFAULT 'success',
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_messages_created
                    ON messages(created_at DESC);
                CREATE TABLE IF NOT EXISTS recent_files (
                    path TEXT PRIMARY KEY,
                    kind TEXT NOT NULL DEFAULT 'file',
                    opened_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS file_index (
                    path TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    extension TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    modified REAL NOT NULL,
                    category TEXT NOT NULL,
                    indexed_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_file_index_name ON file_index(name);
                CREATE INDEX IF NOT EXISTS idx_file_index_category ON file_index(category);
                """
            )

    def add_message(self, role: str, body: str, state: str = "success") -> int:
        role = role if role in {"system", "user", "assistant"} else "assistant"
        cleaned = str(body).strip()
        if not cleaned:
            return 0
        with self.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO messages(role, body, state, created_at) VALUES(?,?,?,?)",
                (role, cleaned, state, utc_now()),
            )
            # Bound database growth on low-memory PCs while preserving useful history.
            connection.execute(
                "DELETE FROM messages WHERE id NOT IN "
                "(SELECT id FROM messages ORDER BY id DESC LIMIT 400)"
            )
            return int(cursor.lastrowid)

    def messages(self, limit: int = 40) -> list[dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 200))
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT id, role, body, state, created_at FROM messages "
                "ORDER BY id DESC LIMIT ?",
                (safe_limit,),
            ).fetchall()
        return [dict(row) for row in reversed(rows)]

    def ollama_context(self, limit: int = 16) -> list[dict[str, str]]:
        return [
            {"role": row["role"], "content": row["body"]}
            for row in self.messages(limit)
            if row["role"] in {"user", "assistant"}
        ]

    def clear_messages(self) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM messages")

    def remember_file(self, path: Path, kind: str = "file") -> None:
        resolved = str(Path(path).resolve())
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO recent_files(path, kind, opened_at) VALUES(?,?,?) "
                "ON CONFLICT(path) DO UPDATE SET kind=excluded.kind, opened_at=excluded.opened_at",
                (resolved, kind, utc_now()),
            )
            connection.execute(
                "DELETE FROM recent_files WHERE path NOT IN "
                "(SELECT path FROM recent_files ORDER BY opened_at DESC LIMIT 30)"
            )

    def recent_files(self, limit: int = 12) -> list[dict[str, str]]:
        safe_limit = max(1, min(int(limit), 30))
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT path, kind, opened_at FROM recent_files "
                "ORDER BY opened_at DESC LIMIT ?",
                (safe_limit,),
            ).fetchall()
        return [dict(row) for row in rows if Path(row["path"]).exists()]

    def replace_file_index(self, rows: list[tuple[str, str, str, int, float, str]]) -> None:
        stamp = utc_now()
        with self.connect() as connection:
            connection.execute("DELETE FROM file_index")
            connection.executemany(
                "INSERT INTO file_index(path,name,extension,size,modified,category,indexed_at) "
                "VALUES(?,?,?,?,?,?,?)",
                [(*row, stamp) for row in rows],
            )

    def file_index_summary(self) -> dict[str, Any]:
        with self.connect() as connection:
            total = connection.execute("SELECT COUNT(*) FROM file_index").fetchone()[0]
            size = connection.execute("SELECT COALESCE(SUM(size),0) FROM file_index").fetchone()[0]
            groups = connection.execute(
                "SELECT category, COUNT(*) AS count FROM file_index GROUP BY category ORDER BY count DESC"
            ).fetchall()
        return {"files": int(total), "bytes": int(size), "categories": [dict(row) for row in groups]}

    def organization_candidates(self, downloads: Path, limit: int = 100) -> list[dict[str, str]]:
        root_prefix = str(downloads.resolve()) + os.sep
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT path,name,category FROM file_index WHERE path LIKE ? "
                "AND category != 'Other' ORDER BY modified DESC LIMIT ?",
                (root_prefix + "%", max(1, min(int(limit), 200))),
            ).fetchall()
        plan = []
        for row in rows:
            source = Path(row["path"])
            # Only files directly inside Downloads are suggested; existing folders stay untouched.
            if source.parent.resolve() != downloads.resolve() or not source.is_file() or source.is_symlink():
                continue
            destination = downloads / "ARLEN Organized" / row["category"] / source.name
            plan.append({"source": str(source), "destination": str(destination), "category": row["category"]})
        return plan


class OllamaClient:
    """Minimal dependency-free client for the local Ollama HTTP API."""

    def __init__(self, base_url: str = DEFAULT_OLLAMA_URL, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _json_request(self, method: str, endpoint: str, payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + endpoint,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise RuntimeError(f"Ollama HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(
                "Ollama is not running. Open Ollama once, then press Refresh Diagnostics."
            ) from exc

    def tags(self) -> list[str]:
        payload = self._json_request("GET", "/api/tags")
        return [str(item.get("name", "")) for item in payload.get("models", []) if item.get("name")]

    @staticmethod
    def has_model(installed: list[str], requested: str) -> bool:
        wanted = requested.casefold()
        wanted_base = wanted.split(":", 1)[0]
        for value in installed:
            candidate = value.casefold()
            if candidate == wanted or candidate.split(":", 1)[0] == wanted_base:
                return True
        return False

    def chat(
        self,
        model: str,
        messages: list[dict[str, str]],
        low_resource: bool = True,
    ) -> str:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "keep_alive": "3m" if low_resource else "10m",
            "options": {
                "num_ctx": 1536 if low_resource else 3072,
                "num_predict": 256 if low_resource else 480,
                "temperature": 0.6,
                "num_thread": max(2, (os.cpu_count() or 4) - 1),
            },
        }
        response = self._json_request("POST", "/api/chat", payload)
        text = str(response.get("message", {}).get("content", "")).strip()
        if not text:
            raise RuntimeError("Ollama returned an empty response.")
        return text

    def analyze_image(
        self,
        model: str,
        image_path: Path,
        prompt: str,
        low_resource: bool = True,
    ) -> str:
        encoded = base64.b64encode(Path(image_path).read_bytes()).decode("ascii")
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": prompt.strip() or "Describe this image and extract any readable text.",
                "images": [encoded],
            }],
            "stream": False,
            "keep_alive": "2m" if low_resource else "8m",
            "options": {
                "num_ctx": 1536 if low_resource else 3072,
                "num_predict": 320 if low_resource else 600,
                "temperature": 0.2,
            },
        }
        response = self._json_request("POST", "/api/chat", payload)
        text = str(response.get("message", {}).get("content", "")).strip()
        if not text:
            raise RuntimeError("The vision model returned an empty response.")
        return text

    def unload(self, model: str) -> None:
        self._json_request("POST", "/api/generate", {
            "model": model, "prompt": "", "stream": False, "keep_alive": 0,
        })


class EnvironmentScanner:
    """Truthful, read-only capability scan used by Settings and diagnostics."""

    def __init__(self, ollama: OllamaClient, chat_model: str, vision_model: str):
        self.ollama = ollama
        self.chat_model = chat_model
        self.vision_model = vision_model

    @staticmethod
    def _windows_app(candidates: list[Path], command: str) -> dict[str, Any]:
        path = shutil.which(command)
        if not path:
            path = next((str(item) for item in candidates if item.is_file()), "")
        return {"installed": bool(path), "path": path}

    def scan(self) -> dict[str, Any]:
        ram_gb = round(_total_ram_bytes() / 1024**3, 1)
        ffmpeg = shutil.which("ffmpeg") or ""
        ollama_exe = shutil.which("ollama") or ""
        tags: list[str] = []
        ollama_running = False
        ollama_error = ""
        try:
            tags = self.ollama.tags()
            ollama_running = True
        except Exception as exc:
            ollama_error = str(exc)

        local = Path(os.environ.get("LOCALAPPDATA", ""))
        programs = Path(os.environ.get("PROGRAMFILES", ""))
        programs_x86 = Path(os.environ.get("PROGRAMFILES(X86)", ""))
        browsers = {
            "brave": self._windows_app([
                local / "BraveSoftware/Brave-Browser/Application/brave.exe",
                programs / "BraveSoftware/Brave-Browser/Application/brave.exe",
            ], "brave"),
            "chrome": self._windows_app([
                local / "Google/Chrome/Application/chrome.exe",
                programs / "Google/Chrome/Application/chrome.exe",
            ], "chrome"),
            "edge": self._windows_app([
                programs_x86 / "Microsoft/Edge/Application/msedge.exe",
                programs / "Microsoft/Edge/Application/msedge.exe",
            ], "msedge"),
        }
        return {
            "app_version": APP_VERSION,
            "platform": platform.platform(),
            "python": platform.python_version(),
            "ram_gb": ram_gb,
            "resource_profile": "4 GB / Lite" if ram_gb < 7.0 else "8 GB+ / Smooth",
            "ffmpeg": {"installed": bool(ffmpeg), "path": ffmpeg},
            "ollama": {
                "installed": bool(ollama_exe) or ollama_running,
                "running": ollama_running,
                "path": ollama_exe,
                "error": ollama_error,
                "models": tags,
            },
            "chat": {
                "model": self.chat_model,
                "ready": ollama_running and self.ollama.has_model(tags, self.chat_model),
            },
            "vision": {
                "model": self.vision_model,
                "ready": ollama_running and self.ollama.has_model(tags, self.vision_model),
            },
            "browsers": browsers,
        }


def _total_ram_bytes() -> int:
    try:
        import psutil
        return int(psutil.virtual_memory().total)
    except Exception:
        return 0


def launch_local_file(path: Path) -> None:
    resolved = str(Path(path).resolve())
    if os.name == "nt":
        os.startfile(resolved)  # type: ignore[attr-defined]
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", resolved])
    else:
        subprocess.Popen(["xdg-open", resolved])
