# ARLEN NEXUS v0.7

**ARLEN:** Adaptive Responsive Local Executive Neural-Assistant  
**NEXUS:** Neural Execution and Experience Unified System  
**Owner / concept / direction:** Jubaer Hossain  
**Product line:** Built for Jubaer Hossain — Controlled by its owner.

ARLEN NEXUS is a private, offline-first Windows desktop intelligence, system-control and creator environment. The source remains private; end users receive a normal Windows installer and do not need Python, an editor, Node, Visual Studio, Rust, Ollama or a separate llama.cpp installation.

## Download

After the v0.7 release workflow publishes:

- [Direct v0.7 installer](https://github.com/arlenray0113-cyber/ARLEN-NEXUS-PRIVATE/releases/download/v0.7/ARLEN-NEXUS-Setup-v0.7.exe)
- [v0.7 release page](https://github.com/arlenray0113-cyber/ARLEN-NEXUS-PRIVATE/releases/tag/v0.7)

The installer uses a fixed AppId and installs per-user under `%LOCALAPPDATA%\Programs\ARLEN NEXUS`. Later installers upgrade the same installation. Owner settings and PIN data live separately under `%LOCALAPPDATA%\ARLEN NEXUS\UserData` and are not removed by normal app upgrades.

## v0.1–v0.7 history

| Version | Milestone | Evidence/status |
|---|---|---|
| v0.1 | Initial offline-first ARLEN concept, identity, security and modular capability plan. | Planning/prototype; no final Windows evidence. |
| v0.2 | Early PySide/QML desktop shell and backend command foundation. | Prototype; not released as production. |
| v0.3 | Owner PIN/profile, macro safety, image foundation, Image-to-PDF, policy locks and staged checksum verification. | 17/17 automated tests and QML lint passed; multiple Windows/live capabilities remained incomplete. |
| v0.4 | GitHub Windows CI, staged update apply/rollback, PDF merge/split and portable packaging. | Run `32768885259`: 20/20 tests, lint, build and launch PASS. |
| v0.5 | Direct single-file EXE experiment. | Run `32795779576`: 20/20 tests, lint, one-file build and 30-second launch PASS. Slow first launch and Temp extraction made it non-ideal. |
| v0.6 | Installer and responsive-interface transition. | Installer/install/launch verification passed; retained as an internal transition, not the desired final interface. |
| v0.7 | Branded installer, supplied ARLEN icon, reference-based Nexus Command Center, centered animated Sphere, compact real telemetry, battery/charger state, capability warnings and safe System Refresh. | Run `32809263990`: 22/22 tests, QML lint, Windows bundle, installer, silent install, installed launch and visual artifact PASS. |

## v0.7 interface and identity

- Official supplied ARLEN NEXUS icon on EXE, installer, shortcut, taskbar and application window.
- Low-saturation black/cyan visual system.
- Centered transparent animated Neural Sphere with slow rotation and breathing pulse.
- Two-line sidebar navigation.
- Nexus Command Center conversation panel.
- Compact System Overview, Network Status and Quick Actions.
- Responsive layout: full side-by-side command center at 1024px and larger; vertical scrolling/reflow for smaller windows.
- Cinematic opening sequence with ARLEN/NEXUS expanded names and configurable 12/7/3-second duration.
- Opening boot sound with on/off control.

## Real built-in capabilities

### PASS / included

- Owner PIN, owner profile and protected actions.
- CPU, RAM, disk, uptime, Wi-Fi, live download/upload and session network usage.
- Battery percentage, charging/discharging, charger connected/removed and remaining-time telemetry when Windows exposes a battery.
- Open Brave, Notepad, Calculator, Paint, Explorer, Task Manager and common folders.
- Confirmation-gated restart, shutdown and cleanup.
- Safe System Refresh: unloads Local Brain if loaded, clears ARLEN preview cache, performs garbage collection and trims ARLEN's own Windows working set. It does not terminate unrelated applications or claim fake RAM gains.
- Custom command builder with allow-listed actions.
- Non-destructive Image Studio preview/export: brightness, contrast, saturation, sharpness, dehaze, crop ratios, rotate, mirror and grayscale.
- Local image metadata reading.
- Image-to-PDF, ordered PDF merge, PDF split and open in Windows default viewer.
- Staged update checksum/path protection, owner-PIN apply, backup and rollback foundation.
- Themes, owner visuals, custom Sphere/background import and UserData backup.

### PARTIAL / optional pack required

- Conversational Chat UI is functional, but private AI conversation requires a compatible GGUF Local Brain Pack and llama.cpp runtime.
- Vision reads image metadata; OCR text recognition requires an offline OCR pack.
- Voice UI and wake-word normalization exist; real microphone transcription and TTS require an offline Voice Pack.
- GPU card reports `N/A / Not bundled` because live GPU-usage telemetry is not bundled.

### NOT INCLUDED

- Bundled GGUF language model.
- Bundled llama.cpp runtime.
- Real multilingual microphone transcription/TTS.
- Bangla/English printed or handwriting OCR models.
- Advanced layer-based image editor, generative fill or background removal model.
- Trusted Windows code-signing certificate.
- Automatic cloud AI or silent personal-data upload.

Missing capability clicks display an explicit warning instead of pretending the feature is active.

## Security and privacy contract

1. Core functions remain offline-first.
2. Public search is Brave-first and owner-policy controlled.
3. Personal uploads remain disabled by default.
4. Local images are not automatically blocked, blurred, deleted or uploaded.
5. Protected/destructive actions require confirmation or owner PIN.
6. UserData must survive app upgrades.
7. Unverified or unbundled functions must never be documented as complete.

## Verified v0.7 gates

Read-only verification workflow run: `32809263990`

- Python compilation: **PASS**
- Automated core tests: **22/22 PASS**
- QML lint: **PASS**
- PyInstaller Windows bundle: **PASS**
- Inno Setup installer: **PASS**
- Silent installation: **PASS**
- Installed application launch: **PASS**
- Windows visual screenshot artifact: **PASS**

See [HANDOVER.md](HANDOVER.md) for architecture, continuation instructions, test classifications, known limitations and next-version plan.
