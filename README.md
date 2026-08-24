# ARLEN NEXUS V0.4 — Evolution Core Development Build

ARLEN NEXUS is an offline-first Personal Intelligence & System Control Environment.

**Concept, Direction & Ownership: Jubaer Hossain**

## Included in this build

- Premium frameless multi-page QML interface
- 12/7/3-second animated opening modes
- Opening circuit visual and animated neural sphere
- Obsidian, Crimson, Emerald, Violet, and Arctic themes
- Live CPU, RAM, disk, Wi-Fi, download, upload, session usage, and process data
- Brave-first application and web search controls
- Ctrl+Alt+A global access shortcut on Windows
- Hidden-terminal launcher
- Home, Chat, Voice, System, Network, Files, Automation, Cleanup, Security, Admin, Image Studio, Vision/OCR, PDF Studio, Theme Studio, and About pages
- First-run owner PIN instead of a default password
- PIN-protected editable owner name, call name, title and welcome message
- Owner data stored separately from application files on Windows so updates preserve identity
- Owner-data backup foundation
- Bangla/Banglish/English voice-command interpretation layer and editable wake word
- PIN-protected Command Builder with allow-listed macro execution
- Capability Pack status for Local Brain, Voice, Vision/OCR, Image and PDF
- Incremental update manifest foundation with preserved user-data boundary
- Owner-PIN update apply and one-step rollback with verified staged files
- Local command engine with confirmation for power and cleanup actions
- Local conversational model integration through an optional GGUF model
- Prompt-based image editing for crop ratios, dehaze, texture/detail, brightness, saturation, rotation, mirroring, and grayscale
- Manual image adjustments and non-destructive preview/export foundation
- Unrestricted local-image policy: no content blocking, automatic blur, deletion, or upload
- Local image inspection and optional Bangla/English OCR-pack integration
- PDF Studio core with Image-to-PDF, merge, split and default/PDFgear access
- Smart Auto public-search policy with no personal uploads

## Portable release policy

The owner will not be asked to install an editor, IDE, compiler, Node, Rust, Visual Studio, or Ollama. The production Windows release is designed as a self-contained portable folder. Optional Local Brain, Voice and OCR models are copied into their pack folders; they are not installed system-wide.

## Developer/source launch

1. Developers may run `setup_windows.bat` to prepare a source environment. End users should use the final portable release instead.
2. Double-click `RUN_ARLEN_SILENT.vbs`.
3. Choose a 12, 7, or 3-second opening mode.
4. Create your own 4–12 digit owner PIN.

Use `run_debug.bat` only when an error must be captured. It intentionally shows a terminal.

## Offline behavior

The core interface, commands, monitoring, files, cleanup, image tools, settings, logs, and installed model run locally. Smart Auto web search opens Brave only when an online information request is made. Uploads remain disabled by default.

## Conversational Brain

Put a compatible small `.gguf` model in `models`, then install `requirements-ai.txt`. The model stays on the PC. Use **Unload Brain** to release its RAM.

## Development status

This is an active development tree, not yet a released ZIP and not yet the final signed Windows portable EXE. Do not treat source files as an end-user build. A release is permitted only after a real `ARLEN NEXUS.exe` launches in a clean Windows environment without editor or development-tool installation.
