# ARLEN AURORA — FINAL PRODUCT SPECIFICATION

> **ARLEN NEXUS → ARLEN AURORA**
>
> The original Nexus vision, fully evolved into a unified AI desktop environment.

## Identity

- **Original:** ARLEN NEXUS — *Adaptive Responsive Local Executive Neural-Assistant*
- **Final product:** ARLEN AURORA — *Adaptive Responsive Local Executive Neural-Assistant*
- **Architecture:** *Autonomous Unified Reasoning & Orchestration Responsive Architecture*
- **AURA:** not a separate product name. The product identity is **AURORA**.

---

## Final Dashboard

```text
┌──────────────────────────────────────────────────────────────────────┐
│  ARLEN AURORA        Ask Aurora...                    ● ONLINE       │
├───────────────┬──────────────────────────────────────┬───────────────┤
│ ✦ AI          │              AURORA CORE             │ SYSTEM        │
│ ◈ IMAGE       │                  ◉                   │ CPU       18% │
│ ▣ PDF         │                                      │ RAM     3.2GB │
│ ▤ FILES       │          "How can I help?"           │ STORAGE   61% │
│ ◫ STUDY       ├──────────────────────────────────────┤ TEMP     1.4G │
│ ◌ RESEARCH    │  ＋ Type a command...          🎙 ➤│ NETWORK  42M  │
│ ⚙ SYSTEM      │                                      │ TASKS         │
│ ◉ TOOLS       │                                      │ • Mission 01  │
│ 🎨 THEMES     │                                      │ • Export      │
│               │                                      │ BATTERY  87%  │
└───────────────┴──────────────────────────────────────┴───────────────┘
```

The shell is unified: sidebar buttons replace the central workspace instead of launching disconnected apps. The universal `+` accepts files, folders, images, PDFs, documents, screenshots, audio/video, URLs and clipboard data.

---

# Module UI Map

## ✦ AI / AURORA

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   ✦ AI / AURORA                                   ● READY    │
├───────────────┬──────────────────────────────────────┬───────────────┤
│ NEW CHAT      │             CONVERSATION             │ CONTEXT       │
│ Today         │ You: amar PDF ta summarize koro     │ Memory   ON   │
│ • Study       │ Aurora: অবশ্যই...                   │ Mode    Smart │
│ • Research    │                                      │ Files     ✓   │
│ • Writing     │ ＋ Ask anything...             🎙 ➤│ PDF       ✓   │
└───────────────┴──────────────────────────────────────┴───────────────┘
```

Chat, reasoning, maths, calculations, problem solving, writing, rewriting, translation, planning, Banglish understanding and Bangla replies.

## ◈ IMAGE STUDIO

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   ◈ IMAGE STUDIO                                   ● READY    │
├────────────┬───────────────────────────────────┬─────────────────────┤
│ CANVAS     │            IMAGE CANVAS           │ AI / EDIT           │
│ Import  ＋ │                                   │ Enhance             │
│ Crop       │          [  IMAGE  ]              │ Upscale             │
│ MultiCrop  │                                   │ Restore             │
│ Rotate     │                                   │ Denoise             │
│ Perspective│                                   │ Remove Object       │
│ Resize     ├───────────────────────────────────┤ Background          │
│ Light      │ Undo  Redo  Before/After  Export │ Layers / Mask / Text│
└────────────┴───────────────────────────────────┴─────────────────────┘
```

Crop, multi-crop, perspective, rotate, resize, exposure, color, curves, HSL, layers, masks, blend modes, text, shapes, gradients, filters, presets, batch editing, OCR and supported local AI-assisted enhancement/restoration.

**Native-module rule:** if a feature is labelled Aurora-native, Aurora should implement/integrate that capability inside its own Image Studio. It must not silently upload the image to another AI and return the result as if Aurora processed it locally.

## ▣ PDF STUDIO

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   ▣ PDF STUDIO                                      ● READY   │
├──────────────┬───────────────────────────────────┬───────────────────┤
│ PAGES        │             PDF VIEW               │ AI / DOCUMENT     │
│ 01 02 03 ... │          ┌──────────────┐         │ Summarize         │
│ Merge        │          │    PAGE      │         │ Rewrite           │
│ Split        │          └──────────────┘         │ Translate         │
│ Rotate       │                                   │ Ask PDF / OCR     │
└──────────────┴───────────────────────────────────┴───────────────────┘
```

Read/search, page operations, merge/split, compression, extraction, OCR, annotations, image→PDF, PDF→image, text extraction, AI summarization/rewrite/translation/Q&A and text editing where technically supported.

## ▤ FILE COMMANDER

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   ▤ FILE COMMANDER                                  ● READY   │
├───────────────┬──────────────────────────────────┬───────────────────┤
│ LOCATIONS     │ 🔍 Search / command              │ DETAILS           │
│ Desktop       │ notes.pdf   PDF      4.2 MB      │ Name / Type / Size │
│ Documents     │ image.png   IMG      2.1 MB      │ Modified / Path    │
│ Downloads     │                                  │                   │
│ Pictures      │ ＋ Import  Select All  Undo      │ Organize / Move    │
└───────────────┴──────────────────────────────────┴───────────────────┘
```

