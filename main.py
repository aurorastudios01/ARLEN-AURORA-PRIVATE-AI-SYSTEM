from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtCore import QSize, QTimer, QUrl
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow
from shiboken6 import getCppPointer, wrapInstance

from backend import Backend


ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def main():
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
    capture_mode = "--capture-ui" in sys.argv
    if capture_mode:
        os.environ.setdefault("QT_QUICK_BACKEND", "software")
        os.environ.setdefault("QSG_RHI_BACKEND", "software")
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
        quick_window = wrapInstance(getCppPointer(window)[0], QQuickWindow)
        window.setProperty("openingVisible", False)
        window.showNormal()
        window.setWidth(width)
        window.setHeight(height)
        window.setPosition(0, 0)

        finished = {"value": False}

        def save_result(result):
            if finished["value"]:
                return
            finished["value"] = True
            output.parent.mkdir(parents=True, exist_ok=True)
            image = result.image()
            if image.isNull() or not image.save(str(output)):
                app.exit(2)
            else:
                app.quit()

        def start_capture():
            quick_window.contentItem().grabToImage(save_result, QSize(width, height))

        def capture_timeout():
            if not finished["value"]:
                finished["value"] = True
                app.exit(3)

        QTimer.singleShot(1200, start_capture)
        QTimer.singleShot(15000, capture_timeout)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
