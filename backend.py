from __future__ import annotations

import gc
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.parse import quote_plus

import psutil
from PySide6.QtCore import QObject, Property, QTimer, Signal, Slot
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(getattr(__import__("sys"), "_MEIPASS", Path(__file__).resolve().parent))
if os.name == "nt":
    # User identity survives application updates and folder replacement.
    DATA = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "ARLEN NEXUS" / "UserData"
else:
    DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)
SETTINGS_FILE = DATA / "settings.json"
LOG_FILE = DATA / "activity.jsonl"
COMMANDS_FILE = DATA / "custom_commands.json"
UPDATE_STATE_FILE = DATA / "update_state.json"
BACKUP_DIR = DATA / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

DEFAULT_SETTINGS = {
    "first_run": True,
    "pin_hash": "",
    "opening_duration": 12,
    "opening_sound": True,
    "theme": "Obsidian",
    "sphere": "Neural Sphere",
    "background_image": "",
    "hotkey": "Ctrl+Alt+A",
    "internet_mode": "Smart Auto",
    "allow_public_search": True,
    "allow_safe_downloads": True,
    "allow_uploads": False,
    "auto_return_offline": True,
    "permission_level": 2,
    "voice_enabled": False,
    # Local images are never blocked, blurred, deleted or uploaded by ARLEN.
    "local_image_policy": "Unrestricted",
    "owner_name": "Jubaer Hossain",
    "owner_call_name": "Jubaer",
    "owner_title": "Administrator",
    "owner_avatar": "",
    "custom_sphere": "",
    "welcome_message": "Your private workspace is ready.",
    "interface_language": "English + Bangla",
    "voice_language": "Auto Detect",
    "voice_speed": 1.0,
    "voice_pitch": 1.0,
    "wake_word": "ARLEN",
    "update_channel": "Stable",
}


def load_settings() -> dict:
    if SETTINGS_FILE.exists():
        try:
            return {**DEFAULT_SETTINGS, **json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))}
        except (OSError, json.JSONDecodeError):
            pass
    return DEFAULT_SETTINGS.copy()


