# ARLEN NEXUS v0.4 — Function Test Report

**Owner / Concept / Direction:** Jubaer Hossain  
**ARLEN:** Adaptive Responsive Local Executive Neural-Assistant  
**NEXUS:** Neural Execution and Experience Unified System  
**Verified commit:** `b54d8d415d575f3e0ff282f78c38981d98291318`  
**Windows workflow run:** `32768885259`

## Automated Windows result

- Python compilation: **PASS**
- Core automated tests: **20/20 PASS**
- QML lint: **PASS**
- PyInstaller one-folder build: **PASS**
- `ARLEN NEXUS.exe` existence: **PASS**
- Windows launch smoke test: **PASS (15 seconds)**
- Portable ZIP creation: **PASS**
- GitHub artifact upload: **PASS**
- Downloaded artifact SHA-256 verification: **PASS**

## Artifact evidence

- Artifact name: `ARLEN-NEXUS-Portable-v0.4-Windows`
- Artifact SHA-256: `bfbaead7e7cc1607a7db41f0b871e2075b955498640e0d92c842de315b404fdb`
- EXE SHA-256: `f605e7e0e95236b8f1d4c7e762f2b38dd527a113b764f3c86f90ff800a3a6333`
- Portable ZIP size: approximately 263 MB
- Extracted portable folder size: approximately 671 MB

## Newly verified v0.4 functions

| Area | Status | Evidence / limitation |
|---|---|---|
| Existing v0.3 core regression | PASS | Original 17 tests remain covered. |
| Update staged-file checksum | PASS | SHA-256 verification succeeds for valid files. |
| Update unsafe/protected path rejection | PASS | Traversal, absolute, updater and UserData paths rejected. |
| Owner-PIN update apply | PASS | Wrong PIN rejected; verified update applied after correct PIN. |
| Update rollback | PASS | Replaced file restored from versioned backup. |
| PDF merge | PASS | Ordered input PDFs merged into a new PDF. |
| PDF split | PASS | Merged PDF split into separate page files. |
| Image Studio core | PASS | Crop, adjustment, prompt export, original preservation and Image-to-PDF regression tests pass. |
| Full QML syntax/type lint | PASS | Windows PySide6 `qmllint` completed successfully. |
| Portable EXE build | PASS | PyInstaller produced `ARLEN NEXUS.exe` and runtime folder. |
| Windows process launch | PASS (smoke test) | EXE stayed running for 15 seconds on GitHub Windows Server 2025 runner. |

## Still not honestly complete

| Area | Status | Required next evidence |
|---|---|---|
| Clean Windows 11 personal-account checklist | WINDOWS TEST REQUIRED | Extract ZIP and complete every manual UI/system checklist item. |
| Real microphone capture/transcription | NOT BUNDLED | A compatible portable local voice model/runtime is required. |
| Local TTS | NOT BUNDLED | Portable multilingual TTS voices/runtime required. |
| Local GGUF conversation | PARTIAL | Provider hook exists; model/runtime pack is not bundled in this artifact. |
| Printed/handwriting OCR | PARTIAL | Provider hook exists; OCR model/runtime pack is not bundled. |
| Full advanced PDF suite | PARTIAL | Image-to-PDF, merge and split exist; remaining roadmap tools are pending. |
| Code signing | NOT IMPLEMENTED | A trusted Windows code-signing certificate is required. |

## Release conclusion

v0.4 is a real Windows portable CI build containing `ARLEN NEXUS.exe`; it is not a source ZIP. Automated Windows gates pass. It must still be described as a **verified CI portable build**, not the final production release, until the clean-Windows manual checklist and unbundled capability packs are completed.

