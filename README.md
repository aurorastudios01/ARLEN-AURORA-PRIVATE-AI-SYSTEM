# ARLEN NEXUS v1.1

<div align="center">

## Adaptive Responsive Local Executive Neural-Assistant

### Neural Execution and Experience Unified System

**A private offline-first AI workstation for Windows**

</div>

---

# Vision

ARLEN NEXUS is designed to become a personal AI operating companion, not just a chatbot.

It combines:

- Local AI intelligence
- Personal memory
- Document understanding
- Image intelligence
- File assistance
- System utilities
- Futuristic desktop experience

Core philosophy:

```
Ollama          = AI Brain
Python Tools   = AI Hands
SQLite Memory  = Local Memory
Premium UI     = AI Workstation
```

---

# Current Status

## Ready Environment

✅ Python 3.11.9  
✅ Ollama 0.32.15  
✅ Qwen2.5:3B Text Model  
✅ Qwen2.5VL:3B Vision Model  
✅ FFmpeg

Target:

- Offline-first operation
- Low resource usage
- 4GB RAM class PC optimization

---

# V1 Feature Scope

## AI Assistant

- Offline chat
- Local AI reasoning
- Context understanding
- Basic memory
- User preferences

## Smart Setup

ARLEN automatically detects:

- Python
- Ollama
- AI models
- FFmpeg
- Installed applications
- Browsers
- Available tools

---

# Intelligence Modules

## PDF Intelligence

- Read PDF
- Summarize
- Explain documents
- Search text
- Extract information
- Merge/Split pages
- Rotate pages
- Add watermark

## Image Intelligence

- Image analysis
- Smart suggestions
- Sharpness improvement
- Texture enhancement
- Light correction
- Contrast adjustment
- Color correction
- Resize/Crop
- Format conversion
- Background blur suggestion

## Vision System

V1 includes lightweight smart vision capabilities for practical image understanding.

Advanced Vision Pro will be considered after V1 stability.

---

# PC Assistant

ARLEN can help with:

- Open Chrome
- Open Brave
- Open VS Code
- Launch installed applications
- Find files
- Open documents
- Search information through browser

---

# Interface System

Default Theme:

## Aurora AI

Features:

- Animated AI Sphere
- Dynamic background
- Dark glass interface
- Theme switching
- Command Center
- Left Quick Tools panel
- UI sound effects

---

# Version History

| Version | Focus |
|---|---|
| v0.1 | Test Code / Early Beta — foundation |
| v0.2 | Test Code / Early Beta — desktop architecture |
| v0.3 | Test Code / Early Beta — local AI setup |
| v0.4 | Beta Development — tool architecture |
| v0.5 | Beta Development — memory system |
| v0.6 | Beta Development — document intelligence |
| v0.7 | Beta Development — image intelligence |
| v0.8 | Prototype Development — futuristic UI |
| v0.9 | Prototype Development — theme and sound system |
| v1.0 | Prototype Development — workstation interface |
| v1.1 | **First Release** — stable smart local workstation |

---

# Not Included in V1

- Voice assistant
- Whisper/TTS
- Plugin system
- Personal knowledge base
- Messenger automation
- Social automation
- Full PC takeover
- Deep browser automation

Future expansion only after stable V1 release.

---

# Development Roadmap

1. Backend Core
2. Ollama Integration
3. Memory System
4. Tool Manager
5. System Scanner
6. PDF Module
7. Image Module
8. File Assistant
9. Premium UI
10. Windows Installer

---

# Goal

Build a private AI workstation that is:

- Local
- Fast
- Reliable
- Intelligent
- Expandable

**ARLEN NEXUS — Your personal AI workstation.**

---

# V1.1 Development Implementation

The current development branch now includes the first V1.1 foundations:

- Ollama chat adapter for `qwen2.5:3b`
- Ollama vision adapter for `qwen2.5vl:3b`
- bounded SQLite conversation memory
- real environment/model diagnostics
- 4 GB Low Resource mode
- responsive Theme 9 / Aurora AI dashboard based on the owner-approved demo
- centre-out animated core splash; the core image itself does not continuously rotate
- removable custom core/background and Aurora reset
- local calculator, unit converter, notes, screenshot and clipboard foundations
- local file metadata index, real filename search, organization preview, PIN-approved Downloads grouping, undo, Open and Reveal

