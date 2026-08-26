# ARLEN AURORA

## Adaptive Responsive Local Executive Neural-Assistant
### Autonomous Unified Reasoning & Orchestration Responsive Architecture

> **ARLEN AURORA** is the next-generation evolution of the Arlen Nexus concept: a unified, offline-first personal AI operating environment designed to understand natural language, plan tasks, use internal tools, operate the PC with explicit authorization, process documents and images, research online when connected, and provide a coherent JARVIS-style desktop experience.

---

## Vision

Aurora is not intended to be a collection of disconnected utilities. The goal is one intelligent desktop environment in which the user can express an intent and Aurora selects the appropriate engine, executes the workflow, verifies the result, and reports what happened.

Example:

> "ei PDF ta pore amar college exam er notes banao, tarpor PDF kore save koro."

Aurora should be able to understand the Banglish request, read the supplied document, create structured notes, export them, verify the output, and explain the result in Bangla.

---

## Five Functional Cores

### 01 — AURA
Reasoning, conversation, planning, calculations, mathematics, problem solving, writing, explanations, memory and personal assistance.

### 02 — VISION
Image understanding, OCR, screenshot understanding, visual analysis and vision-assisted workflows.

### 03 — NEXUS
PC, files, folders, applications, settings, safe automation and task execution.

### 04 — ORBIT
Internet search, research, current information, weather, news and source-aware online intelligence.

### 05 — PULSE
CPU, RAM, storage, battery, network, processes, diagnostics, performance and resource management.

The cores are functional subsystems, not merely visual animations.

---

## Unified Aurora Dashboard

The main experience is centered around:

- ARLEN AURORA identity and status
- Aurora Core visualization
- Universal command/input bar
- Universal `+` uploader
- Voice input entry point
- System telemetry
- Running tasks
- Battery status
- Network status
- AI/core status
- Theme controls
- Quick access to every major studio

### Universal `+` Input

The `+` button is a global input/import entry point. It can accept supported:

- Images
- PDFs
- Documents
- Files
- Folders
- Screenshots
- Audio
- Video
- URLs
- Clipboard content

Drag-and-drop should also be supported. Context determines the most useful actions.

---

## Core Studios

### Image Studio

A unified professional image workspace inspired by the workflow of modern photo editors and canvas/design tools.

Planned capabilities:

- Crop, free crop and multi-crop
- Rotate, flip and perspective correction
- Resize and canvas control
- Exposure, brightness and contrast
- Highlights and shadows
- Whites and blacks
- Temperature and tint
- Saturation and vibrance
- Curves and HSL
- Color grading
- Blur, sharpen and denoise
- Dehaze, vignette and grain
- Masks and selective editing
- Layers and non-destructive history
- Background removal/replacement where supported
- Object cleanup/removal where supported
- Upscaling and restoration where supported
- Text, fonts, shapes, stickers and design elements
- Stroke, shadow, gradients and alignment
- Templates and presets
- Before/after comparison
- Batch processing
- Natural-language editing commands

Aurora should translate requests such as `image ta professional kore dao` into an appropriate editing workflow rather than forcing the user to operate every control manually.

### PDF Studio

A complete document workspace built around local files and AI-assisted document understanding.

Planned capabilities:

- Read and preview
- Page thumbnails and navigation
- Merge and split
- Page reorder and rotation
- Compression
- Extract pages/images/text
- Image to PDF
- PDF to image
- OCR for supported documents
- Annotations, highlights and comments
- Text editing where technically supported
- Rewrite and translation
- Summarization
- Document Q&A
- Structured extraction
- Study-note generation
- Export and verification

### Study Center

A dedicated academic workspace.

Input can be a PDF, document, image, notes or local study material.

Outputs can include:

- Detailed notes
- Short notes
- Chapter summaries
- Definitions
- Formulas
- Worked explanations
- Important questions
- MCQs
- Question/answer sets
- Flashcards
- Revision sheets
- Exam-focused summaries

Banglish input should be understood and Bangla output should be available by default when requested.

### File Commander

An AI layer over the local filesystem.

Planned capabilities:

