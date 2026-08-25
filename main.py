from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from backend import Backend


ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def main():
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
    capture_mode = "--capture-ui" in sys.argv
    app = QGuiApplication([sys.argv[0]] if capture_mode else sys.argv)
    app.setApplicationName("ARLEN NEXUS")
    app.setOrganizationName("Jubaer Hossain")
    app.setWindowIcon(QIcon(str(ROOT / "assets" / "arlen-nexus-icon.png")))
    engine = QQmlApplicationEngine()
    backend = Backend()
    if capture_mode:
        backend.settings["first_run"] = False
        backend.settings["opening_sound"] = False
    engine.rootContext().setContextProperty("backend", backend)
    engine.load(QUrl.fromLocalFile(str(ROOT / "qml" / "Main.qml")))
    if not engine.rootObjects():
        return 1
    if capture_mode:
        marker = sys.argv.index("--capture-ui")
        output = Path(sys.argv[marker + 1]).resolve()
        width = max(900, int(sys.argv[marker + 2]))
        height = max(680, int(sys.argv[marker + 3]))
        window = engine.rootObjects()[0]
        window.setProperty("openingVisible", False)
        window.showNormal()
        window.setWidth(width)
        window.setHeight(height)
        window.setPosition(0, 0)

        def save_capture():
            output.parent.mkdir(parents=True, exist_ok=True)
            image = window.grabWindow()
            if image.isNull() or not image.save(str(output)):
                app.exit(2)
            else:
                app.quit()

        QTimer.singleShot(2500, save_capture)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
