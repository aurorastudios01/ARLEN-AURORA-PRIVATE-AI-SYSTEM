# ARLEN NEXUS

## Full name

**ARLEN — Adaptive Responsive Local Executive Neural-Assistant**  
**NEXUS — Neural Execution and Experience Unified System**

**Built for Jubaer Hossain — Controlled by its owner.**

ARLEN NEXUS is a private, offline-first Windows desktop intelligence and system-control environment. Its stable core is designed to run locally, while optional capability packs provide conversation, voice, Vision/OCR, image and PDF features without a system-wide developer installation.

## Privacy and owner control

- The core operates offline.
- Public information searches open through Brave only when permitted.
- Personal uploads are disabled by default.
- Login, messaging, purchases, protected changes and destructive actions require explicit approval.
- Meaningful changes require confirmation; protected actions require the owner PIN.
- Personal settings and history are stored separately under Windows UserData so application updates do not overwrite the owner's identity.
- Local images are processed without automatic blocking, deletion, blurring or uploading; originals remain unchanged by default.

## Main workspaces

ARLEN NEXUS separates features into dedicated pages: Home, Chat, Voice, System, Network, Files, Automation, Cleanup, Security, Admin, Image Studio, Vision/OCR, PDF Studio, Theme Studio and About.

## Portable release

The end-user package is a Windows portable folder containing `ARLEN NEXUS.exe` and its required runtime. The owner should not need to install Python, an editor, Visual Studio, Node, Rust, Ollama or other development tools.

Optional Local Brain, Voice and OCR capability packs are copied into ARLEN's portable folders and may load or unload independently to control RAM use.

## Safety levels

1. **Level 1 — Safe local actions:** read, inspect and open operations.
2. **Level 2 — Confirmation:** meaningful file, cleanup or system changes.
3. **Level 3 — Owner PIN:** protected, destructive and update/rollback operations.

## Current development truth

This repository contains the active development source and automated Windows portable-build workflow. A generated artifact is considered a verified CI build only after core tests, QML lint, executable creation and the Windows launch smoke test pass. A final public release still requires the complete clean-Windows checklist and must never be represented by a source ZIP.

## Owner

**Owner / Concept / Direction:** Jubaer Hossain

