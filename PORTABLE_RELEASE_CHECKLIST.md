# ARLEN NEXUS Portable Release Gate

A ZIP must not be labelled as an end-user release until every item passes.

- Build on 64-bit Windows using `ARLEN_NEXUS.spec`.
- Confirm `ARLEN NEXUS.exe` opens with no console window.
- Test on a clean Windows user account without Python, VS Code or Visual Studio.
- Confirm first-run PIN creation and second-launch persistence.
- Confirm owner profile survives application-folder replacement.
- Confirm Ctrl+Alt+A restores the window.
- Confirm Brave-first app launch and offline mode.
- Confirm CPU/RAM/disk/network statistics update.
- Confirm image preview/export and Image-to-PDF.
- Confirm local images are never blocked, blurred, deleted or uploaded.
- Confirm power actions require confirmation and remain cancellable.
- Confirm capability packs can be absent without crashing the core.
- Confirm failed update restores the previous application files.
- Package the tested portable folder; never package the source tree as the release.