This is development code, not a released V1.1 installer. The verified v0.7 Release remains available until a V1.x installer passes Windows build, QML lint, screen-size, upgrade and runtime checks.

Detailed UI mapping, responsive breakpoints, historical bugs, fixes, benefits and remaining limitations are consolidated below so this README remains the single project guide.

## Ownership and AI assistance

ARLEN NEXUS was conceived, named, planned, directed, configured and tested by **Jubaer Hossain**. The full product name, logo direction, system structure and setup decisions come from Jubaer's plan. AI-assisted engineering helped implement and document the plan.

> Used correctly, AI makes human work easier, saves time and helps turn a clear plan into a working system while human judgment and ownership remain in control.

---

# V1.1 First Release Guide

## Download for Windows

The permanent verified V1.1 installer link will be placed here immediately after the signed release asset passes installation and launch checks. Development or temporary Actions artifacts are intentionally not linked because those links expire.

## PC requirements

| Profile | Minimum | Recommended |
|---|---|---|
| Operating system | Windows 10 64-bit | Windows 11 64-bit |
| Memory | 4 GB RAM with Low Resource mode | 8 GB or more |
| Free application space | 2 GB | 4 GB |
| Local AI runtime | Ollama installed separately | Current Ollama release |
| Text model | `qwen2.5:3b` | `qwen2.5:3b` |
| Vision model | Optional on 4 GB PCs | `qwen2.5vl:3b` |

The final installer includes the desktop application and its Python/Qt runtime. End users do not need to install Python, VS Code or Git to run ARLEN NEXUS. Ollama and local AI models remain separate because model downloads are large and hardware-dependent.

## First installation

1. Download the V1.1 Setup EXE from the release link above.
2. Open it and complete the per-user installation; administrator access is not normally required.
3. Open ARLEN NEXUS and use AI Setup to check Ollama and the installed models.
4. On a 4 GB PC, keep Low Resource mode enabled and use the text model alone when vision is not needed.

## What V1.1 can do

| Workspace | Working behavior |
|---|---|
| Local Chat | Talks through local Ollama using `qwen2.5:3b`; reports an honest setup error when Ollama/model is missing |
| Local Memory | Saves bounded conversation history and user settings in upgrade-safe SQLite storage |
| Vision | Sends a selected image to `qwen2.5vl:3b` when that optional model is installed |
| Calculator | Safe arithmetic and scientific functions without unrestricted Python `eval` |
| Unit Converter | Local length, weight, temperature and storage conversion |
| Notes | Local UTF-8 Bangla/English note editing and Save As |
| Screenshot | Captures the primary Windows display to a selected local path |
| Clipboard | Reads or replaces the local text clipboard |
| File Search | Searches a bounded metadata index of common user folders and opens/reveals selected results |
| Smart Organization | Previews files directly inside Downloads, requires the owner PIN before moving them into `ARLEN Organized`, and supports one-level undo |
| Image Studio | Non-destructive light, contrast, saturation, sharpness/texture, crop, resize and export-copy foundations |
| PDF Studio | PDF reading and page-tool foundation; the interface must only advertise operations connected to tested handlers |
| System Dashboard | Shows real CPU, RAM, disk, battery, network, environment and AI readiness where available |
| Themes and Core | Ten themes, four core animation styles, custom visual import, remove and Aurora reset |

## Aurora AI interface map

| Control | Interface opened |
|---|---|
| Dashboard | Responsive Aurora home with system overview, animated core, Command Center and AI status |
| Calculator / Scientific | Basic and scientific calculator workspace |
| Unit Converter | Category-based converter |
| PDF Tools | Local PDF workspace |
| Image Tools | Local image analysis and non-destructive editing workspace with examples |
| File Manager | Search, recent files, safe organization preview, apply and undo |
| Note Pad | Local note editor |
| Screenshot | Screen capture workspace |
| Clipboard | Text clipboard workspace |
| System Info | Device, runtime and ownership information |
| Settings | PIN, AI diagnostics, Low Resource mode, themes, custom core remove/reset and update safety |
| Top command field | Unified local chat and recognized safe-command router |

