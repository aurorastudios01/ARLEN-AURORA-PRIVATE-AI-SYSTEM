# ARLEN NEXUS v0.7 — Project Handover and Continuation Memory

Last updated: 25 August 2026  
Repository: `arlenray0113-cyber/ARLEN-NEXUS-PRIVATE` (private)  
Owner, concept and direction: Jubaer Hossain

## 1. Purpose of this file

This file is the authoritative continuation guide for another account, coding assistant or developer. Read it before editing. Preserve privacy, owner authority, modular/offline-first operation, separate UserData and truthful capability reporting.

## 2. Product contract

ARLEN NEXUS is a proper Windows application, not a source ZIP. The owner must not need Python, an editor, Ollama, llama.cpp, Node, Visual Studio or other development tools. Optional intelligence runtimes must eventually ship as portable capability packs.

- Stable Core: interface, command engine, owner policy, system telemetry, Image/PDF foundations and updater safety.
- Capability Packs: Local Brain, Voice, Vision/OCR, advanced Image, PDF and Theme/Sphere.
- Personal data: `%LOCALAPPDATA%\ARLEN NEXUS\UserData`.
- Installed app: `%LOCALAPPDATA%\Programs\ARLEN NEXUS`.
- Upgrades use the same Inno Setup AppId and must never overwrite UserData.

## 3. Architecture

- `main.py`: Qt application startup, QML engine and window/taskbar icon.
- `backend.py`: Qt-exposed backend, settings, policy, commands, telemetry, Image/PDF tools, capability warnings, updater and System Refresh.
- `qml/Main.qml`: all application pages, opening sequence, dialogs and responsive Nexus Command Center.
- `assets/`: official icon, Windows ICO, Neural Sphere and visual assets.
- `tests/test_core.py`: automated safety and function tests.
- `ARLEN_NEXUS.spec`: PyInstaller one-folder Windows application definition.
- `installer/ARLEN-NEXUS.iss`: per-user Inno Setup installer.
- `.github/workflows/windows-installer-v06-verify.yml`: read-only PR Windows verification (content now targets v0.7; filename is historical).
- `.github/workflows/windows-installer-v06.yml`: v0.7 release build/publish workflow (historical filename).
- `updates/`: manifest/staging foundation for verified updates.

## 4. Version record

- v0.1: concept, name, offline-first contract, owner control and modular roadmap.
- v0.2: early QML desktop shell and local command/backend prototype.
- v0.3: 17/17 tests; PIN/profile, safe macros, image foundation, Image-to-PDF and staged verification.
- v0.4: 20/20 tests; Windows CI, update apply/rollback, PDF merge/split and portable packaging. Verified run `32768885259`.
- v0.5: direct single EXE, verified run `32795779576`; first-launch Temp extraction and earlier interface were not acceptable as the long-term delivery.
- v0.6: proper installer and responsive transition; kept as an internal evolution step.
- v0.7: official branding, reference-based Command Center, repaired/generated Sphere asset at 50% saturation, compact right telemetry, battery/charger telemetry, warnings for missing packs, safe System Refresh and 22 tests. Verified run `32809263990`.

## 5. v0.7 feature truth table

| Feature | Status | Notes |
|---|---|---|
| Windows installer/shortcut/app icon | PASS | Supplied ARLEN artwork; same icon used throughout. |
| Installer upgrade path | PASS | Fixed AppId; per-user installation. |
| Opening sequence/sound | PASS | Code-native cinematic screen; selectable 12/7/3 sec; boot tone on/off. |
| Responsive main window | PASS | 1024×768 Windows visual run passed; smaller windows scroll/reflow. |
| Centered animated Neural Sphere | PASS | New valid transparent asset, 50% saturation, slow rotation/pulse. |
| CPU/RAM/disk/uptime | PASS | Real psutil values. |
| Wi-Fi/network throughput/session | PASS | Real local telemetry; connectivity probe. |
| Battery/charger/remaining time | PASS | Real psutil battery data; `N/A` when unavailable. |
| GPU usage | NOT IMPLEMENTED | UI states Not bundled/N/A. |
| System Refresh | PASS | ARLEN-only cleanup/working-set trim; does not kill other apps. |
| English/Bangla/Banglish command mapping | PASS | Supported built-in command vocabulary. |
| Protected power actions | PASS | Confirmation/cancel. |
| Custom safe macros | PASS | Allow-listed; power actions rejected inside macros. |
| Conversational Chat | PARTIAL | UI/wiring works; GGUF model and llama.cpp runtime not bundled. |
| Voice/TTS | NOT IMPLEMENTED | UI/profile foundation only; explicit warning. |
| Image upload/metadata | PASS | Local file picker and metadata. |
| OCR | PARTIAL | Optional pytesseract hook; models/runtime not bundled; warning displayed. |
| Image adjustments/export | PASS | Non-destructive local copy workflow. |
| Advanced generative image editing | NOT IMPLEMENTED | No model/layers/generative fill. |
| Image-to-PDF | PASS | Automated test. |
| PDF merge/split | PASS | Automated test. |
| Advanced PDF editor/OCR | NOT IMPLEMENTED | Future pack. |
| Staged update verification/apply/rollback | PASS FOUNDATION | Local staged flow tested; remote download service is not complete. |
| Trusted code signing | NOT IMPLEMENTED | SmartScreen warning remains possible. |

