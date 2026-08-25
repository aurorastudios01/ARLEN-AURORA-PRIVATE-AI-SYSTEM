# ARLEN NEXUS v0.8 Core Reprogram

**ARLEN:** Adaptive Responsive Local Executive Neural-Assistant  
**NEXUS:** Neural Execution and Experience Unified System  
**Owner, concept and direction:** Jubaer Hossain

ARLEN NEXUS is a private, local-first Windows desktop command center. v0.8 is a core reprogram focused on truthful capability status, reliable commands and automations, visible image/PDF workspaces, upgrade-safe owner data and a new animated identity based on the supplied luminous network sphere and official ARLEN NEXUS logo.

> v0.8 is under validation. Do not call it a release until the Windows test workflow passes compilation, tests, QML lint, installer build, silent install, installed launch and screenshots. The last verified public build is v0.7.

## Download

- [Latest verified release](https://github.com/arlenray0113-cyber/ARLEN-NEXUS-PRIVATE/releases/latest)
- Planned v0.8 installer: `ARLEN-NEXUS-Setup-v0.8.exe`

The installer is per-user and uses the existing fixed AppId. Application files go to `%LOCALAPPDATA%\Programs\ARLEN NEXUS`; settings, PIN, visual imports, history and automations remain under `%LOCALAPPDATA%\ARLEN NEXUS\UserData`, outside the replaceable app directory.

## v0.8 goals and implemented core changes

- Supplied luminous sphere is the default identity; supplied logo is used for app, EXE and installer branding.
- Six animation profiles: Luminous Core, Particle Bloom, Quantum Halo, Neural Pulse, Aurora Mesh and Minimal Core. The design uses core-origin pulse/ring/particle motion instead of simply rotating the whole image.
- Custom sphere/background import now verifies the image, creates a unique cached copy and supports remove/reset.
- One persistent conversation replaces duplicate Home/Chat models and routes each input once.
- Chat looks for a valid GGUF model in a capability-pack directory and reports the missing runtime/model honestly.
- Custom commands have stable IDs, validation, update, enable/disable, run and PIN-protected delete.
- In-app Daily/Once schedules run only while ARLEN is open; no Windows service is falsely claimed.
- Failed macro actions no longer produce fake success.
- Image Reader exposes the selected image and local metadata/OCR status.
- Image Studio supports non-destructive local presets such as 9:16 Portrait, Square Social, Clear & Dehaze, Vibrant, Documentary B&W, Mirror, Warm Portrait and Cool Editorial.
- PDF Studio backend can inspect documents, render a selected page and export pages as PNG through PyMuPDF.
- Owner backup v2 includes settings, commands, schedules and conversation history.
- Safe System Refresh clears both legacy and v0.8 preview caches and only trims ARLEN-owned memory.
- Installer/version metadata moved to 0.8.0; UserData migration remains compatible.

## Capability truth table

| Capability | v0.8 Core status | Requirement/limit |
|---|---|---|
| Windows app/installer/upgrade path | Implemented; Windows CI validation required | End user installs one Setup EXE |
| System telemetry and safe commands | Implemented | Windows/psutil |
| Animated core profiles and custom visuals | Implemented in v0.8 source; visual CI required | GPU-accelerated Qt Quick |
| Local image metadata/edit presets/export | Implemented | Deterministic Pillow editing, not generative AI |
| PDF inspect/page render/export | Implemented | PyMuPDF is bundled in the installer |
| Custom command CRUD/test/run | Implemented | Allow-listed actions; protected actions rejected |
| Daily/Once scheduling | Implemented in-app | ARLEN must remain open |
| Conversational chat | Optional pack | Compatible GGUF + bundled llama-cpp runtime required |
| Voice microphone/STT/TTS | Not bundled | Verified offline Voice Pack required |
| Bangla/English OCR | Optional hook | OCR runtime/language data required |
| GPU utilization telemetry | Not bundled | UI must show N/A, not invented data |
| Generative fill/background removal/layers | Not implemented | Future Image Pack |
| Trusted Windows signing | Not included | SmartScreen may warn |

## Development and installation

End users do **not** need Python, VS Code, Git, Visual Studio, Node, Rust, Ollama or llama.cpp. GitHub Actions produces the Windows installer with dependencies included.

For contributors, use Python 3.12 and install `requirements.txt`, `pytest` and `pyinstaller`. Visual Studio Build Tools are needed only when compiling native optional runtimes such as llama-cpp; they are not required to run the packaged Core application.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pytest pyinstaller
python -m pytest -q
python -m PyInstaller --noconfirm --clean ARLEN_NEXUS.spec
```

## Security and privacy contract

1. Local files are not uploaded silently.
2. Public web search is owner-policy controlled and opens Brave.
3. Restart/shutdown require explicit confirmation; owner settings and deletion require PIN where applicable.
4. Automation accepts only allow-listed applications, folders and web links.
5. UserData survives application replacement and normal upgrades.
6. Missing packs are shown as missing; a folder alone is not proof that a capability works.
7. Source remains private; users receive a signed or hashed installer artifact.

## Documentation

- [Complete version history and bug audit](docs/VERSION-HISTORY-AND-BUG-AUDIT.md)
- [Technical handover](HANDOVER.md)