- Browse and search
- Natural-language file discovery
- Rename and batch rename
- Copy/move/delete with safety controls
- Folder creation
- File categorization
- Duplicate detection
- Storage analysis
- Smart organization proposals
- Batch organization
- Undo/rollback journal
- Verification after file operations

Example: `sob PDF alada folder e organize koro`.

### System Center

A local control and diagnostics center exposing safe system information and supported controls.

Dashboard telemetry includes:

- CPU
- RAM
- Storage
- Temporary/storage pressure
- Battery
- Network
- Processes
- System information
- Task status

Aurora should diagnose before applying optimization and should distinguish safe actions from potentially destructive operations.

---

## Agent Architecture

Aurora is designed around an orchestrated execution loop:

```text
User Intent
    ↓
Understand
    ↓
Plan
    ↓
Select Core / Tool / Agent
    ↓
Check Permissions
    ↓
Execute
    ↓
Verify
    ↓
Recover / Retry if appropriate
    ↓
Remember useful context
    ↓
Report in natural language
```

### Mission Mode

High-level requests can become multi-step missions.

```text
MISSION
├── Goal
├── Plan
├── Steps
├── Permissions
├── Execution
├── Verification
├── Retry / Recovery
├── Rollback when available
└── Final Report
```

The system should never claim a task succeeded merely because an action was attempted. It should verify the resulting state whenever technically possible.

---

## Vision and Screen Agent

Where supported and authorized, Aurora can use visual context to understand:

- Screenshots
- Application windows
- UI states
- Visible errors
- Document/image content

The intended workflow is:

```text
Observe → Understand → Plan → Act → Verify
```

Application interaction must respect OS permissions, application constraints and user authorization.

---

## Online + Offline Architecture

Aurora is designed to remain useful without an internet connection.

### Offline-capable layer

Local functionality should include as much as the machine can realistically support:

- Local conversation/reasoning
- Local file management
- Local document processing
- Local PDF operations
- Local image processing
- Local calculations
- Local notes/study processing over available files
- Local system monitoring
- Local automation supported by the OS and application environment

### Online layer

When connected, Aurora can use online capabilities for:

- Web search
- Research
- Current news
- Weather
- Fresh public information
- Online sources
- Cloud intelligence where configured

Online-only information must not be presented as current when the system is offline.

---

## Resource-Aware Design

The primary target environment includes low-resource Windows machines, including approximately 6 GB RAM.

Aurora therefore uses a resource-aware lifecycle:

```text
Idle
 ↓
Core services only
 ↓
Load required engine
 ↓
Execute task
 ↓
Verify result
 ↓
Release unused resources
```

Heavy engines should not remain resident unnecessarily. Text, vision, image AI and other resource-intensive components should be loaded according to the active task and hardware capability.

Adaptive quality, throttling, caching and memory-pressure handling are part of the architecture.

---

## Single-EXE Product Goal

The user-facing product target is:

```text
ArlenAurora.exe
```

The internal architecture may remain modular, but the end-user experience should not require separately installing the project's individual runtime modules.

The final packaging target is a self-contained Windows application as far as technically and legally feasible.

Important engineering constraint: truly embedded local AI models and heavyweight AI engines can be very large and memory intensive. The project must distinguish between a self-contained executable and external model/runtime dependencies, and optimize accordingly rather than pretending those constraints do not exist.

---

## Ten Aurora Themes

1. Aurora — cyan/purple futuristic
2. Obsidian — black premium
3. Nebula — deep violet
4. Arctic — clean ice blue
5. Emerald — green futuristic
6. Crimson — red/black cinematic
7. Solar — gold/orange
8. Cyber — neon cyberpunk
9. Minimal — clean professional
10. Midnight — cinematic dark

Theme customization should cover more than background color:

- Accent colors
- Surfaces/cards
- Gradients
- Glow
- Typography
- Icons
- Core visualization
- Animations
- Wallpapers/backgrounds

---

## Identity

Product identity:

**ARLEN AURORA**

Primary expansion:

**Adaptive Responsive Local Executive Neural-Assistant**

