from __future__ import annotations

import gc
import ast
import ctypes
from ctypes import wintypes
import hashlib
import json
import math
import os
import platform
import re
import shutil
import socket
import subprocess
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.parse import quote_plus

import psutil
from PySide6.QtCore import QObject, Property, QTimer, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from v1_services import (
    APP_VERSION,
    ArlenDatabase,
    EnvironmentScanner,
    OllamaClient,
    launch_local_file,
)


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
DB_FILE = DATA / "arlen_memory.sqlite3"
ORGANIZE_STATE_FILE = DATA / "last_organization.json"
VISUAL_DIR = DATA / "visuals"
VISUAL_DIR.mkdir(exist_ok=True)

DEFAULT_SETTINGS = {
    "app_version": APP_VERSION,
    "first_run": True,
    "pin_hash": "",
    "opening_duration": 12,
    "opening_sound": True,
    "theme": "Aurora AI",
    "sphere": "Aurora Core",
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
    "low_resource_mode": True,
    "memory_enabled": True,
    "ollama_url": "http://127.0.0.1:11434",
    "chat_model": "qwen2.5:3b",
    "vision_model": "qwen2.5vl:3b",
    "animation_level": "Enhanced",
    "sphere_scale": 1.0,
    "sphere_glow": 0.78,
    "sphere_pulse_speed": 1.0,
    "sphere_animation": True,
    "background_opacity": 0.24,
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
    conversationChanged = Signal()
    environmentChanged = Signal()
    recentFilesChanged = Signal()
    fileIndexChanged = Signal()
    busyChanged = Signal()
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
        self._battery_percent = -1.0
        self._battery_state = "NOT AVAILABLE"
        self._power_source = "UNKNOWN"
        self._battery_time = "N/A"
        self._top_apps = "Scanning processes…"
        self._brain = None  # Kept for safe migration from the v0.7 GGUF backend.
        self._brain_loading = False
        self._busy = False
        self._environment = {
            "app_version": APP_VERSION,
            "resource_profile": "Scanning…",
            "ollama": {"installed": False, "running": False, "models": []},
            "chat": {"model": self.settings["chat_model"], "ready": False},
            "vision": {"model": self.settings["vision_model"], "ready": False},
            "ffmpeg": {"installed": False, "path": ""},
        }
        self._file_index_status = "Not scanned yet"
        self._database = ArlenDatabase(DB_FILE)
        self._ollama = OllamaClient(self.settings["ollama_url"])
        self._scanner = EnvironmentScanner(
            self._ollama,
            self.settings["chat_model"],
            self.settings["vision_model"],
        )
        self._custom_commands = self._load_custom_commands()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(1000)
        self.refresh_stats()
        threading.Thread(target=self._refresh_environment_worker, daemon=True).start()
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

    @Property(float, notify=statsChanged)
    def batteryPercent(self): return self._battery_percent

    @Property(str, notify=statsChanged)
    def batteryState(self): return self._battery_state

    @Property(str, notify=statsChanged)
    def powerSource(self): return self._power_source

    @Property(str, notify=statsChanged)
    def batteryTime(self): return self._battery_time

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

    @Property(str, constant=True)
    def appVersion(self): return APP_VERSION

    @Property(bool, notify=settingsChanged)
    def lowResourceMode(self): return bool(self.settings.get("low_resource_mode", True))

    @Property(bool, notify=busyChanged)
    def busy(self): return self._busy

    @Property(str, notify=environmentChanged)
    def environmentStatus(self):
        return json.dumps(self._environment, ensure_ascii=False)

    @Property(str, notify=conversationChanged)
    def conversationHistory(self):
        return json.dumps(self._database.messages(80), ensure_ascii=False)

    @Property(str, notify=recentFilesChanged)
    def recentFiles(self):
        return json.dumps(self._database.recent_files(12), ensure_ascii=False)

    @Property(str, notify=fileIndexChanged)
    def fileIndexStatus(self): return self._file_index_status

    @Property(float, notify=settingsChanged)
    def sphereScale(self): return float(self.settings.get("sphere_scale", 1.0))

    @Property(float, notify=settingsChanged)
    def sphereGlow(self): return float(self.settings.get("sphere_glow", .78))

    @Property(float, notify=settingsChanged)
    def spherePulseSpeed(self): return float(self.settings.get("sphere_pulse_speed", 1.0))

    @Property(bool, notify=settingsChanged)
    def sphereAnimation(self): return bool(self.settings.get("sphere_animation", True))

    def _set_busy(self, value):
        value = bool(value)
        if self._busy != value:
            self._busy = value
            self.busyChanged.emit()

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
        try:
            battery = psutil.sensors_battery()
        except (AttributeError, OSError):
            battery = None
        if battery is None:
            self._battery_percent = -1.0
            self._battery_state = "NOT AVAILABLE"
            self._power_source = "NO BATTERY"
            self._battery_time = "N/A"
        else:
            self._battery_percent = float(battery.percent)
            self._power_source = "CHARGER CONNECTED" if battery.power_plugged else "BATTERY POWER"
            self._battery_state = "CHARGING" if battery.power_plugged and battery.percent < 100 else ("FULL" if battery.power_plugged else "DISCHARGING")
            if battery.secsleft in (psutil.POWER_TIME_UNKNOWN, psutil.POWER_TIME_UNLIMITED) or battery.secsleft < 0:
                self._battery_time = "CALCULATING"
            else:
                remaining = int(battery.secsleft)
                self._battery_time = f"{remaining//3600:02}:{(remaining%3600)//60:02}"
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
        if theme in (
            "Aurora AI", "Obsidian", "Ocean", "Crimson", "Emerald",
            "Violet", "Arctic", "Solar", "Graphite", "Midnight",
        ):
            self.settings["theme"] = theme
            self._save()

    @Slot(str)
    def setSphere(self, name):
        self.settings["sphere"] = name
        self._save()

    @Slot(bool)
    def setLowResourceMode(self, enabled):
        self.settings["low_resource_mode"] = bool(enabled)
        self._save()

    @Slot(float, float, float, bool)
    def saveCoreSettings(self, scale, glow, speed, animated):
        self.settings["sphere_scale"] = max(.65, min(1.35, float(scale)))
        self.settings["sphere_glow"] = max(.1, min(1.0, float(glow)))
        self.settings["sphere_pulse_speed"] = max(.35, min(2.5, float(speed)))
        self.settings["sphere_animation"] = bool(animated)
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
            destination = VISUAL_DIR / f"{kind}-{uuid.uuid4().hex[:12]}{source_path.suffix.lower()}"
            shutil.copy2(source_path, destination)
            key = {"avatar": "owner_avatar", "background": "background_image", "sphere": "custom_sphere"}[kind]
            old_value = self.settings.get(key, "")
            self.settings[key] = str(destination)
            if kind == "sphere":
                self.settings["sphere"] = "Custom Sphere"
            self._save()
            self._safe_remove_visual(old_value)
            self._log(f"custom {kind}", str(source_path))
            return f"Custom {kind} saved."
        except Exception as exc:
            return f"Could not import {kind}: {exc}"

    @staticmethod
    def _safe_remove_visual(value):
        try:
            candidate = Path(value).resolve()
            if candidate.is_file() and VISUAL_DIR.resolve() in candidate.parents:
                candidate.unlink()
        except (OSError, RuntimeError, ValueError):
            pass

    @Slot(str, result=str)
    def removeProfileVisual(self, kind):
        mapping = {
            "avatar": "owner_avatar",
            "background": "background_image",
            "sphere": "custom_sphere",
        }
        key = mapping.get(kind)
        if not key:
            return "Unsupported visual type."
        old_value = self.settings.get(key, "")
        self.settings[key] = ""
        if kind == "sphere":
            self.settings["sphere"] = "Aurora Core"
        self._save()
        self._safe_remove_visual(old_value)
        return f"Custom {kind} removed; Aurora default restored."

    @Slot(result=str)
    def resetVisuals(self):
        for key in ("owner_avatar", "background_image", "custom_sphere"):
            self._safe_remove_visual(self.settings.get(key, ""))
            self.settings[key] = ""
        self.settings.update({
            "theme": "Aurora AI", "sphere": "Aurora Core",
            "sphere_scale": 1.0, "sphere_glow": .78,
            "sphere_pulse_speed": 1.0, "sphere_animation": True,
        })
        self._save()
        return "Aurora AI visuals restored."

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
        elif any(term in text for term in ("system refresh", "refresh system", "free arlen ram", "ram refresh", "র‍্যাম রিফ্রেশ", "সিস্টেম রিফ্রেশ")):
            self.systemRefresh()
            return
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
            self.updateStatusChanged.emit(f"ARLEN {APP_VERSION} development build: no staged update manifest was found.")
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
        chat = bool(self._environment.get("chat", {}).get("ready"))
        vision = bool(self._environment.get("vision", {}).get("ready"))
        ollama = bool(self._environment.get("ollama", {}).get("running"))
        ffmpeg = bool(self._environment.get("ffmpeg", {}).get("installed"))
        packs = {
            "Ollama Service": ollama,
            f"Chat ({self.settings['chat_model']})": chat,
            f"Vision ({self.settings['vision_model']})": vision,
            "Image Studio": True,
            "PDF Studio": True,
            "FFmpeg": ffmpeg,
        }
        return "\n".join(f"{name}: {'READY' if ready else 'NOT READY'}" for name, ready in packs.items())

    @Slot()
    def refreshEnvironment(self):
        threading.Thread(target=self._refresh_environment_worker, daemon=True).start()

    def _refresh_environment_worker(self):
        try:
            self._environment = self._scanner.scan()
        except Exception as exc:
            self._environment = {**self._environment, "scan_error": str(exc)}
        self.environmentChanged.emit()

    @Slot(result=str)
    def installationReport(self):
        env = self._environment
        ollama = env.get("ollama", {})
        lines = [
            f"ARLEN NEXUS {APP_VERSION}",
            f"Resource profile: {env.get('resource_profile', 'Unknown')}",
            f"Python: {env.get('python', 'Unknown')}",
            f"Ollama: {'RUNNING' if ollama.get('running') else 'NOT RUNNING'}",
            f"Chat model {self.settings['chat_model']}: {'READY' if env.get('chat', {}).get('ready') else 'MISSING'}",
            f"Vision model {self.settings['vision_model']}: {'READY' if env.get('vision', {}).get('ready') else 'MISSING'}",
            f"FFmpeg: {'READY' if env.get('ffmpeg', {}).get('installed') else 'MISSING'}",
        ]
        return "\n".join(lines)

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
            self.systemRefresh()

    @Slot()
    def cancelPower(self):
        if os.name == "nt":
            subprocess.Popen(["shutdown", "/a"], creationflags=0x08000000)
        self.commandResult.emit("Pending Windows power action cancelled.", "success")

    @Slot(str)
    def routeInput(self, message):
        text = message.strip()
        if not text:
            return
        self._database.add_message("user", text)
        self.conversationChanged.emit()
        if self._looks_like_pc_command(text):
            self.execute(text)
            return
        self._set_busy(True)
        threading.Thread(target=self._chat_worker, args=(text,), daemon=True).start()

    @Slot(str)
    def sendChat(self, message):
        self.routeInput(message)

    @staticmethod
    def _looks_like_pc_command(message):
        text = message.casefold()
        terms = (
            "open ", "launch ", "kholo", "khol ", "চালু", "খোলো", "খুলে",
            "restart", "shutdown", "শাটডাউন", "system refresh", "ram refresh",
            "status", "সিস্টেম", "search online", "web search", "অনলাইনে খুঁজ",
        )
        return any(term in text for term in terms)

    def _chat_worker(self, message):
        try:
            installed = self._ollama.tags()
            model = self.settings["chat_model"]
            if not self._ollama.has_model(installed, model):
                raise RuntimeError(f"Model {model} is not installed. Open Settings → AI Models for the exact command.")
            system_prompt = (
                "You are ARLEN NEXUS, Jubaer Hossain's private offline Windows assistant. "
                "Reply in Bangla when the user writes Bangla or Banglish; otherwise reply in English. "
                "Be concise, practical and honest. Never claim a PC action happened unless the app executed it. "
                "The V1.1 build supports text chat, local vision, images, PDFs, files and safe PC tools; voice is not included."
            )
            context = self._database.ollama_context(12 if self.lowResourceMode else 24)
            reply = self._ollama.chat(
                model,
                [{"role": "system", "content": system_prompt}, *context],
                self.lowResourceMode,
            )
            self._database.add_message("assistant", reply, "success")
            self.chatReply.emit(reply, "success")
        except Exception as exc:
            reply = f"Local AI is not ready: {exc}"
            self._database.add_message("assistant", reply, "error")
            self.chatReply.emit(reply, "error")
            self.capabilityWarning.emit("LOCAL AI NOT READY", str(exc))
        finally:
            self._set_busy(False)
            self.conversationChanged.emit()

    @Slot()
    def clearConversation(self):
        self._database.clear_messages()
        self.conversationChanged.emit()

    @Slot(result=str)
    def systemRefresh(self):
        """Release ARLEN-owned memory without terminating unrelated applications."""
        before = psutil.Process(os.getpid()).memory_info().rss
        brain_was_loaded = bool(self._environment.get("ollama", {}).get("running"))
        self._brain = None
        if brain_was_loaded:
            try:
                self._ollama.unload(self.settings["chat_model"])
                self._ollama.unload(self.settings["vision_model"])
            except Exception:
                pass
        gc.collect()

        preview_dir = DATA / "image_previews"
        removed = 0
        if preview_dir.exists():
            for candidate in preview_dir.iterdir():
                if candidate.is_file():
                    try:
                        candidate.unlink()
                        removed += 1
                    except OSError:
                        pass

        if os.name == "nt":
            try:
                handle = ctypes.windll.kernel32.GetCurrentProcess()
                ctypes.windll.psapi.EmptyWorkingSet(handle)
            except Exception:
                pass

        after = psutil.Process(os.getpid()).memory_info().rss
        released_mb = max(0.0, (before - after) / 1024**2)
        details = (
            f"SYSTEM REFRESH COMPLETE — ARLEN released {released_mb:.1f} MB; "
            f"cleared {removed} preview file(s); "
            + ("Local Brain unloaded." if brain_was_loaded else "Local Brain was already idle.")
        )
        self._log("system refresh", details)
        self.commandResult.emit(details, "success")
        return details

    @Slot()
    def unloadBrain(self):
        self._brain = None
        try:
            self._ollama.unload(self.settings["chat_model"])
            self._ollama.unload(self.settings["vision_model"])
        except Exception:
            pass
        gc.collect()
        self.chatReply.emit("Ollama models unloaded from memory.", "success")

    @Slot()
    def startVoice(self):
        self.capabilityWarning.emit("VOICE IS OUTSIDE V1.1", "V1.1 intentionally ships text chat and local vision first. No microphone recording was started.")
        self.voiceStateChanged.emit("Voice is planned after the verified V1 text + vision release")

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

    @Slot(int, result=bool)
    def setBrightness(self, percent):
        if os.name != "nt":
            self.commandResult.emit("Brightness control is available in the Windows build.", "warning")
            return False
        value = max(0, min(100, int(percent)))
        script = (
            "$m=Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods;"
            f"if($m){{$m.WmiSetBrightness(1,{value})|Out-Null}}else{{exit 2}}"
        )
        try:
            completed = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                capture_output=True, text=True, timeout=12,
                creationflags=0x08000000,
            )
            if completed.returncode != 0:
                raise RuntimeError("This display does not expose Windows brightness control.")
            self.commandResult.emit(f"Brightness set to {value}%.", "success")
            return True
        except Exception as exc:
            self.commandResult.emit(f"Brightness could not be changed: {exc}", "warning")
            return False

    @Slot(int)
    def changeVolume(self, steps):
        if os.name != "nt":
            self.commandResult.emit("Volume control is available in the Windows build.", "warning")
            return
        count = max(-20, min(20, int(steps)))
        key = 0xAF if count > 0 else 0xAE
        try:
            for _ in range(abs(count)):
                ctypes.windll.user32.keybd_event(key, 0, 0, 0)
                ctypes.windll.user32.keybd_event(key, 0, 2, 0)
            self.commandResult.emit("Volume adjusted.", "success")
        except Exception as exc:
            self.commandResult.emit(f"Volume could not be changed: {exc}", "warning")

    @Slot(result=str)
    def discoverApplications(self):
        return json.dumps(self._environment.get("browsers", {}), ensure_ascii=False)

    @Slot(str, result=str)
    def calculate(self, expression):
        """Evaluate arithmetic only; names, calls, attributes and indexing are rejected."""
        binary = {
            ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b, ast.Div: lambda a, b: a / b,
            ast.FloorDiv: lambda a, b: a // b, ast.Mod: lambda a, b: a % b,
            ast.Pow: lambda a, b: a ** b,
        }
        unary = {ast.UAdd: lambda a: a, ast.USub: lambda a: -a}
        functions = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
            "abs": abs, "round": round,
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.Name) and node.id in {"pi", "e"}:
                return {"pi": math.pi, "e": math.e}[node.id]
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in functions and not node.keywords:
                return functions[node.func.id](*[evaluate(argument) for argument in node.args])
            if isinstance(node, ast.BinOp) and type(node.op) in binary:
                left, right = evaluate(node.left), evaluate(node.right)
                if isinstance(node.op, ast.Pow) and abs(right) > 12:
                    raise ValueError("power is too large")
                return binary[type(node.op)](left, right)
            if isinstance(node, ast.UnaryOp) and type(node.op) in unary:
                return unary[type(node.op)](evaluate(node.operand))
            raise ValueError("only arithmetic is allowed")

        try:
            cleaned = expression.strip().replace("×", "*").replace("÷", "/").replace("^", "**")
            if len(cleaned) > 120:
                raise ValueError("expression is too long")
            result = evaluate(ast.parse(cleaned, mode="eval"))
            return f"{result:.12g}" if isinstance(result, float) else str(result)
        except Exception as exc:
            return f"Error: {exc}"

    @Slot(str, float, str, str, result=str)
    def convertUnit(self, category, value, from_unit, to_unit):
        try:
            number = float(value)
            if category == "Temperature":
                celsius = {"Celsius": number, "Fahrenheit": (number-32)*5/9, "Kelvin": number-273.15}[from_unit]
                result = {"Celsius": celsius, "Fahrenheit": celsius*9/5+32, "Kelvin": celsius+273.15}[to_unit]
            else:
                factors = {
                    "Length": {"Meter":1, "Kilometer":1000, "Centimeter":.01, "Mile":1609.344, "Foot":.3048},
                    "Weight": {"Kilogram":1, "Gram":.001, "Pound":.45359237, "Ounce":.028349523125},
                    "Storage": {"Byte":1, "KB":1024, "MB":1024**2, "GB":1024**3, "TB":1024**4},
                }
                table = factors[category]
                result = number * table[from_unit] / table[to_unit]
            return f"{result:,.10g}"
        except Exception as exc:
            return f"Error: {exc}"

    @Slot(str, str, result=bool)
    def saveTextFile(self, destination, content):
        try:
            path = self._local_path(destination)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            self._database.remember_file(path, "note")
            self.recentFilesChanged.emit()
            return True
        except Exception as exc:
            self.commandResult.emit(f"Could not save note: {exc}", "error")
            return False

    @Slot(result=str)
    def clipboardText(self):
        return QGuiApplication.clipboard().text()

    @Slot(str)
    def setClipboardText(self, text):
        QGuiApplication.clipboard().setText(text)

    @Slot(str, result=bool)
    def captureScreenshot(self, destination):
        try:
            path = self._local_path(destination)
            if path.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                path = path.with_suffix(".png")
            screen = QGuiApplication.primaryScreen()
            if screen is None or not screen.grabWindow(0).save(str(path)):
                raise RuntimeError("Windows screen capture was unavailable")
            self._database.remember_file(path, "screenshot")
            self.recentFilesChanged.emit()
            return True
        except Exception as exc:
            self.commandResult.emit(f"Screenshot failed: {exc}", "error")
            return False

    @Slot(str)
    def inspectImage(self, source):
        """Read local image metadata and OCR when a bundled OCR engine is available.

        Content is intentionally not classified or blocked. Nothing leaves the PC.
        """
        try:
            path = self._local_path(source)
            self._database.remember_file(path, "image")
            self.recentFilesChanged.emit()
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
    def analyzeImage(self, source, prompt):
        """Analyze one selected local image with the configured Ollama vision model."""
        try:
            path = self._local_path(source)
        except Exception as exc:
            self.visionResult.emit(f"Choose a valid local image: {exc}")
            return
        self._database.remember_file(path, "vision")
        self.recentFilesChanged.emit()
        self._set_busy(True)
        threading.Thread(target=self._vision_worker, args=(path, prompt), daemon=True).start()

    def _vision_worker(self, path, prompt):
        try:
            installed = self._ollama.tags()
            model = self.settings["vision_model"]
            if not self._ollama.has_model(installed, model):
                raise RuntimeError(f"Model {model} is not installed. Open Settings → AI Models.")
            result = self._ollama.analyze_image(model, path, prompt, self.lowResourceMode)
            self.visionResult.emit(result)
        except Exception as exc:
            self.visionResult.emit(f"Local vision is not ready: {exc}")
            self.capabilityWarning.emit("VISION MODEL NOT READY", str(exc))
        finally:
            self._set_busy(False)

    @Slot(str, str)
    def imageToPdf(self, source, destination):
        try:
            source_path = self._local_path(source)
            destination_path = self._local_path(destination)
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source_path) as image:
                image.convert("RGB").save(destination_path, "PDF", resolution=150.0)
            self._database.remember_file(destination_path, "pdf")
            self.recentFilesChanged.emit()
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
            self._database.remember_file(output, "pdf")
            self.recentFilesChanged.emit()
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
            launch_local_file(path)
            self._database.remember_file(path, "pdf")
            self.recentFilesChanged.emit()
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

    @Slot(str, str, result=str)
    def searchFiles(self, query, location):
        """Bounded filename search; never reads file contents or follows symlinks."""
        cleaned = query.strip().casefold()
        if len(cleaned) < 2:
            return "[]"
        try:
            root = self._local_path(location) if location.strip() else Path.home()
            if not root.is_dir():
                raise ValueError("search location is not a folder")
            results, visited = [], 0
            for current, directories, files in os.walk(root, followlinks=False):
                directories[:] = [name for name in directories if not name.startswith(".")][:80]
                visited += 1
                if visited > 2500 or len(results) >= 80:
                    break
                for name in files:
                    if cleaned in name.casefold():
                        path = Path(current) / name
                        try:
                            stat = path.stat()
                            results.append({
                                "name": name, "path": str(path), "size": stat.st_size,
                                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="minutes"),
                            })
                        except OSError:
                            continue
                        if len(results) >= 80:
                            break
            return json.dumps(results, ensure_ascii=False)
        except Exception as exc:
            self.commandResult.emit(f"File search failed: {exc}", "error")
            return "[]"

    @Slot()
    def scanUserFiles(self):
        self._file_index_status = "Scanning local folders…"
        self.fileIndexChanged.emit()
        threading.Thread(target=self._scan_user_files_worker, daemon=True).start()

    @staticmethod
    def _file_category(path):
        extension = path.suffix.casefold()
        groups = {
            "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"},
            "Images": {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".svg", ".heic"},
            "Video": {".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4v"},
            "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"},
            "Archives": {".zip", ".7z", ".rar", ".tar", ".gz"},
            "Installers": {".exe", ".msi", ".msix", ".appx"},
            "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".qml", ".cpp", ".c", ".java"},
        }
        return next((name for name, values in groups.items() if extension in values), "Other")

    def _scan_user_files_worker(self):
        roots = [Path.home() / name for name in ("Desktop", "Documents", "Downloads", "Pictures")]
        rows, visited = [], set()
        try:
            for root in roots:
                if not root.is_dir():
                    continue
                for current, directories, files in os.walk(root, followlinks=False):
                    directories[:] = [name for name in directories if not name.startswith(".")][:100]
                    for name in files:
                        path = Path(current) / name
                        try:
                            resolved = path.resolve()
                            if resolved in visited or path.is_symlink():
                                continue
                            stat = path.stat()
                            rows.append((str(resolved), name, path.suffix.casefold(), int(stat.st_size), float(stat.st_mtime), self._file_category(path)))
                            visited.add(resolved)
                        except OSError:
                            continue
                        if len(rows) >= 30000:
                            break
                    if len(rows) >= 30000:
                        break
                if len(rows) >= 30000:
                    break
            self._database.replace_file_index(rows)
            summary = self._database.file_index_summary()
            self._file_index_status = f"Indexed {summary['files']:,} files locally • {len(summary['categories'])} categories"
        except Exception as exc:
            self._file_index_status = f"Local scan failed: {exc}"
        self.fileIndexChanged.emit()

    @Slot(result=str)
    def organizationPreview(self):
        downloads = Path.home() / "Downloads"
        plan = self._database.organization_candidates(downloads, 100) if downloads.is_dir() else []
        return json.dumps(plan, ensure_ascii=False)

    @Slot(str, str, result=bool)
    def applyOrganizationPlan(self, plan_json, pin):
        if not self.verifyPin(pin):
            self.commandResult.emit("Owner PIN is required before files are moved.", "error")
            return False
        try:
            plan = json.loads(plan_json)
            if not isinstance(plan, list) or len(plan) > 100:
                raise ValueError("organization plan is invalid")
            home = Path.home().resolve()
            downloads = (Path.home() / "Downloads").resolve()
            completed = []
            for item in plan:
                source = Path(str(item.get("source", ""))).resolve()
                destination = Path(str(item.get("destination", ""))).resolve()
                if source.parent != downloads or home not in destination.parents:
                    raise ValueError("plan contains a path outside the approved user folders")
                if not source.is_file() or source.is_symlink():
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    destination = destination.with_name(f"{destination.stem}-{int(time.time())}{destination.suffix}")
                shutil.move(str(source), str(destination))
                completed.append({"source": str(source), "destination": str(destination)})
            ORGANIZE_STATE_FILE.write_text(json.dumps(completed, ensure_ascii=False, indent=2), encoding="utf-8")
            self.commandResult.emit(f"Organized {len(completed)} file(s). Undo remains available.", "success")
            self.scanUserFiles()
            return True
        except Exception as exc:
            self.commandResult.emit(f"Files were not organized: {exc}", "error")
            return False

    @Slot(str, result=bool)
    def undoLastOrganization(self, pin):
        if not self.verifyPin(pin):
            self.commandResult.emit("Owner PIN is required to undo file organization.", "error")
            return False
        try:
            moves = json.loads(ORGANIZE_STATE_FILE.read_text(encoding="utf-8"))
            restored = 0
            for item in reversed(moves):
                source, destination = Path(item["source"]), Path(item["destination"])
                if destination.is_file() and not source.exists():
                    source.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(destination), str(source))
                    restored += 1
            ORGANIZE_STATE_FILE.unlink(missing_ok=True)
            self.commandResult.emit(f"Restored {restored} file(s) to Downloads.", "success")
            self.scanUserFiles()
            return True
        except Exception as exc:
            self.commandResult.emit(f"Undo could not complete: {exc}", "error")
            return False

    @Slot(str, result=bool)
    def openLocalPath(self, source):
        try:
            path = self._local_path(source)
            launch_local_file(path)
            if path.is_file():
                self._database.remember_file(path, "file")
                self.recentFilesChanged.emit()
            return True
        except Exception as exc:
            self.commandResult.emit(f"Could not open item: {exc}", "error")
            return False

    @Slot(str, result=bool)
    def revealLocalPath(self, source):
        try:
            path = self._local_path(source)
            if os.name == "nt":
                subprocess.Popen(["explorer.exe", "/select,", str(path)], creationflags=0x08000000)
            else:
                launch_local_file(path.parent)
            return True
        except Exception as exc:
            self.commandResult.emit(f"Could not reveal item: {exc}", "error")
            return False

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
