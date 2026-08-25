import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication
from PIL import Image

import backend as backend_module
from backend import Backend


APP = QCoreApplication.instance() or QCoreApplication([])


class ArlenCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.settings_file = self.base / "settings.json"
        self.commands_file = self.base / "custom_commands.json"
        self.log_file = self.base / "activity.jsonl"
        self.backup_dir = self.base / "backups"
        self.update_state_file = self.base / "update_state.json"
        self.backup_dir.mkdir()
        self.patchers = [
            patch.object(backend_module, "SETTINGS_FILE", self.settings_file),
            patch.object(backend_module, "COMMANDS_FILE", self.commands_file),
            patch.object(backend_module, "LOG_FILE", self.log_file),
            patch.object(backend_module, "BACKUP_DIR", self.backup_dir),
            patch.object(backend_module, "UPDATE_STATE_FILE", self.update_state_file),
        ]
        for item in self.patchers:
            item.start()
        self.backend = Backend()
        self.backend.timer.stop()

    def tearDown(self):
        for item in reversed(self.patchers):
            item.stop()
        self.temp.cleanup()

    def test_initial_pin_and_owner_profile(self):
        self.assertFalse(self.backend.setInitialPin("12"))
        self.assertTrue(self.backend.setInitialPin("8642"))
        self.assertTrue(self.backend.verifyPin("8642"))
        self.assertTrue(self.backend.saveOwnerProfile("Jubaer Hossain", "Jubaer", "Owner", "System ready", "8642"))
        self.assertEqual(self.backend.ownerCallName, "Jubaer")
        saved = json.loads(self.settings_file.read_text(encoding="utf-8"))
        self.assertEqual(saved["welcome_message"], "System ready")

    def test_change_pin(self):
        self.backend.setInitialPin("8642")
        self.assertFalse(self.backend.changePin("0000", "9753"))
        self.assertTrue(self.backend.changePin("8642", "9753"))
        self.assertTrue(self.backend.verifyPin("9753"))

    def test_command_builder_persistence(self):
        self.backend.setInitialPin("8642")
        self.assertTrue(self.backend.addCustomCommand("Work Mode", "open brave\nopen documents", "Ready", "8642"))
        stored = json.loads(self.commands_file.read_text(encoding="utf-8"))
        self.assertEqual(stored[0]["trigger"], "Work Mode")
        self.assertEqual(len(stored[0]["actions"]), 2)

    def test_macro_power_action_is_not_allow_listed(self):
        completed = []
        self.backend._run_macro_action("shutdown computer", completed)
        self.assertIn("Skipped unsupported action", completed[0])

    def test_owner_backup(self):
        self.backend.setInitialPin("8642")
        result = self.backend.backupOwnerData("8642")
        self.assertIn("backup created", result)
        self.assertEqual(len(list(self.backup_dir.glob("owner-data-*.json"))), 1)

    def test_image_crop_and_processing(self):
        source = self.base / "sample.png"
        Image.new("RGB", (800, 600), "#335577").save(source)
        cropped = self.backend._center_crop(Image.open(source), 1.0)
        self.assertEqual(cropped.size, (600, 600))
        result = self.backend.processImage(str(source), 1.1, 1.1, 1.0, 1.2, 0.2)
        self.assertTrue(result.startswith("file:"))

    def test_image_to_pdf(self):
        source = self.base / "sample.png"
        output = self.base / "sample.pdf"
        Image.new("RGB", (320, 240), "white").save(source)
        self.backend.imageToPdf(str(source), str(output))
        self.assertTrue(output.exists())
        self.assertGreater(output.stat().st_size, 1000)

    def test_prompt_edit_export(self):
        source = self.base / "sample.png"
        output = self.base / "edited.jpg"
        Image.new("RGB", (800, 600), "#335577").save(source)
        preview = self.backend.promptEditImage(str(source), "1:1 crop, dehaze and sharp")
        self.assertTrue(self.backend.exportPreview(preview, str(output)))
        self.assertTrue(output.exists())

    def test_custom_profile_visual_import(self):
        source = self.base / "avatar.png"
        Image.new("RGB", (120, 120), "#224466").save(source)
        with patch.object(backend_module, "DATA", self.base):
            result = self.backend.importProfileVisual(str(source), "avatar")
        self.assertIn("saved", result)
        self.assertTrue(self.backend.settings["owner_avatar"])

    def test_pack_status_core_packs(self):
        status = self.backend.packStatus()
        self.assertIn("Image: READY", status)
        self.assertIn("PDF: READY", status)

    def test_update_manifest_absence_is_safe(self):
        messages = []
        self.backend.updateStatusChanged.connect(messages.append)
        self.backend.checkForUpdates()
        APP.processEvents()
        self.assertTrue(messages)
        self.assertFalse(self.backend.verifyStagedUpdate())

    def test_staged_update_checksum_verification(self):
        updates = self.base / "updates"
        staged = updates / "staging" / "qml"
        staged.mkdir(parents=True)
        payload = b"verified update bytes"
        (staged / "Main.qml").write_bytes(payload)
        import hashlib
        manifest = {"version": "0.3.1", "files": [{"path": "qml/Main.qml", "sha256": hashlib.sha256(payload).hexdigest()}]}
        (updates / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with patch.object(backend_module, "ROOT", self.base):
            self.assertTrue(self.backend.verifyStagedUpdate())

    def test_update_apply_and_rollback(self):
        self.backend.setInitialPin("8642")
        updates = self.base / "updates"
        staged = updates / "staging"
        staged.mkdir(parents=True)
        destination = self.base / "component.txt"
        destination.write_text("old", encoding="utf-8")
        payload = b"new verified bytes"
        (staged / "component.txt").write_bytes(payload)
        import hashlib
        manifest = {"version": "0.3.1", "files": [{"path": "component.txt", "sha256": hashlib.sha256(payload).hexdigest()}]}
        (updates / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with patch.object(backend_module, "ROOT", self.base):
            self.assertFalse(self.backend.applyStagedUpdate("0000"))
            self.assertTrue(self.backend.applyStagedUpdate("8642"))
            self.assertEqual(destination.read_text(encoding="utf-8"), "new verified bytes")
            self.assertTrue(self.backend.rollbackLastUpdate("8642"))
            self.assertEqual(destination.read_text(encoding="utf-8"), "old")

    def test_update_rejects_protected_path(self):
        for value in ("../outside.txt", "/absolute.txt", "updates/manifest.json", "UserData/settings.json"):
            with self.assertRaises(ValueError):
                self.backend._safe_update_relative_path(value)

    def test_pdf_merge_and_split(self):
        first = self.base / "first.pdf"
        second = self.base / "second.pdf"
        merged = self.base / "merged.pdf"
        split_dir = self.base / "split"
        Image.new("RGB", (100, 100), "white").save(first, "PDF")
        Image.new("RGB", (100, 100), "black").save(second, "PDF")
        self.assertTrue(self.backend.mergePdfs(json.dumps([str(first), str(second)]), str(merged)))
        self.assertTrue(self.backend.splitPdf(str(merged), str(split_dir)))
        self.assertEqual(len(list(split_dir.glob("*.pdf"))), 2)

    def test_voice_wake_word_normalization(self):
        with patch.object(self.backend, "execute") as execute:
            self.backend.interpretVoiceText("Hey ARLEN Brave kholo")
            execute.assert_called_once_with("brave kholo")

    def test_brave_command_uses_hidden_process_launch(self):
        with patch.object(backend_module.subprocess, "Popen") as popen:
            self.backend._execute_worker("open brave")
            self.assertTrue(popen.called)

    def test_restart_requires_confirmation(self):
        messages = []
        self.backend.commandResult.connect(lambda message, level: messages.append((message, level)))
        self.backend._execute_worker("restart computer")
        APP.processEvents()
        self.assertIn("REQUIRES_CONFIRMATION", messages[-1][0])

    def test_public_search_respects_admin_policy(self):
        messages = []
        self.backend.commandResult.connect(lambda message, level: messages.append((message, level)))
        self.backend.settings["allow_public_search"] = False
        self.backend.webSearch("test")
        APP.processEvents()
        self.assertIn("locked", messages[-1][0].lower())

    def test_battery_charger_telemetry(self):
        battery = type("Battery", (), {"percent": 72.0, "power_plugged": True, "secsleft": 3600})()
        with patch.object(backend_module.psutil, "sensors_battery", return_value=battery):
            self.backend.refresh_stats()
        self.assertEqual(self.backend.batteryPercent, 72.0)
        self.assertEqual(self.backend.batteryState, "CHARGING")
        self.assertEqual(self.backend.powerSource, "CHARGER CONNECTED")
        self.assertEqual(self.backend.batteryTime, "01:00")

    def test_system_refresh_is_safe_and_clears_arlen_previews(self):
        preview_dir = self.base / "image_previews"
        preview_dir.mkdir()
        (preview_dir / "preview.jpg").write_bytes(b"temporary")
        self.backend._brain = object()
        messages = []
        self.backend.commandResult.connect(lambda message, level: messages.append((message, level)))
        with patch.object(backend_module, "DATA", self.base):
            result = self.backend.systemRefresh()
        self.assertIsNone(self.backend._brain)
        self.assertFalse((preview_dir / "preview.jpg").exists())
        self.assertIn("SYSTEM REFRESH COMPLETE", result)
        self.assertEqual(messages[-1][1], "success")

    def test_system_details_are_valid_json(self):
        details = json.loads(self.backend.systemDetails())
        self.assertIn("total_ram_gb", details)
        self.assertIn("logical_cpu", details)


if __name__ == "__main__":
    unittest.main(verbosity=2)