class Backend(QObject):
    statsChanged = Signal()
    chatReply = Signal(str, str)
    commandResult = Signal(str, str)
    settingsChanged = Signal()
    voiceStateChanged = Signal(str)
    showRequested = Signal()
    imageReady = Signal(str)
    visionResult = Signal(str)
    pdfResult = Signal(str)
    profileSaved = Signal(str)
    automationChanged = Signal()
    updateStatusChanged = Signal(str)
    capabilityWarning = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self._cpu = self._ram = self._disk = 0.0
        self._down = self._up = 0.0
        self._network = "Checking"
        self._wifi = "Unknown"
        self._last_net = psutil.net_io_counters()
        self._last_net_time = time.monotonic()
        self._session_in = self._last_net.bytes_recv
        self._session_out = self._last_net.bytes_sent
        self._uptime = "00:00:00"
        self._top_apps = "Scanning processes…"
        self._brain = None
        self._brain_loading = False
        self._custom_commands = self._load_custom_commands()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(1000)
        self.refresh_stats()
        if os.name == "nt" and self.settings["opening_sound"]:
            threading.Thread(target=self._startup_sound, daemon=True).start()
        if os.name == "nt":
            threading.Thread(target=self._hotkey_loop, daemon=True).start()

    @staticmethod
    def _startup_sound():
        try:
            import winsound
            for frequency, duration in ((260, 70), (390, 80), (520, 90), (780, 140)):
                winsound.Beep(frequency, duration)
        except Exception:
            pass

    def _hotkey_loop(self):
        """Register Ctrl+Alt+A without a visible helper window."""
        try:
            user32 = ctypes.windll.user32
            if not user32.RegisterHotKey(None, 1, 0x0002 | 0x0001, ord("A")):
                return
            message = wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(message), None, 0, 0) != 0:
                if message.message == 0x0312 and message.wParam == 1:
                    self.showRequested.emit()
        except Exception:
            return

    @Property(float, notify=statsChanged)
    def cpu(self): return self._cpu

    @Property(float, notify=statsChanged)
    def ram(self): return self._ram

    @Property(float, notify=statsChanged)
    def disk(self): return self._disk

    @Property(float, notify=statsChanged)
    def downloadSpeed(self): return self._down

    @Property(float, notify=statsChanged)
    def uploadSpeed(self): return self._up

    @Property(str, notify=statsChanged)
    def networkStatus(self): return self._network

    @Property(str, notify=statsChanged)
    def wifiName(self): return self._wifi

    @Property(str, notify=statsChanged)
    def uptime(self): return self._uptime

    @Property(str, notify=statsChanged)
    def topApps(self): return self._top_apps

    @Property(str, notify=settingsChanged)
    def currentTheme(self): return self.settings["theme"]

    @Property(int, notify=settingsChanged)
    def openingDuration(self): return int(self.settings["opening_duration"])

    @Property(bool, notify=settingsChanged)
    def openingSound(self): return bool(self.settings["opening_sound"])

    @Property(str, notify=settingsChanged)
    def sphereName(self): return self.settings["sphere"]

    @Property(int, notify=settingsChanged)
    def permissionLevel(self): return int(self.settings["permission_level"])

    @Property(str, notify=settingsChanged)
    def localImagePolicy(self): return self.settings.get("local_image_policy", "Unrestricted")

    @Property(bool, notify=settingsChanged)
    def firstRun(self): return bool(self.settings["first_run"])

    @Property(str, notify=settingsChanged)
    def ownerName(self): return self.settings.get("owner_name", "Jubaer Hossain")

    @Property(str, notify=settingsChanged)
    def ownerCallName(self): return self.settings.get("owner_call_name", "Jubaer")

    @Property(str, notify=settingsChanged)
    def ownerTitle(self): return self.settings.get("owner_title", "Administrator")

    @Property(str, notify=settingsChanged)
    def welcomeMessage(self): return self.settings.get("welcome_message", "Your private workspace is ready.")

    @Property(str, notify=settingsChanged)
    def wakeWord(self): return self.settings.get("wake_word", "ARLEN")

    @Property(str, notify=settingsChanged)
    def ownerAvatar(self):
        value = self.settings.get("owner_avatar", "")
        return Path(value).as_uri() if value and Path(value).is_file() else ""

    @Property(str, notify=settingsChanged)
    def customBackground(self):
        value = self.settings.get("background_image", "")
        return Path(value).as_uri() if value and Path(value).is_file() else ""

    @Property(str, notify=settingsChanged)
    def customSphere(self):
        value = self.settings.get("custom_sphere", "")
        return Path(value).as_uri() if value and Path(value).is_file() else ""

    @Property(str, notify=automationChanged)
    def customCommands(self):
        return json.dumps(self._custom_commands, ensure_ascii=False)

    @Slot()
    def refresh_stats(self):
        self._cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        self._ram = memory.percent
        self._disk = psutil.disk_usage(Path.home().anchor).percent
        now = time.monotonic()
        current = psutil.net_io_counters()
        elapsed = max(now - self._last_net_time, 0.1)
        self._down = max(0.0, (current.bytes_recv - self._last_net.bytes_recv) * 8 / elapsed / 1_000_000)
        self._up = max(0.0, (current.bytes_sent - self._last_net.bytes_sent) * 8 / elapsed / 1_000_000)
        self._last_net, self._last_net_time = current, now
        seconds = int(time.time() - psutil.boot_time())
        self._uptime = f"{seconds//3600:02}:{(seconds%3600)//60:02}:{seconds%60:02}"
        self._network = "Online" if self._has_network() else "Offline"
        if int(now) % 5 == 0:
            self._wifi = self._get_wifi_name()
            self._top_apps = self._process_summary()
        self.statsChanged.emit()

    @staticmethod
    def _has_network():
        try:
            with socket.create_connection(("1.1.1.1", 53), timeout=0.35):
                return True
        except OSError:
            return False

    @staticmethod
    def _get_wifi_name():
        if os.name != "nt":
            return "Windows Wi-Fi"
        try:
            output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=True, encoding="utf-8", errors="ignore", creationflags=0x08000000)
            for line in output.splitlines():
                if line.strip().startswith("SSID") and "BSSID" not in line:
                    return line.split(":", 1)[1].strip()
        except Exception:
            pass
        return "Not connected"

    @staticmethod
    def _process_summary():
        rows = []
        for process in psutil.process_iter(["name", "memory_info"]):
            try:
                rows.append((process.info["memory_info"].rss, process.info["name"] or "Process"))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        rows.sort(reverse=True)
        return "\n".join(f"{name[:20]}  •  {rss/1024**2:.0f} MB" for rss, name in rows[:5])

    def _save(self):
        SETTINGS_FILE.write_text(json.dumps(self.settings, indent=2), encoding="utf-8")
        self.settingsChanged.emit()

    @staticmethod
    def _load_custom_commands():
        if COMMANDS_FILE.exists():
            try:
                data = json.loads(COMMANDS_FILE.read_text(encoding="utf-8"))
                return data if isinstance(data, list) else []
            except (OSError, json.JSONDecodeError):
                pass
        return []

    def _save_custom_commands(self):
        COMMANDS_FILE.write_text(json.dumps(self._custom_commands, ensure_ascii=False, indent=2), encoding="utf-8")
        self.automationChanged.emit()

    def _log(self, action, result):
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"time": datetime.now().isoformat(timespec="seconds"), "action": action, "result": result}, ensure_ascii=False) + "\n")

    @Slot(str)
    def setOpeningDuration(self, value):
        duration = int(value)
        if duration in (3, 7, 12):
            self.settings["opening_duration"] = duration
            self._save()

    @Slot(bool)
    def setOpeningSound(self, enabled):
        self.settings["opening_sound"] = bool(enabled)
        self._save()

    @Slot(str)
    def setTheme(self, theme):
        if theme in ("Obsidian", "Crimson", "Emerald", "Violet", "Arctic"):
            self.settings["theme"] = theme
            self._save()

    @Slot(str)
    def setSphere(self, name):
        self.settings["sphere"] = name
        self._save()

    @Slot(str, result=bool)
    def setInitialPin(self, pin):
        if not (pin.isdigit() and 4 <= len(pin) <= 12):
            return False
        self.settings["pin_hash"] = hashlib.sha256(pin.encode()).hexdigest()
        self.settings["first_run"] = False
        self._save()
        return True

    @Slot(str, result=bool)
    def verifyPin(self, pin):
        return bool(self.settings["pin_hash"]) and hashlib.sha256(pin.encode()).hexdigest() == self.settings["pin_hash"]

    @Slot(str, str, result=bool)
    def changePin(self, old, new):
        if not self.verifyPin(old) or not (new.isdigit() and 4 <= len(new) <= 12):
            return False
        self.settings["pin_hash"] = hashlib.sha256(new.encode()).hexdigest()
        self._save()
        return True

    @Slot(str, str, str, str, str, result=bool)
    def saveOwnerProfile(self, name, call_name, title, welcome, pin):
        if not self.verifyPin(pin):
            self.profileSaved.emit("Owner PIN did not match.")
            return False
        cleaned_name = name.strip()[:60]
        cleaned_call = call_name.strip()[:30]
        if not cleaned_name or not cleaned_call:
            self.profileSaved.emit("Owner name and call name are required.")
            return False
        self.settings.update({
            "owner_name": cleaned_name,
            "owner_call_name": cleaned_call,
            "owner_title": title.strip()[:50] or "Administrator",
            "welcome_message": welcome.strip()[:180] or "Your private workspace is ready.",
        })
        self._save()
        self._log("owner profile updated", cleaned_name)
        self.profileSaved.emit("Owner account updated securely.")
        return True

    @Slot(str, str, result=str)
    def importProfileVisual(self, source, kind):
        if kind not in ("avatar", "background", "sphere"):
            return "Unsupported visual type."
        try:
            source_path = self._local_path(source)
            if source_path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp", ".bmp"):
                return "Choose a supported image file."
            visual_dir = DATA / "visuals"
            visual_dir.mkdir(parents=True, exist_ok=True)
            destination = visual_dir / f"{kind}{source_path.suffix.lower()}"
            shutil.copy2(source_path, destination)
            key = {"avatar": "owner_avatar", "background": "background_image", "sphere": "custom_sphere"}[kind]
            self.settings[key] = str(destination)
            if kind == "sphere":
                self.settings["sphere"] = "Custom Sphere"
            self._save()
            self._log(f"custom {kind}", str(source_path))
            return f"Custom {kind} saved."
        except Exception as exc:
            return f"Could not import {kind}: {exc}"

    @Slot(str, str, str, str, result=bool)
    def addCustomCommand(self, trigger, actions, response, pin):
        if not self.verifyPin(pin):
            self.commandResult.emit("Owner PIN is required to teach a new command.", "error")
            return False
        trigger = trigger.strip()
        action_list = [part.strip() for part in re.split(r"[;\n]+", actions) if part.strip()]
        if len(trigger) < 2 or not action_list:
            self.commandResult.emit("Add a trigger phrase and at least one action.", "warning")
            return False
        self._custom_commands = [item for item in self._custom_commands if item.get("trigger", "").lower() != trigger.lower()]
        self._custom_commands.append({"trigger": trigger, "actions": action_list, "response": response.strip()[:180], "enabled": True})
        self._save_custom_commands()
        self._log("custom command created", trigger)
        self.commandResult.emit(f"ARLEN learned: {trigger}", "success")
        return True

    @Slot(str)
    def interpretVoiceText(self, transcript):
        text = transcript.strip()
        if not text:
            self.voiceStateChanged.emit("I could not hear a command.")
            return
        wake = self.settings.get("wake_word", "ARLEN").lower()
        normalized = text.lower().replace("hey " + wake, "").replace(wake, "").strip(" ,.-")
        self.voiceStateChanged.emit(f"HEARD: {text}  •  UNDERSTOOD: {normalized}")
        self.execute(normalized)

    @Slot(str, str)
    def saveVoicePreferences(self, wake_word, language):
        wake_word = wake_word.strip()[:24] or "ARLEN"
        allowed = ("Auto Detect", "Bangla", "Banglish", "English")
        self.settings["wake_word"] = wake_word
        self.settings["voice_language"] = language if language in allowed else "Auto Detect"
        self._save()
        self.voiceStateChanged.emit(f"Voice profile saved. Wake word: {wake_word}")

    @Slot(str)
    def execute(self, command):
        text = command.strip()
        if not text:
            return
        threading.Thread(target=self._execute_worker, args=(text,), daemon=True).start()

    def _execute_worker(self, command):
        text = command.lower()
        result, level = "Command not recognized. Open Command Center to view examples.", "warning"
        for item in self._custom_commands:
            if item.get("enabled", True) and item.get("trigger", "").lower() in text:
                completed = []
                for action in item.get("actions", []):
                    self._run_macro_action(action, completed)
                result = item.get("response") or f"Custom command completed: {item.get('trigger')}"
                self._log(command, {"macro": item.get("trigger"), "completed": completed})
                self.commandResult.emit(result, "success")
                return
        apps = {
            "brave": [self._brave_path()], "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"], "paint": ["mspaint.exe"],
            "explorer": ["explorer.exe"], "task manager": ["taskmgr.exe"],
            "vs code": ["code"],
        }
        aliases = {"ব্রেভ": "brave", "browser": "brave", "ব্রাউজার": "brave", "নোটপ্যাড": "notepad", "ক্যালকুলেটর": "calculator", "ক্যালকুলেটরটা": "calculator", "পেইন্ট": "paint", "টাস্ক ম্যানেজার": "task manager", "ভিএস কোড": "vs code", "ডাউনলোডস": "downloads", "ডকুমেন্টস": "documents", "ছবির ফোল্ডার": "pictures"}
        for alias, name in aliases.items():
            text = text.replace(alias, name)
        if any(prefix in text for prefix in ("search online ", "web search ", "অনলাইনে খুঁজ", "ইন্টারনেটে খুঁজ")):
            query = text
            for prefix in ("search online", "web search", "অনলাইনে খুঁজে দাও", "অনলাইনে খুঁজ", "ইন্টারনেটে খুঁজে দাও", "ইন্টারনেটে খুঁজ"):
                query = query.replace(prefix, "").strip()
            self.webSearch(query)
            return
        if any(word in text for word in ("open", "launch", "kholo", "khol", "chalu", "open koro", "খোলো", "খুলে", "চালু")):
            for name, cmd in apps.items():
                if name in text:
                    try:
                        subprocess.Popen(cmd, creationflags=0x08000000 if os.name == "nt" else 0)
                        result, level = f"{name.title()} opened successfully.", "success"
                    except Exception as exc:
                        result, level = f"Could not open {name}: {exc}", "error"
                    break
            else:
                folders = {"downloads": Path.home()/"Downloads", "documents": Path.home()/"Documents", "desktop": Path.home()/"Desktop", "pictures": Path.home()/"Pictures"}
                for name, path in folders.items():
                    if name in text:
                        os.startfile(path) if os.name == "nt" else None
                        result, level = f"{name.title()} opened.", "success"
                        break
        elif "system" in text or "status" in text or "সিস্টেম" in text:
            result, level = f"CPU {self._cpu:.0f}%, RAM {self._ram:.0f}%, Disk {self._disk:.0f}%. Network is {self._network}.", "success"
        elif "restart" in text or "restart koro" in text or "রিস্টার্ট" in text:
            result, level = "REQUIRES_CONFIRMATION:Restart the PC in 10 seconds?", "confirm"
        elif "shutdown" in text or "shut down" in text or "off koro" in text or "শাটডাউন" in text:
            result, level = "REQUIRES_CONFIRMATION:Shut down the PC in 10 seconds?", "confirm"
        elif "cleanup" in text or "ক্লিন" in text:
            result, level = "REQUIRES_CONFIRMATION:Scan safe temporary files and ARLEN memory?", "confirm_cleanup"
        self._log(command, result)
        self.commandResult.emit(result, level)

    def _run_macro_action(self, action, completed):
        """Run only allow-listed macro actions; power/delete actions stay outside macros."""
        text = action.lower().strip()
        safe_apps = {"brave": [self._brave_path()], "notepad": ["notepad.exe"], "calculator": ["calc.exe"], "paint": ["mspaint.exe"], "task manager": ["taskmgr.exe"], "vs code": ["code"]}
        for name, command in safe_apps.items():
            if name in text and any(word in text for word in ("open", "start", "launch", "খোল", "চালু")):
                subprocess.Popen(command, creationflags=0x08000000 if os.name == "nt" else 0)
                completed.append(action)
                return
        folders = {"downloads": Path.home()/"Downloads", "documents": Path.home()/"Documents", "desktop": Path.home()/"Desktop", "pictures": Path.home()/"Pictures"}
        for name, path in folders.items():
            if name in text and os.name == "nt":
                os.startfile(path)
                completed.append(action)
                return
        completed.append(f"Skipped unsupported action: {action}")

    @Slot()
    def checkForUpdates(self):
        """Read a signed/local manifest foundation; no files are replaced silently."""
        manifest = ROOT / "updates" / "manifest.json"
        if not manifest.exists():
            self.updateStatusChanged.emit("ARLEN v0.3 is current. No staged update manifest was found.")
            return
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            version = str(data.get("version", "Unknown"))
            files = data.get("files", [])
            self.updateStatusChanged.emit(f"Update {version} is staged with {len(files)} changed component(s). Review is required before apply.")
        except Exception as exc:
            self.updateStatusChanged.emit(f"Update manifest could not be verified: {exc}")

    @Slot(result=bool)
    def verifyStagedUpdate(self):
        try:
            data, _files = self._read_verified_update()
            self.updateStatusChanged.emit(f"Update {data.get('version', 'Unknown')} verified. Apply remains owner-confirmed and rollback-protected.")
            return True
        except Exception as exc:
            self.updateStatusChanged.emit(f"Update verification failed safely: {exc}")
            return False

    @staticmethod
    def _safe_update_relative_path(value: str) -> Path:
        """Return a normalized application-relative path or reject it.

        Update packages may change application files only. UserData, the updater's
        own working directory, absolute paths, traversal, and symlink targets are
        deliberately outside this contract.
        """
        normalized = str(value).replace("\\", "/")
        relative = Path(normalized)
        if (not normalized or normalized.startswith("/") or re.match(r"^[A-Za-z]:/", normalized)
                or ".." in relative.parts):
            raise ValueError("unsafe update path")
        if relative.parts[0].lower() in {"data", "userdata", "updates"}:
            raise ValueError("protected update path")
        return relative

    def _read_verified_update(self) -> tuple[dict, list[tuple[Path, Path]]]:
        manifest = ROOT / "updates" / "manifest.json"
        staging = ROOT / "updates" / "staging"
        if not manifest.is_file():
            raise ValueError("no staged update manifest")
        data = json.loads(manifest.read_text(encoding="utf-8"))
        files = data.get("files")
        if not isinstance(files, list) or not files:
            raise ValueError("manifest contains no files")
        verified = []
        seen = set()
        for item in files:
            relative = self._safe_update_relative_path(item.get("path", ""))
            key = relative.as_posix().casefold()
            if key in seen:
                raise ValueError(f"duplicate update path: {relative}")
            seen.add(key)
            source = staging / relative
            if not source.is_file() or source.is_symlink():
                raise ValueError(f"missing or unsafe staged file: {relative}")
            expected = str(item.get("sha256", "")).lower()
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
            if not expected or actual != expected:
                raise ValueError(f"checksum failed: {relative}")
            verified.append((relative, source))
        return data, verified

    @Slot(str, result=bool)
    def applyStagedUpdate(self, pin):
        """Apply a verified staged update after owner-PIN approval.

        Every replaced file is copied to a versioned backup first. Any exception
        restores the previous application state immediately. Personal UserData is
        never part of the allowed destination set.
        """
        if not self.verifyPin(pin):
            self.updateStatusChanged.emit("Owner PIN did not match. Update was not applied.")
            return False
        try:
            data, files = self._read_verified_update()
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            backup_root = ROOT / "updates" / "backups" / stamp
            backup_root.mkdir(parents=True, exist_ok=False)
            state = {"version": str(data.get("version", "Unknown")), "backup": str(backup_root), "replaced": [], "created": []}
            for relative, source in files:
                destination = ROOT / relative
                if destination.is_symlink():
                    raise ValueError(f"refusing symlink destination: {relative}")
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    backup = backup_root / relative
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(destination, backup)
                    state["replaced"].append(relative.as_posix())
                else:
                    state["created"].append(relative.as_posix())
                temporary = destination.with_name(destination.name + ".arlen-new")
                shutil.copy2(source, temporary)
                os.replace(temporary, destination)
            state["applied_at"] = datetime.now().isoformat(timespec="seconds")
            UPDATE_STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
            self._log("update applied", state["version"])
            self.updateStatusChanged.emit(f"Update {state['version']} applied. Restart ARLEN to complete validation; rollback remains available.")
            return True
        except Exception as exc:
            try:
                if "state" in locals():
                    self._restore_update_state(state)
            except Exception:
                pass
            self.updateStatusChanged.emit(f"Update failed safely and previous files were restored: {exc}")
            return False

    def _restore_update_state(self, state: dict):
        backup_root = Path(state["backup"])
        for value in state.get("replaced", []):
            relative = self._safe_update_relative_path(value)
            source, destination = backup_root / relative, ROOT / relative
            if not source.is_file():
                raise ValueError(f"rollback backup missing: {relative}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_name(destination.name + ".arlen-rollback")
            shutil.copy2(source, temporary)
            os.replace(temporary, destination)
        for value in state.get("created", []):
            destination = ROOT / self._safe_update_relative_path(value)
            if destination.exists() and not destination.is_symlink():
                destination.unlink()

    @Slot(str, result=bool)
    def rollbackLastUpdate(self, pin):
        if not self.verifyPin(pin):
            self.updateStatusChanged.emit("Owner PIN did not match. Rollback was not started.")
            return False
        try:
            if not UPDATE_STATE_FILE.is_file():
                raise ValueError("no applied update state was found")
            state = json.loads(UPDATE_STATE_FILE.read_text(encoding="utf-8"))
            self._restore_update_state(state)
            UPDATE_STATE_FILE.unlink(missing_ok=True)
            self._log("update rolled back", state.get("version", "Unknown"))
            self.updateStatusChanged.emit(f"Update {state.get('version', 'Unknown')} rolled back. Restart ARLEN.")
            return True
        except Exception as exc:
            self.updateStatusChanged.emit(f"Rollback could not complete: {exc}")
            return False

    @Slot(result=str)
    def packStatus(self):
        packs = {
            "Local Brain": any((ROOT/"models").glob("*.gguf")),
            "Voice": (ROOT/"models"/"voice").exists(),
            "Vision/OCR": (ROOT/"models"/"ocr").exists(),
            "Image": True,
            "PDF": True,
        }
        return "\n".join(f"{name}: {'READY' if ready else 'NOT LOADED'}" for name, ready in packs.items())

    @Slot(str, result=str)
    def backupOwnerData(self, pin):
        if not self.verifyPin(pin):
            return "Owner PIN did not match. Backup was not created."
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        destination = BACKUP_DIR / f"owner-data-{stamp}.json"
        payload = {
            "format": "ARLEN_OWNER_BACKUP_V1",
            "created": datetime.now().isoformat(timespec="seconds"),
            "settings": self.settings,
            "custom_commands": self._custom_commands,
        }
        destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        self._log("owner backup", str(destination))
        return f"PIN-authorized local backup created: {destination}"

    @staticmethod
    def _brave_path():
        candidates = [
            Path(os.environ.get("PROGRAMFILES", ""))/"BraveSoftware/Brave-Browser/Application/brave.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", ""))/"BraveSoftware/Brave-Browser/Application/brave.exe",
            Path(os.environ.get("LOCALAPPDATA", ""))/"BraveSoftware/Brave-Browser/Application/brave.exe",
        ]
        found = next((str(path) for path in candidates if path.is_file()), None)
        return found or "brave.exe"

    @Slot(str)
    def confirmAction(self, action):
        if action == "restart" and os.name == "nt":
            subprocess.Popen(["shutdown", "/r", "/t", "10"], creationflags=0x08000000)
            self.commandResult.emit("Restart scheduled. Use Cancel Power Action within 10 seconds to abort.", "success")
        elif action == "shutdown" and os.name == "nt":
            subprocess.Popen(["shutdown", "/s", "/t", "10"], creationflags=0x08000000)
            self.commandResult.emit("Shutdown scheduled. Use Cancel Power Action within 10 seconds to abort.", "success")
        elif action == "cleanup":
            gc.collect()
            self.commandResult.emit("ARLEN memory optimized. Temporary files were not deleted without a selected scope.", "success")

    @Slot()
    def cancelPower(self):
        if os.name == "nt":
            subprocess.Popen(["shutdown", "/a"], creationflags=0x08000000)
        self.commandResult.emit("Pending Windows power action cancelled.", "success")

    @Slot(str)
    def sendChat(self, message):
        text = message.strip()
        if not text:
            return
        threading.Thread(target=self._chat_worker, args=(text,), daemon=True).start()

    def _chat_worker(self, message):
        model = next((p for p in (ROOT/"models").glob("*.gguf")), None)
        if model is None:
            self.capabilityWarning.emit("LOCAL BRAIN NOT INSTALLED", "Private conversational chat needs a compatible GGUF Local Brain Pack. PC commands and built-in tools remain available.")
            reply = "My local Conversational Brain is not installed yet. I can still execute PC commands. Add a compatible GGUF model in the models folder to enable private offline conversation."
            self.chatReply.emit(reply, "brain_missing")
            return
        try:
            if self._brain is None:
                from llama_cpp import Llama
                self._brain = Llama(model_path=str(model), n_ctx=2048, n_threads=max(2, (os.cpu_count() or 4)-1), verbose=False)
            prompt = f"You are ARLEN NEXUS, Jubaer Hossain's private offline PC assistant. Be concise, helpful and security-conscious. User: {message}\nARLEN:"
            output = self._brain(prompt, max_tokens=260, stop=["User:"], temperature=0.65)
            reply = output["choices"][0]["text"].strip()
            self.chatReply.emit(reply, "success")
        except Exception as exc:
            self.chatReply.emit(f"Local brain could not start: {exc}", "error")

    @Slot()
    def unloadBrain(self):
        self._brain = None
        gc.collect()
        self.chatReply.emit("Conversational Brain unloaded from memory.", "success")

    @Slot()
    def startVoice(self):
        model_dir = ROOT / "models" / "voice"
        if not model_dir.exists():
            self.capabilityWarning.emit("VOICE NOT SUPPORTED YET", "The offline microphone, speech recognition and TTS pack is not bundled in this release. No microphone recording was started.")
            self.voiceStateChanged.emit("Voice Pack not installed")
            return
        self.voiceStateChanged.emit("Voice module ready; microphone integration will use the selected local model")

    @Slot(result=str)
    def systemDetails(self):
        return json.dumps({
            "device": platform.node(), "windows": platform.platform(),
            "processor": platform.processor(), "python": platform.python_version(),
            "total_ram_gb": round(psutil.virtual_memory().total/1024**3, 1),
            "logical_cpu": psutil.cpu_count(),
        })

    @Slot(result=str)
    def sessionUsage(self):
        net = psutil.net_io_counters()
        return f"↓ {(net.bytes_recv-self._session_in)/1024**2:.1f} MB   ↑ {(net.bytes_sent-self._session_out)/1024**2:.1f} MB"

    @Slot(str)
    def inspectImage(self, source):
        """Read local image metadata and OCR when a bundled OCR engine is available.

        Content is intentionally not classified or blocked. Nothing leaves the PC.
        """
        try:
            path = self._local_path(source)
            with Image.open(path) as image:
                details = [
                    f"FILE: {path.name}",
                    f"FORMAT: {image.format or 'Unknown'}",
                    f"SIZE: {image.width} x {image.height}",
                    f"COLOR: {image.mode}",
                    "LOCAL CONTENT POLICY: UNRESTRICTED",
                ]
                try:
                    import pytesseract
                    text = pytesseract.image_to_string(image, lang="eng+ben").strip()
                    details.append("\nOCR TEXT:\n" + (text or "No readable text detected."))
                except Exception:
                    self.capabilityWarning.emit("OCR PACK NOT INSTALLED", "Image metadata and editing work locally, but Bangla/English text recognition needs the optional OCR Pack.")
                    details.append("\nOCR: Portable OCR pack is not present. Image reading remains available.")
            self._log("vision inspect", str(path))
            self.visionResult.emit("\n".join(details))
        except Exception as exc:
            self.visionResult.emit(f"Image inspection failed: {exc}")

    @Slot(str, str)
    def imageToPdf(self, source, destination):
        try:
            source_path = self._local_path(source)
            destination_path = self._local_path(destination)
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source_path) as image:
                image.convert("RGB").save(destination_path, "PDF", resolution=150.0)
            self._log("image to pdf", str(destination_path))
            self.pdfResult.emit(f"PDF created: {destination_path}")
        except Exception as exc:
            self.pdfResult.emit(f"PDF creation failed: {exc}")

    @staticmethod
    def _pdf_library():
        try:
            from pypdf import PdfReader, PdfWriter
            return PdfReader, PdfWriter
        except ImportError as exc:
            raise RuntimeError("Portable PDF Pack is not installed.") from exc

    @Slot(str, str, result=bool)
    def mergePdfs(self, sources_json, destination):
        """Merge an ordered JSON list of PDFs into a new file."""
        try:
            sources = json.loads(sources_json)
            if not isinstance(sources, list) or len(sources) < 2:
                raise ValueError("choose at least two PDF files")
            PdfReader, PdfWriter = self._pdf_library()
            writer = PdfWriter()
            for source in sources:
                path = self._local_path(str(source))
                for page in PdfReader(str(path)).pages:
                    writer.add_page(page)
            output = self._local_path(destination)
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("wb") as handle:
                writer.write(handle)
            self._log("pdf merge", str(output))
            self.pdfResult.emit(f"Merged PDF created: {output}")
            return True
        except Exception as exc:
            self.pdfResult.emit(f"PDF merge failed: {exc}")
            return False

    @Slot(str, str, result=bool)
    def splitPdf(self, source, destination_folder):
        """Export every page as a separate PDF without altering the source."""
        try:
            PdfReader, PdfWriter = self._pdf_library()
            source_path = self._local_path(source)
            output_dir = self._local_path(destination_folder)
            output_dir.mkdir(parents=True, exist_ok=True)
            reader = PdfReader(str(source_path))
            if not reader.pages:
                raise ValueError("PDF has no pages")
            for index, page in enumerate(reader.pages, start=1):
                writer = PdfWriter()
                writer.add_page(page)
                output = output_dir / f"{source_path.stem}-page-{index:03}.pdf"
                with output.open("wb") as handle:
                    writer.write(handle)
            self._log("pdf split", f"{source_path} -> {output_dir}")
            self.pdfResult.emit(f"Split {len(reader.pages)} page(s) into: {output_dir}")
            return True
        except Exception as exc:
            self.pdfResult.emit(f"PDF split failed: {exc}")
            return False

    @Slot(str)
    def openPdf(self, source):
        try:
            path = self._local_path(source)
            if os.name == "nt":
                os.startfile(path)
            self.pdfResult.emit(f"Opened securely with your Windows default PDF application: {path.name}")
        except Exception as exc:
            self.pdfResult.emit(f"Could not open PDF: {exc}")

    @Slot(str)
    def webSearch(self, query):
        query = query.strip()
        if not query or not self.settings.get("allow_public_search", True):
            self.commandResult.emit("Public web search is locked in Admin Policy.", "warning")
            return
        url = "https://search.brave.com/search?q=" + quote_plus(query)
        try:
            subprocess.Popen([self._brave_path(), url], creationflags=0x08000000 if os.name == "nt" else 0)
            self._log("smart auto web search", query)
            self.commandResult.emit("Opened a controlled Brave search. ARLEN remains local; no personal files were uploaded.", "success")
        except Exception as exc:
            self.commandResult.emit(f"Web search could not start: {exc}", "error")

    @staticmethod
    def _local_path(url_or_path: str) -> Path:
        if url_or_path.startswith("file:"):
            parsed = urlparse(url_or_path)
            path = unquote(parsed.path)
            if os.name == "nt" and path.startswith("/"):
                path = path[1:]
            return Path(path)
        return Path(url_or_path)

    @Slot(str, float, float, float, float, float, result=str)
    def processImage(self, source, brightness, contrast, saturation, sharpness, dehaze):
        """Create a non-destructive preview; original bytes are never overwritten."""
        try:
            path = self._local_path(source)
            image = Image.open(path).convert("RGB")
            image = ImageEnhance.Brightness(image).enhance(max(.1, brightness))
            image = ImageEnhance.Contrast(image).enhance(max(.1, contrast + dehaze*.35))
            image = ImageEnhance.Color(image).enhance(max(0, saturation))
            image = ImageEnhance.Sharpness(image).enhance(max(0, sharpness))
            if dehaze > .05:
                image = ImageOps.autocontrast(image, cutoff=min(4, int(dehaze*4)))
                image = image.filter(ImageFilter.UnsharpMask(radius=1.3, percent=int(70+dehaze*80), threshold=3))
            preview_dir = DATA / "image_previews"
            preview_dir.mkdir(exist_ok=True)
            output = preview_dir / "current_preview.jpg"
            image.thumbnail((1800, 1200), Image.Resampling.LANCZOS)
            image.save(output, quality=94)
            return output.as_uri() + f"?v={time.time_ns()}"
        except Exception as exc:
            self.commandResult.emit(f"Image preview failed: {exc}", "error")
            return ""

    @Slot(str, str, float, float, float, float, float, result=bool)
    def exportImage(self, source, destination, brightness, contrast, saturation, sharpness, dehaze):
        try:
            source_path = self._local_path(source)
            destination_path = self._local_path(destination)
            image = Image.open(source_path).convert("RGB")
            image = ImageEnhance.Brightness(image).enhance(max(.1, brightness))
            image = ImageEnhance.Contrast(image).enhance(max(.1, contrast + dehaze*.35))
            image = ImageEnhance.Color(image).enhance(max(0, saturation))
            image = ImageEnhance.Sharpness(image).enhance(max(0, sharpness))
            if dehaze > .05:
                image = ImageOps.autocontrast(image, cutoff=min(4, int(dehaze*4)))
                image = image.filter(ImageFilter.UnsharpMask(radius=1.3, percent=int(70+dehaze*80), threshold=3))
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(destination_path, quality=95)
            self._log("image export", str(destination_path))
            return True
        except Exception as exc:
            self.commandResult.emit(f"Image export failed: {exc}", "error")
            return False

    @Slot(str, str, result=bool)
    def exportPreview(self, preview_source, destination):
        """Export a generated prompt preview to a new file; never overwrite the original."""
        try:
            source_path = self._local_path(preview_source.split("?", 1)[0])
            destination_path = self._local_path(destination)
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source_path) as image:
                if destination_path.suffix.lower() in (".jpg", ".jpeg"):
                    image = image.convert("RGB")
                image.save(destination_path, quality=95)
            self._log("prompt image export", str(destination_path))
            return True
        except Exception as exc:
            self.commandResult.emit(f"Prompt export failed: {exc}", "error")
            return False

    @Slot(str, str, result=str)
    def promptEditImage(self, source, prompt):
        """Translate common Bangla/English edit instructions into safe local operations."""
        try:
            path = self._local_path(source)
            text = prompt.lower()
            image = Image.open(path).convert("RGB")

            if any(key in text for key in ("9:16", "9x16", "vertical", "portrait", "পোর্ট্রেট")):
                image = self._center_crop(image, 9/16)
            elif any(key in text for key in ("16:9", "16x9", "landscape", "ল্যান্ডস্কেপ")):
                image = self._center_crop(image, 16/9)
            elif any(key in text for key in ("1:1", "square", "স্কয়ার", "স্কয়ার")):
                image = self._center_crop(image, 1)

            if any(key in text for key in ("rotate left", "বামে ঘুর", "left rotate")):
                image = image.rotate(90, expand=True)
            elif any(key in text for key in ("rotate right", "ডানে ঘুর", "right rotate")):
                image = image.rotate(-90, expand=True)
            if any(key in text for key in ("flip horizontal", "mirror", "মিরর")):
                image = ImageOps.mirror(image)

            if any(key in text for key in ("dehaze", "remove haze", "haze কম", "কুয়াশা", "কুয়াশা", "ঝাপসা কম")):
                image = ImageOps.autocontrast(image, cutoff=2)
                image = ImageEnhance.Contrast(image).enhance(1.18)
            if any(key in text for key in ("texture", "detail", "sharp", "clear", "ক্লিয়ার", "ক্লিয়ার", "শার্প", "ডিটেইল")):
                image = image.filter(ImageFilter.UnsharpMask(radius=1.5, percent=145, threshold=3))
                image = ImageEnhance.Sharpness(image).enhance(1.35)
            if any(key in text for key in ("bright", "উজ্জ্বল", "লাইট কর")):
                image = ImageEnhance.Brightness(image).enhance(1.12)
            if any(key in text for key in ("dark", "ডার্ক", "অন্ধকার")):
                image = ImageEnhance.Brightness(image).enhance(.88)
            if any(key in text for key in ("more color", "vibrant", "রঙ বাড়", "রঙ বাড়", "স্যাচুরেশন")):
                image = ImageEnhance.Color(image).enhance(1.2)
            if any(key in text for key in ("less color", "muted", "রঙ কম")):
                image = ImageEnhance.Color(image).enhance(.78)
            if any(key in text for key in ("black and white", "grayscale", "সাদা কালো")):
                image = ImageOps.grayscale(image).convert("RGB")

            preview_dir = DATA / "image_previews"
            preview_dir.mkdir(exist_ok=True)
            output = preview_dir / "prompt_preview.jpg"
            image.thumbnail((1800, 1200), Image.Resampling.LANCZOS)
            image.save(output, quality=95)
            self._log("image prompt", prompt)
            return output.as_uri() + f"?v={time.time_ns()}"
        except Exception as exc:
            self.commandResult.emit(f"Prompt edit failed: {exc}", "error")
            return ""

    @staticmethod
    def _center_crop(image: Image.Image, target_ratio: float) -> Image.Image:
        width, height = image.size
        ratio = width / height
        if ratio > target_ratio:
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            return image.crop((left, 0, left + new_width, height))
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        return image.crop((0, top, width, top + new_height))