Natural-language search, rename, batch rename, copy/move, folders, categorization, duplicate/large-file detection, storage analysis and rollback where feasible.

```text
SCAN → PLAN → PREVIEW → PERMISSION → EXECUTE → VERIFY
```

## ◫ STUDY CENTER

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   ◫ STUDY CENTER                                    ● READY   │
├───────────────┬──────────────────────────────────┬───────────────────┤
│ MATERIAL      │             STUDY HUB             │ AI TOOLS          │
│ ＋ Add PDF    │ [ Chapter / Topic ]              │ Notes             │
│ Biology.pdf   │ Progress ███████░░░ 62%          │ Summary / MCQ      │
│ Physics.pdf   │                                  │ Flashcards / Quiz  │
└───────────────┴──────────────────────────────────┴───────────────────┘
```

Local material → notes, summaries, explanations, formulas, important questions, MCQs, Q&A, flashcards, quizzes and revision sheets.

## ◌ ORBIT RESEARCH

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   ◌ ORBIT RESEARCH                                  ● ONLINE  │
├───────────────┬──────────────────────────────────┬───────────────────┤
│ HISTORY       │ 🔎 [ Research question ]         │ SOURCES           │
│ Today         │ ☑ Deep Research                 │ Source 01 ✓       │
│ Yesterday     │ ☑ Compare Sources               │ Source 02 ✓       │
│ Bookmarks     │ ☑ Find Latest                   │ Source 03 ✓       │
├───────────────┴──────────────────────────────────┴───────────────────┤
│ SUMMARY • FINDINGS • CONTRADICTIONS • SOURCES                       │
└──────────────────────────────────────────────────────────────────────┘
```

Quick, Standard, Deep and Academic research. Online sources are visibly separated from local/offline knowledge.

## ⚙ SYSTEM CENTER

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   ⚙ SYSTEM CENTER                                 ● HEALTHY  │
├───────────────┬──────────────────────────────────┬───────────────────┤
│ CPU           │ CPU       █████░░░░ 18%          │ Refresh           │
│ RAM           │ RAM       ██████░░░ 3.2/8 GB     │ Cleanup           │
│ STORAGE       │ Storage   ███████░░ 61%          │ Processes         │
│ BATTERY       │ Temp      47°C                  │ Diagnose          │
│ NETWORK       │ Battery   ████████░ 87%          │ Optimize          │
├───────────────┴──────────────────────────────────┴───────────────────┤
│ HEALTH: ✓ No critical problems detected                              │
└──────────────────────────────────────────────────────────────────────┘
```

CPU/RAM/storage/temp/battery/network/process monitoring, diagnostics, startup/process inspection and safe resource cleanup. “RAM refresh” means supported cleanup/working-set optimization, not physical RAM expansion.

## ◉ AURORA TOOLS

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ◉ AURORA TOOLS                                                        │
├──────────────────────────────────────────────────────────────────────┤
│ 🧮 Calculator   📦 Converter   📝 Text   🔎 OCR   📋 Clipboard       │
│ 🕒 Timers       📸 Screenshot  🎙 Voice 📁 Batch  🔐 Hash/Check      │
└──────────────────────────────────────────────────────────────────────┘
```