## Responsive screen policy

| Available width | Layout |
|---|---|
| 1450 px or more | Full navigation and three-column Aurora dashboard |
| 1100–1449 px | Narrow navigation and compact three-column dashboard |
| 900–1099 px | Icon navigation and single-column scrolling dashboard |
| Below 900 px | Not supported; the app enforces a 900×680 minimum |

The automated Windows gate renders and checks 1366×768 and 1920×1080 checkpoints. Release review also covers maximized/restored layouts, common Windows scaling, long labels, empty data and error messages.

## Historical problems fixed for V1.1

| Earlier problem | V1.1 correction |
|---|---|
| A model folder could be reported as a ready AI brain | Real Ollama health and `/api/tags` model discovery |
| Home and Chat used separate message state | One SQLite-backed conversation source |
| Chat depended on a manually copied GGUF file | Local Ollama adapter for `qwen2.5:3b` |
| Vision readiness was guessed from folders | Real `qwen2.5vl:3b` discovery and selected-image payload |
| A custom sphere overwrote one cached filename | Unique visual filenames with Remove Custom Core and Reset Aurora |
| The entire sphere rotated continuously | Static core artwork with pulse, orbital rings and centre-out particle splash |
| Common laptop widths clipped the right rail | Responsive allocation and narrow-screen scrolling fallback |
| Voice controls implied an unavailable feature | Voice removed from the first-release scope |
| Chat history disappeared | Bounded WAL-mode SQLite history |
| File Manager was decorative | Real bounded search, Open, Reveal, organization preview, PIN approval and undo |
| Tools could look ready without a connected implementation | Status and errors now report unavailable dependencies honestly |

## Verified release gates

- Python source compilation
- 28 automated backend/service regression tests
- QML syntax validation
- 1366×768 responsive render
- 1920×1080 responsive render
- Windows PyInstaller EXE creation
- executable existence check
- final installer launch and upgrade test before the Release link is published

## Safety and privacy

- Chat, memory, notes and metadata stay local unless the owner explicitly opens an external service.
- File discovery records filenames, paths, types, sizes and modified times; it does not silently upload file contents.
- Smart organization never auto-deletes files and does not move anything before preview plus owner PIN approval.
- User data is stored under `%LOCALAPPDATA%\ARLEN NEXUS\UserData` and is preserved across application upgrades.
- Missing model, GPU telemetry or tool support is shown as unavailable; ARLEN does not invent readiness or sensor values.

## First-release limitations

- Voice, Whisper and TTS are not included in V1.1.
- Ollama and the Qwen models are separate installations.
- Image prompt editing maps supported words to deterministic local filters; it is not a generative image model.
- GPU temperature is omitted when a reliable provider is unavailable.
- Full PC takeover, mouse/keyboard automation, background monitoring, social automation and silent deletion remain disabled.

## Source structure

- `main.py` — Qt startup, bundled UI font and automated screenshot capture.
- `backend.py` — settings, commands, telemetry, migrations and tool routing.
- `v1_services.py` — SQLite, Ollama, discovery and local launching services.
- `qml/Main.qml` — responsive Aurora AI interface and animations.
- `tests/` — core, safety and service regression tests.
- `ARLEN_NEXUS.spec` — Windows portable application build.
- `installer/ARLEN-NEXUS.iss` — fixed-AppId per-user installer definition.
- `.github/workflows/v1-development-verify.yml` — Windows validation and build gate.

The active repository keeps only current V1.1 source, tests, assets, installer/build definitions, this README and the single verification workflow. Historical code remains available through Git history, not as duplicate active files.

## Bundled font notice

ARLEN NEXUS bundles DejaVu Sans for reliable English UI rendering on minimal Windows installations. DejaVu fonts are distributed under their permissive license; see the DejaVu project license terms included in the upstream font package.
