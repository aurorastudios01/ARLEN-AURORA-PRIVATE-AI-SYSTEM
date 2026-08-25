# Windows portable one-folder build definition.
# Run only in the release build environment; end users do not run this file.

from PyInstaller.utils.hooks import collect_all

pyside_data, pyside_bins, pyside_hidden = collect_all("PySide6")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=pyside_bins,
    datas=pyside_data + [
        ("qml", "qml"),
        ("assets", "assets"),
        ("models/README.txt", "models"),
        ("updates/manifest.example.json", "updates"),
    ],
    hiddenimports=pyside_hidden + ["psutil", "PIL", "PIL.ImageQt", "pypdf"],
    excludes=["tkinter", "unittest"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ARLEN NEXUS",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/arlen-nexus.ico",
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, name="ARLEN NEXUS Portable")