Status definitions:

- **PASS:** implemented and covered by automated or Windows workflow evidence.
- **PARTIAL:** UI/foundation works, but optional runtime/model or complete live behavior is missing.
- **WINDOWS TEST REQUIRED:** must be manually checked on the owner's real PC/hardware.
- **NOT IMPLEMENTED:** no claim of support; UI must warn clearly.

## 6. v0.7 verified evidence

Workflow run `32809263990`:

- Python compile PASS.
- 22/22 automated tests PASS.
- QML lint PASS.
- PyInstaller bundle PASS.
- Inno Setup compile PASS.
- Silent install PASS.
- Installed EXE remained running after launch wait.
- Clean-dashboard screenshot artifact uploaded.

Still required on the owner's PC:

- Confirm battery/charger changes live on the Dell Latitude 7490.
- Test global `Ctrl+Alt+A`.
- Test restart/shutdown confirmation without accepting destructive action unnecessarily.
- Test shortcut/icon persistence after reboot.
- Test real screen scaling at the owner's Windows DPI.
- Verify opening sound level.
- Test every file dialog with personal sample files.

## 7. System Refresh behavior

Accepted phrases include `system refresh`, `refresh system`, `free arlen ram`, `ram refresh`, Bangla equivalents and the Quick Action button.

It:

1. unloads an active Local Brain;
2. deletes ARLEN-owned temporary image previews;
3. runs Python garbage collection;
4. on Windows, asks the OS to trim ARLEN's own working set;
5. reports measured ARLEN RSS change and cleared preview count.

It does not kill unrelated programs, delete arbitrary Windows Temp files or promise fake RAM improvement.

## 8. Missing capability warnings

When a user attempts unavailable functionality:

- Chat without a GGUF brain: `LOCAL BRAIN NOT INSTALLED`.
- Voice without runtime/models: `VOICE NOT SUPPORTED YET`.
- OCR without pack: `OCR PACK NOT INSTALLED`.

The dialog states what remains available. Future development must keep this honest behavior.

## 9. Release and verification procedure

1. Make changes on a branch/PR.
2. Run source compile, all tests and QML lint.
3. Build the one-folder PyInstaller application.
4. Build the Inno Setup installer.
5. Install silently into a deterministic test directory.
6. Launch the installed EXE and wait at least 22 seconds.
7. Capture and visually inspect the Windows screenshot.
8. Only after all checks, merge to `main`.
9. Publish `ARLEN-NEXUS-Setup-v0.7.exe` and SHA-256 through GitHub Releases.
10. Update README/HANDOVER with the exact run ID, hash and remaining limitations.

Never present a source archive or empty ZIP as the Windows app.

## 10. Next-version priorities

Recommended v0.8 order:

1. Portable Local Brain Pack suitable for 8GB RAM, including llama.cpp runtime and a carefully selected small quantized GGUF model.
2. Real manual DPI/resizing tests on the owner's Dell.
3. Live GPU telemetry provider with honest fallback.
4. Notification/button sound pack with volume control.
5. Offline microphone transcription and TTS pack.
6. Bundled Bangla/English printed OCR, followed by handwriting OCR.
7. Advanced image history/layers and optional background-removal model.
8. Remote signed update manifest/download with owner approval.
9. Trusted Windows code-signing certificate.

Do not begin a capability pack by weakening the stable core or bundling an unlicensed model.

## 11. Continuation rules

- Preserve the supplied icon and centered Sphere identity.
- Keep the visual palette low saturation; status colors are exceptions.
- Keep Sphere central, system/network cards on the right and Command Center below.
- Never fake PC status, network speed, battery or unsupported capabilities.
- Keep source private.
- Preserve all existing tests and add tests for new backend behavior.
- Do not call the project complete merely because the UI button exists.
- Update this file after every verified release.
