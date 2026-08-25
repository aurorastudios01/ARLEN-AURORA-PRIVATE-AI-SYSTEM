# ARLEN NEXUS v0.5 — Project Handover & Continuation Memory

**Owner / Concept / Direction:** Jubaer Hossain  
**ARLEN:** Adaptive Responsive Local Executive Neural-Assistant  
**NEXUS:** Neural Execution and Experience Unified System  
**Product line:** Built for Jubaer Hossain — Controlled by its owner.  
**Private repository:** `arlenray0113-cyber/ARLEN-NEXUS-PRIVATE`

## 1. Product purpose

ARLEN NEXUS is a private, offline-first Windows desktop intelligence and system-control environment. It combines a premium cinematic interface, local commands, system monitoring, automation, image tools, Vision/OCR and PDF tools. The owner always retains final authority.

## 2. Non-negotiable requirements

1. The end user must not install Python, an editor, Visual Studio, Node, Rust, Ollama or other development dependencies.
2. The Windows delivery must be portable and directly runnable.
3. Core functionality works offline.
4. Public online search uses Brave and remains controlled by owner policy.
5. Personal uploads, login/account actions, messages, purchases, protected changes and destructive operations require explicit approval.
6. Local images must never be automatically blocked, blurred, deleted or uploaded. Originals remain unchanged by default.
7. Personal data must remain under `%LOCALAPPDATA%/ARLEN NEXUS/UserData` and survive application updates.
8. UI must remain premium, serious and cinematic, with features separated into dedicated pages.
9. Never claim an untested or unbundled capability is complete.
10. Do not label a build final production until the clean-Windows manual checklist passes.

## 3. Direct v0.5 single-EXE release

Download:

[ARLEN-NEXUS-v0.5.exe](https://github.com/arlenray0113-cyber/ARLEN-NEXUS-PRIVATE/releases/download/v0.5/ARLEN-NEXUS-v0.5.exe)

- File type: Direct Windows EXE; no ZIP extraction.
- Approximate size: 266 MB.
- SHA-256: `56060957473bade2997246260d6663c4dd39e72c23ade7d0882bb188ac08ecd2`
- Release page: https://github.com/arlenray0113-cyber/ARLEN-NEXUS-PRIVATE/releases/tag/v0.5
- No developer installation is required.
- First launch may take longer because the single EXE extracts its private bundled runtime into Windows Temp.

## 4. Verified v0.5 gates

Read-only Windows verification workflow run: `32795779576`

- Python source compilation: **PASS**
- Automated core tests: **20/20 PASS**
- QML lint: **PASS**
- PyInstaller single-file EXE build: **PASS**
- Windows single-EXE launch smoke test: **PASS (30 seconds)**

## 5. Built-in core features

### Interface and identity

- Frameless premium multi-page QML interface.
- Cinematic opening sequence with configurable 12, 7 or 3-second duration.
- Opening sound and mute control.
- Obsidian, Crimson, Emerald, Violet and Arctic themes.
- Animated Neural Sphere states.
- Editable owner photo, background, sphere, name, call-name, title and welcome message.
- Windows global shortcut target: `Ctrl+Alt+A`.

### Security and owner control

- First-run 4–12 digit owner PIN.
- Permission Level 1 safe actions, Level 2 confirmation and Level 3 owner PIN.
- PIN-protected owner profile, custom commands, updates and rollback.
- Activity logging and owner-data backup.
- Protected/destructive actions cannot be hidden in safe macros.

### Commands and system control

- English, Bangla and Banglish command normalization.
- Open Brave, Notepad, Calculator, Paint, Explorer, Task Manager and common folders.
- Custom Command Builder with allow-listed actions.
- Restart and shutdown confirmation with cancel support.
- CPU, RAM, disk, uptime, Wi-Fi, network speed, session usage and top-memory processes.
- Safe ARLEN memory cleanup without fake or destructive RAM-cleaner behavior.

### Chat and internet

- Command Engine and Conversational Brain are separate.
- Optional local GGUF provider hook.
- Brain can be unloaded to release RAM.
- Brave-first Smart Auto public search.
- Admin policy can disable public search.
- Personal uploads remain disabled by default.

### Image Studio

- Non-destructive preview and copy export.
- Brightness, contrast, saturation, sharpness/detail and dehaze.
- Prompt controls for 1:1, 9:16 and 16:9 crop, rotation, mirror and grayscale.
- Original-image preservation.
- No automatic adult/nude-content blocking, deletion, blur or upload.

### Vision/OCR foundation

- Local image format, dimensions and color information.
- Optional local OCR provider hook for Bangla/English.
- No cloud upload requirement.

### PDF Studio

- Image-to-PDF.
- Ordered PDF merge.
- PDF page split.
- Open PDF through the Windows default viewer.

### Safe updater

- Staged-file SHA-256 verification.
- Absolute path, traversal, updater-path and UserData-path protection.
- Owner-PIN update apply.
- Versioned backup and one-step rollback.
- Personal UserData preservation.

## 6. Capability-pack architecture

The stable core must remain usable when an optional pack is absent. Packs are portable folders, not system-wide installations, and should load/unload independently for RAM control.

- Local Brain Pack
- Voice Pack
- Vision/OCR Pack
- Image Pack
- PDF Pack
- Theme/Sphere Pack

## 7. Truthful remaining work

The following are not bundled or not fully complete in v0.5:

- Multilingual GGUF Local Brain model/runtime.
- Real microphone capture and local multilingual transcription.
- Local multilingual TTS voices/runtime.
- Bangla/English printed and handwriting OCR models/runtime.
- Advanced PDF operations beyond Image-to-PDF, merge and split.
- Advanced Image Studio layers, timeline/history and selective editing.
- Trusted Windows code signing.
- Full manual validation on a clean Windows 11 personal account.

Windows SmartScreen may warn because the EXE is not code-signed. This does not replace the requirement for future trusted signing.

## 8. Continuation instructions

Any future coding assistant or developer must:

1. Read this entire handover before changing the project.
2. Preserve every non-negotiable privacy, safety and owner-control requirement.
3. Continue unfinished capability packs without breaking the verified offline core.
4. Run Python compilation, all automated tests, QML lint, Windows EXE build and launch verification after meaningful changes.
5. Update this README with new evidence, hashes, workflow run IDs and remaining limitations.
6. Never call unbundled or untested functions complete.
7. Keep source private and publish end-user binaries through GitHub Releases, not as source ZIPs presented as the app.

## 9. Repository release policy

The private source repository remains the authoritative continuation point. Old ZIP artifacts may expire or be removed, but source history must remain so future fixes and upgrades are possible. The GitHub Release should present the direct EXE and checksum evidence for the owner.
