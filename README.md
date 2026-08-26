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

```text
Ollama         = AI Brain
Python Tools   = AI Hands
SQLite Memory  = Local Memory
Premium UI     = AI Workstation
```

---

# Current Status

## Ready Environment

Current development/test environment:

- ✅ Python 3.11.9
- ✅ Ollama 0.32.15
- ✅ Qwen2.5:3B Text Model
- ✅ Qwen2.5VL:3B Vision Model
- ✅ FFmpeg
- ✅ Image-processing Python stack

Primary target:

- Windows desktop
- Offline-first operation
- Low-resource design
- 4GB RAM class PC support for the lightweight/core workflow
- 8GB+ RAM recommended for smoother Vision workloads

ARLEN should avoid keeping both local models loaded at the same time on low-memory systems. The normal text model and vision model should be loaded only when required.

---

# PC Requirements & Official Setup Links

> This section documents the current development/manual environment. The final user-facing goal is still a simple `ARLEN-NEXUS-Setup.exe` experience where ARLEN detects and configures the PC automatically with as little manual setup as possible.

## 1. Python

Current tested version: **Python 3.11.9**

Official links:

- Python 3.11.9: https://www.python.org/downloads/release/python-3119/
- Python downloads: https://www.python.org/downloads/windows/

Python is used for the ARLEN backend, tools, memory, document processing, image processing and Windows integration.

## 2. Ollama

Current tested version: **Ollama 0.32.15**

Official links:

- Windows download: https://ollama.com/download/windows
- Ollama website: https://ollama.com/

Check installation:

```cmd
ollama --version
```

## 3. Text Brain — Qwen2.5:3B

Used for:

- Offline chat
- Command understanding
- Reasoning
- Tool planning
- Normal assistant tasks

Official model page:

- https://ollama.com/library/qwen2.5

Install:

```cmd
ollama pull qwen2.5:3b
```

Test:

```cmd
ollama run qwen2.5:3b
```

## 4. Vision Brain — Qwen2.5VL:3B

Used for:

- Image understanding
- Screenshot analysis
- Document-image understanding
- Smart image-editing suggestions

Official model page:

- https://ollama.com/library/qwen2.5vl

Install:

```cmd
ollama pull qwen2.5vl:3b
```

Test:

```cmd
ollama run qwen2.5vl:3b
```

Recommended:

- Core/normal ARLEN use: 4GB RAM target
- Vision workloads: 8GB+ RAM recommended for a smoother experience

## 5. FFmpeg

Used for future/local media-processing features.

Official links:

- https://ffmpeg.org/download.html
- Windows build information: https://ffmpeg.org/download.html#build-windows

Check:

```cmd
ffmpeg -version
```

---

# Python Dependency Stack

The current ARLEN V1 development stack uses lightweight Python libraries instead of separate large desktop applications whenever possible.

## Core / System

### psutil

CPU, RAM, disk, battery and process/system information.

- https://pypi.org/project/psutil/

```cmd
pip install psutil
```

### requests

Local Ollama HTTP/API communication and other controlled HTTP tasks.

- https://pypi.org/project/requests/

```cmd
pip install requests
```

### SQLite

Python includes `sqlite3` by default. No separate installation is normally required.

Test:

```cmd
python -c "import sqlite3; print('SQLite OK')"
```

---

# PDF Dependencies

### PyMuPDF

PDF reading, extraction, rendering and document processing.

- https://pypi.org/project/PyMuPDF/

```cmd
pip install pymupdf
```

### pypdf

PDF merge, split and page-level operations.

- https://pypi.org/project/pypdf/

```cmd
pip install pypdf
```

---

# Image Dependencies

### Pillow

Basic image loading, resizing, conversion and enhancement.

- https://pypi.org/project/pillow/

```cmd
pip install pillow
```

### OpenCV

Sharpness, dehaze-style processing, blur, contrast and advanced local image operations.

- https://pypi.org/project/opencv-python/

```cmd
pip install opencv-python
```

### NumPy

