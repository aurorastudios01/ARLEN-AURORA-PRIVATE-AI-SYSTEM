# ARLEN NEXUS — V1 Continuation Handover

Last updated: 25 August 2026  
Repository: `arlenray0113-cyber/ARLEN-NEXUS-PRIVATE` (private)  
Owner, concept and direction: Jubaer Hossain

## Product state

The latest verified application remains **v0.7**. Main is a V1 development line and must not be described as a released v1.0/v1.1 until Windows validation and a V1 installer exist.

Keep the existing v0.7 GitHub release unchanged during development. After a verified V1.x release is published, remove the v0.7 Release entry as requested by the owner. Do not delete or rewrite Git history.

## Locked V1 decisions

- Support 4 GB Windows PCs through a Low Resource mode; 8 GB is recommended.
- Local AI runtime: Ollama with `qwen2.5:3b` for the stable conversational baseline.
- Local memory: SQLite.
- Keep Python tool modules and FFmpeg.
- No voice assistant, Whisper or TTS in V1.
- Input: Bangla, Banglish and English. Reply: Bangla or English.
- Image tools remain local, non-destructive and do not introduce an automatic adult-content blocker.
- Default UI: Aurora AI, animated core, dynamic background, UI sounds, left Quick Tools and ten selectable themes.
- Owner should only download/install; final setup must not require coding or terminal work.

## Stable architecture

- `main.py`: Qt application startup and official icon.
- `backend.py`: settings, commands, telemetry, tool routing, image/PDF functions and migrations.
- `qml/Main.qml`: application UI and animations.
- `tests/test_core.py`: backend and safety regression tests.
- `ARLEN_NEXUS.spec`: PyInstaller one-folder definition.
- `installer/ARLEN-NEXUS.iss`: fixed-AppId per-user installer.
- `%LOCALAPPDATA%\ARLEN NEXUS\UserData`: upgrade-safe PIN, settings, SQLite memory, history, visuals and automations.
- Ollama: separate local process discovered/managed by the setup and application; do not embed model files in Git.

## Development order

1. Consolidate backend contracts and migration.
2. Add Ollama health/model discovery and `qwen2.5:3b` chat adapter.
3. Add SQLite memory with bounded context and user controls.
4. Build permissioned tool manager and app/file discovery.
5. Finish real image/PDF/file tools.
6. Rebuild responsive Aurora AI interface and Low Resource animation mode.
7. Build first-run setup and runtime/model diagnostics.
8. Test on 4 GB and 8 GB profiles.
9. Build, install, upgrade, visually inspect and publish V1.x.

## V1.1 development checkpoint — 25 August 2026

- Added dependency-free Ollama service adapter for text and selected-image vision.
- Added bounded SQLite/WAL conversation memory and recent local files.
- Added truthful environment/model/FFmpeg/browser diagnostics.
- Added 4 GB Lite and 8 GB+ runtime profiles.
- Reworked QML toward the owner-approved Theme 9 / Aurora AI demo.
- Quick Tools, System Overview, centre core, Command Center and right AI status follow the approved zoning.
- Added centre-out particles; do not restore whole-image continuous rotation.
- Added custom visual remove/reset, ten themes and four core animation modes.
- Added calculator, converter, note, screenshot, clipboard and functional file-search foundations.
- Added metadata-only user-folder indexing and a constrained Downloads organizer: preview, owner PIN, category folders and one-level undo; never move/delete silently.
- Added `V1.1-IMPLEMENTATION.md` as the UI, responsive, bug/fix and limitation record.
- Still required: Windows QML lint, rendered multi-resolution screenshots, full core regression tests, installer/upgrade checks and remaining PDF/UI completion.

## Truth rules

- A UI button is not proof that a feature works.
- Missing Ollama/model/FFmpeg/tool state must be reported clearly.
- Do not fake CPU, RAM, network, battery or completion results.
- Do not claim generative editing when an operation is a deterministic local filter.
- Never overwrite UserData during application upgrades.
- Destructive PC actions require confirmation; owner policy controls powerful actions.

## Repository cleanup policy

The active tree keeps only the current source, tests, assets, V1 docs, package definition, installer definition and one verification workflow. Old one-file/portable scripts, duplicate preview files and obsolete release workflows are removed from the active tree because Git history already preserves them.

## Release policy

Development CI is verification-only. It must not overwrite the v0.7 release. A V1 publishing workflow is added only when the version, installer names and release notes are final and all gates are green.
