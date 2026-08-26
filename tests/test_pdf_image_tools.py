"""Regression tests for the V1.1 PDF and image tool additions."""
from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PIL = pytest.importorskip("PIL")
pypdf = pytest.importorskip("pypdf")
from PIL import Image  # noqa: E402


def _make_pdf(path: Path, text: str = "ARLEN NEXUS local document") -> Path:
    image = Image.new("RGB", (612, 792), "white")
    image.save(path, "PDF")
    return path


def _make_image(path: Path, size=(800, 600)) -> Path:
    Image.new("RGB", size, (30, 60, 120)).save(path)
    return path


@pytest.fixture()
def backend(tmp_path, monkeypatch):
    pytest.importorskip("PySide6")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    import backend as backend_module

    instance = object.__new__(backend_module.Backend)
    instance.settings = backend_module.DEFAULT_SETTINGS.copy()
    instance._database = types.SimpleNamespace(remember_file=lambda *a, **k: None)
    instance.pdfResult = types.SimpleNamespace(emit=lambda *a: None)
    instance.commandResult = types.SimpleNamespace(emit=lambda *a: None)
    instance.recentFilesChanged = types.SimpleNamespace(emit=lambda: None)
    instance._log = lambda *a, **k: None
    return instance


def test_rotate_pdf_creates_new_file(backend, tmp_path):
    source = _make_pdf(tmp_path / "in.pdf")
    output = tmp_path / "rotated.pdf"
    assert backend.rotatePdf(str(source), str(output), 90) is True
    assert output.exists() and source.exists()


def test_rotate_pdf_rejects_invalid_angle(backend, tmp_path):
    source = _make_pdf(tmp_path / "in.pdf")
    assert backend.rotatePdf(str(source), str(tmp_path / "out.pdf"), 45) is False


def test_watermark_pdf_writes_output(backend, tmp_path):
    source = _make_pdf(tmp_path / "in.pdf")
    output = tmp_path / "marked.pdf"
    assert backend.watermarkPdf(str(source), str(output), "ARLEN") is True
    assert output.exists() and output.stat().st_size > 0


def test_watermark_pdf_requires_text(backend, tmp_path):
    source = _make_pdf(tmp_path / "in.pdf")
    assert backend.watermarkPdf(str(source), str(tmp_path / "o.pdf"), "  ") is False


def test_search_pdf_returns_json_list(backend, tmp_path):
    source = _make_pdf(tmp_path / "in.pdf")
    assert backend.searchPdf(str(source), "nothing-here").startswith("[")


def test_resize_image_keeps_ratio(backend, tmp_path):
    source = _make_image(tmp_path / "in.png")
    output = tmp_path / "small.png"
    assert backend.resizeImage(str(source), str(output), 400, 400, True) is True
    with Image.open(output) as result:
        assert result.size == (400, 300)


def test_resize_image_exact(backend, tmp_path):
    source = _make_image(tmp_path / "in.png")
    output = tmp_path / "exact.png"
    assert backend.resizeImage(str(source), str(output), 320, 320, False) is True
    with Image.open(output) as result:
        assert result.size == (320, 320)


def test_convert_image_format(backend, tmp_path):
    source = _make_image(tmp_path / "in.png")
    output = tmp_path / "out.jpg"
    assert backend.convertImage(str(source), str(output)) is True
    with Image.open(output) as result:
        assert result.format == "JPEG"


def test_convert_image_rejects_unknown_format(backend, tmp_path):
    source = _make_image(tmp_path / "in.png")
    assert backend.convertImage(str(source), str(tmp_path / "out.xyz")) is False


def test_crop_image_ratio(backend, tmp_path):
    source = _make_image(tmp_path / "in.png")
    output = tmp_path / "square.jpg"
    assert backend.cropImage(str(source), str(output), "1:1") is True
    with Image.open(output) as result:
        assert result.size[0] == result.size[1]


def test_crop_image_rejects_unknown_ratio(backend, tmp_path):
    source = _make_image(tmp_path / "in.png")
    assert backend.cropImage(str(source), str(tmp_path / "o.jpg"), "5:7") is False


def test_original_files_are_never_modified(backend, tmp_path):
    source = _make_image(tmp_path / "in.png")
    before = source.read_bytes()
    backend.resizeImage(str(source), str(tmp_path / "a.png"), 100, 100, True)
    backend.cropImage(str(source), str(tmp_path / "b.jpg"), "1:1")
    assert source.read_bytes() == before