Image/numerical processing dependency.

- https://pypi.org/project/numpy/

```cmd
pip install numpy
```

### piexif

Image EXIF/metadata handling.

- https://pypi.org/project/piexif/

```cmd
pip install piexif
```

### rembg

Optional background-removal dependency. It is installed/available in the development environment but background removal is **not** a default ARLEN V1 workflow; background blur and enhancement are preferred.

- https://pypi.org/project/rembg/

```cmd
pip install rembg
```

---

# UI Dependency

### PySide6

Planned main Windows desktop UI framework for ARLEN NEXUS.

Used for:

- Main desktop window
- Panels
- Command Center
- Theme engine
- Animated sphere/background system
- Quick Tools

Official links:

- https://pypi.org/project/PySide6/
- https://doc.qt.io/qtforpython-6/

Install:

```cmd
pip install PySide6
```

---

# Optional OCR

OCR is **not required to start ARLEN V1 development**.

Normal digital PDFs can be processed with PyMuPDF/pypdf, while Qwen2.5VL can assist with screenshots and image understanding.

OCR becomes useful for:

- Scanned PDFs
- Photos of documents
- Printed text extraction
- Image-to-text workflows

Possible future option:

### Tesseract OCR

- Official project: https://github.com/tesseract-ocr/tesseract
- Python wrapper: https://pypi.org/project/pytesseract/

OCR remains optional until the scanned-document workflow is implemented and tested.

---

# Quick Development Install Command

For the Python-side V1 stack:

```cmd
pip install psutil requests pymupdf pypdf pillow opencv-python numpy piexif rembg PySide6
```

Environment check example:

```cmd
python -c "import psutil, requests, fitz, pypdf, PIL, cv2, numpy, piexif, sqlite3, PySide6; print('ARLEN V1 Environment Ready')"
```

---

# Final Installer Goal

The final ARLEN NEXUS user experience should be:

```text
Download
   ↓
ARLEN-NEXUS-Setup.exe
   ↓
Install
   ↓
Automatic System Detection
   ↓
Automatic Configuration
   ↓
ARLEN Ready
```

The installer/first-launch setup should detect:

- Existing Ollama installation
- Installed Qwen models
- FFmpeg
- Available browsers
- Installed applications
- ARLEN-supported tools
- Hardware/RAM capability

The user should not need to manually build folders, edit code or configure Python packages for the final release.

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

- Python/runtime environment
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

V1 includes lightweight smart-vision capabilities for practical image understanding.

Advanced Vision Pro will be considered only after the stable V1 base is complete.

---

# PC Assistant

ARLEN can help with:

- Open Chrome
- Open Brave
- Open VS Code
- Launch installed applications
- Find files
- Open documents
- Search useful documents/news/information through a browser
- Safe ARLEN/system refresh utilities

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
- Compact battery/sound/brightness controls
- UI sound effects only — no AI voice system

---

# Version History

| Version | Focus |
|---|---|
| v0.1 | Foundation |
| v0.2 | Desktop architecture |
| v0.3 | Local AI setup |
| v0.4 | Tool architecture |
| v0.5 | Memory system |
| v0.6 | Document intelligence |
| v0.7 | Image intelligence |
| v0.8 | Futuristic UI |
| v0.9 | Theme and sound system |
| v1.0 | Workstation interface |
| v1.1 | Smart environment setup |

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

These are not current priorities. Expansion will be considered only after a stable V1 release.

---

# Development Roadmap

1. Backend Core
2. Ollama Integration
3. Memory System
4. Tool Manager
5. System Scanner
6. PDF Module
7. Image + Smart Vision Module
8. File Assistant
9. System Tools / Safe Refresh
10. Premium UI
11. Windows EXE + Installer
12. Stability Testing

---

# Goal

Build a private AI workstation that is:

- Local
- Fast
- Reliable
- Intelligent
- Low-resource aware
- Easy to install
- Expandable after V1 stability

**ARLEN NEXUS — Your personal AI workstation.**
