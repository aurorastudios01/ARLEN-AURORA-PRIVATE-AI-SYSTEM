# ARLEN NEXUS v0.5 single-file Windows build.
# The executable extracts its private runtime to Windows Temp at launch.
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
    a.binaries,
    a.datas,
    [],
    name="ARLEN-NEXUS-v0.5",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    runtime_tmpdir=None,
)