Architecture expansion:

**Autonomous Unified Reasoning & Orchestration Responsive Architecture**

Branding should include a dedicated logo, iconography, typography, startup sequence, Aurora Core visual language and consistent application identity.

---

## Reliability and Safety by Design

Aurora is intended to be powerful without silently performing irreversible operations.

Required engineering principles:

- Explicit permission boundaries
- Safe defaults
- Confirmation for destructive/high-impact operations
- Operation history
- Undo/rollback where feasible
- Verification after execution
- Clear errors
- No fabricated success states
- User-visible task status
- Local privacy by default
- Configurable memory
- Ability to disable capabilities

Powerful automation should operate only within the user's authorized environment and applicable platform/application permissions.

---

## Engineering Principles

1. **One identity, many engines.**
2. **AI chooses tools; tools perform deterministic work.**
3. **Every meaningful action has a verification path.**
4. **Offline functionality remains useful.**
5. **Online intelligence is clearly distinguished from local knowledge.**
6. **6 GB RAM is a first-class optimization target.**
7. **Heavy modules are loaded on demand.**
8. **UI remains responsive during long tasks.**
9. **Features are modular internally but unified to the user.**
10. **The system must report limitations honestly.**

---

## Planned Architecture

```text
ARLEN AURORA
│
├── Aurora UI
│   ├── Dashboard
│   ├── Image Studio
│   ├── PDF Studio
│   ├── Study Center
│   ├── File Commander
│   ├── Research Center
│   ├── System Center
│   ├── Settings
│   └── Theme Engine
│
├── Aurora Core
│   ├── Intent Understanding
│   ├── Planner
│   ├── Tool Router
│   ├── Permission Manager
│   ├── Mission Manager
│   ├── Verifier
│   ├── Recovery Manager
│   └── Memory
│
├── Engines
│   ├── AI
│   ├── Vision
│   ├── Image
│   ├── PDF
│   ├── OCR
│   ├── Files
│   ├── Study
│   ├── Browser / Research
│   └── System
│
├── Agents
│   ├── File Agent
│   ├── Screen Agent
│   ├── Research Agent
│   └── Mission Agent
│
└── Runtime
    ├── Resource Manager
    ├── Model Lifecycle Manager
    ├── Logging
    ├── Updates
    └── Packaging
```

---

## Development Roadmap

### Phase 1 — Aurora Foundation
Dashboard, branding, command interface, universal input, theme system and core contracts.

### Phase 2 — Aurora Brain
Intent router, planner, tool registry, permissions, verification and memory.

### Phase 3 — File + System
File Commander, system diagnostics, telemetry, battery, task manager and safe automation.

### Phase 4 — PDF Studio
Document workspace, PDF operations, OCR and document AI.

### Phase 5 — Image Studio
Professional editing, canvas, layers and AI-assisted workflows.

### Phase 6 — Study Center
Academic extraction, notes, quizzes, flashcards and revision workflows.

### Phase 7 — Orbit / Research
Web search, source aggregation, research workflows and live information.

### Phase 8 — Vision / Screen Agent
Screen understanding and authorized UI workflows.

### Phase 9 — Mission System
Multi-step autonomous workflows, verification, retry and recovery.

### Phase 10 — 6 GB Optimization
Resource budgets, lazy loading, memory pressure handling and performance profiling.

### Phase 11 — Windows Packaging
Self-contained user-facing application, crash handling, logging and update architecture.

### Phase 12 — Full QA
Unit tests, integration tests, UI tests, offline tests, low-RAM tests and end-to-end mission tests.

---

## Current Repository Direction

This repository is intentionally being transformed from the former **Arlen Nexus** implementation into the **Arlen Aurora** architecture described above.

The repository should contain only Aurora-specific implementation as development proceeds. Legacy Nexus modules are not part of the target architecture.

---

## Product Statement

> **ARLEN AURORA — one assistant, one interface, many capabilities.**

The objective is not to imitate a movie character. The objective is to build a practical, resource-aware, customizable personal AI environment that feels coherent, intelligent and genuinely useful on a Windows desktop.