## 🎨 THEME STUDIO

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← HOME   🎨 THEME STUDIO                                             │
├───────────────┬──────────────────────────────────┬───────────────────┤
│ THEMES        │          LIVE PREVIEW            │ CUSTOMIZE         │
│ ● Aurora      │         ARLEN AURORA             │ Accent             │
│ ○ Obsidian    │             ◉                    │ Background / Cards │
│ ○ Nebula      │         Ask Aurora...            │ Glow / Font        │
│ ○ Arctic      │                                  │ Animation / Core   │
│ ○ Emerald     │                                  │ Wallpaper          │
│ ○ Crimson     │                                  │ [ SAVE THEME ]     │
│ ○ Solar       │                                  │                    │
│ ○ Cyber       │                                  │                    │
│ ○ Minimal     │                                  │                    │
│ ○ Midnight    │                                  │                    │
└───────────────┴──────────────────────────────────┴───────────────────┘
```

Ten initial themes: Aurora, Obsidian, Nebula, Arctic, Emerald, Crimson, Solar, Cyber, Minimal and Midnight.

---

# Universal Add / Voice / Mission

```text
┌──────────────────────────────────────────────────────────────┐
│                         ADD TO AURORA                         │
├──────────────────────────────────────────────────────────────┤
│  📄 File     📁 Folder     🖼 Image     ▣ PDF                │
│  🔗 URL      📋 Clipboard  📸 Screenshot 🎵 Audio            │
│  🎬 Video                                                        │
│                    Drag & Drop Anything                      │
└──────────────────────────────────────────────────────────────┘
```

```text
┌──────────────────────────────────────────────────────────────┐
│                         ◉ LISTENING                           │
│                  “I'm listening...”                          │
│                  ▁▃▅▇▅▃▁▃▆▇▆▃▁                              │
│                         [ CANCEL ]                            │
└──────────────────────────────────────────────────────────────┘
```

Voice flow: speech → intent → Aurora Core → response → optional speech synthesis. Banglish is a supported interaction goal.

Mission flow:

```text
GOAL → PLAN → PERMISSION → EXECUTE → VERIFY → RECOVER → REPORT
```

---

# Online + Offline

```text
                         AURORA CORE
                              │
                        NETWORK CHECK
                              │
                ┌─────────────┴─────────────┐
                │                           │
             ONLINE                      OFFLINE
                │                           │
       Search / current info        Local AI if bundled
       Optional cloud AI            Files / PDF / Image
       Optional voice API           Calculator / Study
       Optional online tools        System / local automation
                │                           │
                └─────────────┬─────────────┘
                              │
                         Aurora result
```

Wi-Fi/internet enables live web information and optional cloud connectors. Without internet, Aurora falls back to bundled/local capabilities that actually exist on the device. It must never fake a live result or claim a cloud operation was completed offline.

---

# API & Connectivity Center

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ← SYSTEM   ⚙ API & CONNECTIVITY                           ● SECURE  │
├────────────────┬──────────────────────────────────────┬──────────────┤
│ PROVIDERS      │ CONNECTION CONTROL                  │ STATUS       │
│ AI             │ Mode: ● Auto  ○ Online  ○ Offline │ AI        ✓  │
│ SEARCH         │ Cloud upload: ● NEVER               │ Search    ✓  │
│ VOICE          │              ○ ASK EVERY TIME       │ Voice     ○  │
│ IMAGE          │              ○ ALLOW SELECTED       │ Image     ○  │
│ PDF            │                                      │ PDF       ○  │
│ SECURITY       │ [ Test Connections ] [ Revoke Keys ]│ Local     ✓  │
└────────────────┴──────────────────────────────────────┴──────────────┘
```

### Free-first provider strategy

| Capability | Adapter strategy | Default |
|---|---|---|
| AI reasoning | Gemini or another permitted free-tier provider + local engine | Local for sensitive data |
| Search | Configurable search/web connector | Query-only unless needed |
| Voice | ElevenLabs or compatible provider + local voice when available | Ask before cloud audio |
| Image | Aurora local Image Core + optional providers | Local only |
| PDF | Aurora local PDF Core + optional providers | Local only |

Free tiers, quotas and policies change. Provider adapters must therefore be replaceable and Aurora should show current status/limits instead of hard-coding old quotas.

Google currently documents free access for selected Gemini API models, but also states that free-tier content may be used to improve products. Therefore private images, PDFs and sensitive personal information must not be routed to a free cloud AI by default. ElevenLabs currently lists a $0 Free plan with 10k monthly credits and API-related capabilities; current provider limits must still be checked at implementation time.

---

# Privacy Firewall — NON-NEGOTIABLE

```text
┌──────────────────────────────┬────────────────────────────────┐
│ DATA                         │ DEFAULT                        │
├──────────────────────────────┼────────────────────────────────┤
│ Personal images              │ ✓ LOCAL ONLY                   │
│ Private PDFs                 │ ✓ LOCAL ONLY                   │
│ Documents / files            │ ✓ LOCAL ONLY                   │
│ Clipboard                    │ ✓ LOCAL ONLY                   │
│ Personal memory              │ ✓ LOCAL ONLY                   │
│ Voice                        │ ✓ LOCAL unless approved       │
│ Web search                   │ → QUERY ONLY                   │
│ Cloud AI                     │ → ASK FIRST                    │
│ Cloud image/PDF processing   │ → ASK FIRST                    │
└──────────────────────────────┴────────────────────────────────┘
```

