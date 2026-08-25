import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from v1_services import ArlenDatabase, OllamaClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


class V11ServiceTests(unittest.TestCase):
    def test_sqlite_memory_is_bounded_and_ordered(self):
        with tempfile.TemporaryDirectory() as folder:
            database = ArlenDatabase(Path(folder) / "memory.sqlite3")
            database.add_message("user", "hello")
            database.add_message("assistant", "hi")
            self.assertEqual([item["role"] for item in database.messages()], ["user", "assistant"])
            self.assertEqual(database.ollama_context()[-1]["content"], "hi")
            database.clear_messages()
            self.assertEqual(database.messages(), [])

    def test_recent_files_only_returns_existing_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            database = ArlenDatabase(base / "memory.sqlite3")
            existing = base / "document.pdf"
            existing.write_bytes(b"pdf")
            database.remember_file(existing, "pdf")
            database.remember_file(base / "missing.png", "image")
            recent = database.recent_files()
            self.assertEqual(len(recent), 1)
            self.assertEqual(recent[0]["kind"], "pdf")

    def test_file_index_builds_downloads_organization_preview(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            downloads = base / "Downloads"
            downloads.mkdir()
            image = downloads / "photo.png"
            image.write_bytes(b"image")
            database = ArlenDatabase(base / "memory.sqlite3")
            database.replace_file_index([(
                str(image.resolve()), image.name, image.suffix, image.stat().st_size,
                image.stat().st_mtime, "Images",
            )])
            self.assertEqual(database.file_index_summary()["files"], 1)
            plan = database.organization_candidates(downloads)
            self.assertEqual(plan[0]["category"], "Images")
            self.assertIn("ARLEN Organized", plan[0]["destination"])

    def test_ollama_model_matching_accepts_explicit_or_default_tag(self):
        self.assertTrue(OllamaClient.has_model(["qwen2.5:3b"], "qwen2.5:3b"))
        self.assertTrue(OllamaClient.has_model(["qwen2.5:latest"], "qwen2.5:3b"))
        self.assertFalse(OllamaClient.has_model(["llama3.2:3b"], "qwen2.5:3b"))

    def test_low_resource_chat_payload(self):
        captured = {}

        def fake_open(request, timeout):
            captured["url"] = request.full_url
            captured["payload"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse({"message": {"content": "Ready"}})

        client = OllamaClient("http://127.0.0.1:11434")
        with patch("urllib.request.urlopen", side_effect=fake_open):
            reply = client.chat("qwen2.5:3b", [{"role": "user", "content": "Hi"}], True)
        self.assertEqual(reply, "Ready")
        self.assertEqual(captured["payload"]["options"]["num_ctx"], 1536)
        self.assertEqual(captured["payload"]["options"]["num_predict"], 256)
        self.assertTrue(captured["url"].endswith("/api/chat"))

    def test_vision_payload_embeds_selected_image(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / "example.png"
            image.write_bytes(b"local-image")
            captured = {}

            def fake_open(request, timeout):
                captured.update(json.loads(request.data.decode("utf-8")))
                return FakeResponse({"message": {"content": "A local image"}})

            client = OllamaClient()
            with patch("urllib.request.urlopen", side_effect=fake_open):
                result = client.analyze_image("qwen2.5vl:3b", image, "Describe", True)
            self.assertEqual(result, "A local image")
            self.assertEqual(captured["model"], "qwen2.5vl:3b")
            self.assertTrue(captured["messages"][0]["images"][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