**Default cloud upload policy = NEVER.**

Any cloud action must show the provider, purpose, data being sent and a clear one-time approval button:

```text
┌──────────────────────────────────────────────────────────────┐
│                     CLOUD ACTION REQUEST                     │
├──────────────────────────────────────────────────────────────┤
│ Service: <provider>                                          │
│ Purpose: <operation>                                         │
│ Data: <selected item(s)>                                     │
│ Destination: <provider>                                      │
│                                                              │
│             [ CANCEL ]       [ ALLOW ONCE ]                  │
└──────────────────────────────────────────────────────────────┘
```

No silent uploads, hidden background sharing or automatic third-party AI processing of private content.

API keys must not be hard-coded. Store them using appropriate Windows secure credential storage, with test/revoke controls and no secrets in logs.

---

# Universal Windows Hardware Target

The product must **not be tied to one specific PC**. It should detect CPU, RAM, GPU, storage, OS and available resources and adapt automatically.

```text
┌──────────────────────────────────────────────────────────────┐
│ PROFILE       PRACTICAL TARGET                               │
├──────────────────────────────────────────────────────────────┤
│ Minimum       4 GB RAM • Windows 10/11 x64 • SSD preferred  │
│ Recommended   8 GB RAM • modern Intel i5/Ryzen equivalent   │
│ Better        16 GB+ RAM • stronger CPU/GPU • SSD           │
└──────────────────────────────────────────────────────────────┘
```

Heavy local generative AI/image workloads can exceed low-RAM hardware. Aurora must degrade gracefully rather than promise impossible local performance.

---

# Resource Strategy

```text
IDLE → CORE ONLY → DETECT TASK → LOAD ENGINE → EXECUTE
                                      ↓
                                   VERIFY
                                      ↓
                              RELEASE RESOURCES
```

Use lazy loading, memory-pressure detection, adaptive quality, cache control, background throttling and model lifecycle management.

---

# Agent Architecture

```text
USER INTENT
    ↓
UNDERSTAND → PLAN → SELECT TOOL/AGENT
    ↓
PERMISSION CHECK
    ↓
EXECUTE → VERIFY → RECOVER/RETRY → REPORT
```

Agents: File, Screen/Application, Research, Study, Image, PDF, System and Mission.

Authorized UI automation: **OBSERVE → UNDERSTAND → PLAN → ACT → VERIFY**.

---

# Single-EXE Goal

```text
ArlenAurora.exe
```

The user-facing target is one unified EXE. Internal modular engines/runtimes are allowed, but the user should not need to install separate companion applications for Aurora's core local features. Large AI models may make a fully self-contained package very large; model size, runtime, licensing and Windows constraints must be handled honestly.

---

# Final Architecture

```text
ARLEN AURORA
│
├── UI SHELL
│   ├── Dashboard / AI
│   ├── Image Studio
│   ├── PDF Studio
│   ├── File Commander
│   ├── Study Center
│   ├── Orbit Research
│   ├── System Center
│   ├── Aurora Tools
│   ├── Mission View
│   ├── API / Privacy Center
│   └── Theme Studio
│
├── AURORA CORE
│   ├── Intent Router
│   ├── Planner
│   ├── Tool Router
│   ├── Permission Manager
│   ├── Mission Manager
│   ├── Verifier / Recovery
│   └── Memory
│
├── LOCAL ENGINES
│   ├── AI / Reasoning
│   ├── Vision / Image
│   ├── PDF / OCR
│   ├── Files
│   ├── Study
│   └── System
│
├── ONLINE CONNECTORS
│   ├── Search / Research
│   ├── Current Information
│   ├── Optional AI
│   ├── Optional Voice
│   ├── Optional Image
│   └── Optional PDF
│
└── RUNTIME
    ├── Resource Manager
    ├── Privacy Firewall
    ├── Secure Key Store
    ├── Logging
    ├── Updates
    └── Packaging
```

## Final Principle

> **ARLEN NEXUS becomes ARLEN AURORA.**
>
> **One assistant. One interface. Many capabilities.**
>
> Aurora-native features should be real integrated modules. External APIs are connectors, never hidden replacements for Aurora's own work.

Repository name may retain `ARLEN-NEXUS-PRIVATE` for continuity, while the product identity is **ARLEN AURORA**.
