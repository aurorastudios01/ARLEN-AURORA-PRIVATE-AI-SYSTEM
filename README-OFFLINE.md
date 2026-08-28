# AURORA

> **Create • Edit • Organize • Control**

**AURORA** is a private, offline-first Windows desktop suite for documents, images, OCR, video, files, system monitoring and practical everyday utilities.

It is **not an AI assistant**. AURORA contains no chatbot, generative AI, local language model, AI voice, cloud AI provider, Ollama, Qwen, Llama, Gemini, OpenAI or ElevenLabs dependency.

The product goal is simple:

```text
ONE APPLICATION
ONE INSTALLER
MANY OFFLINE TOOLS
NO EXTRA DOWNLOADS
```

## Product identity

- **Application name:** AURORA
- **Platform:** Windows 10/11 x64
- **Product type:** Offline creative, document and system utility suite
- **Tagline:** Create • Edit • Organize • Control
- **Primary colors:**
  - Aurora Cyan — `#19D3FF`
  - Electric Violet — `#7B4DFF`
  - Midnight Navy — `#07111F`
  - Ice White — `#F4F8FF`
  - Success Green — `#4FE28A`
- **Visual direction:** clean Windows 11 interface, dark glass panels, restrained aurora glow, crisp typography and high-contrast controls
- **Logo direction:** a geometric capital “A” formed from two aurora-light ribbons, recognizable as a small Windows app icon

The identity must avoid AI brains, robots, chat bubbles, microphones and cloud imagery.

## Startup experience

AURORA opens with a short two-to-three-second splash sequence:

```text
AURORA LOGO
     ↓
Loading Core
     ↓
PDF Engine
     ↓
Image Tools
     ↓
Media Tools
     ↓
System Ready
     ↓
Dashboard
```

All required engines are packaged with the application. The startup screen must never ask the user to download an external runtime or model.

## Main navigation

```text
HOME
IMAGE
PDF
OCR
VIDEO
FILES
SYSTEM
TOOLS
THEMES
SETTINGS
```

## Home dashboard

The dashboard provides:

- Quick access to Image, PDF, OCR, Video and File tools
- Recent files and operations
- Active exports and conversions
- CPU, RAM, storage, network and battery summaries
- Favorite tools
- Safe cleanup notifications
- Operation history and recoverable actions
- Offline-ready status

## Image Studio

AURORA Image Studio provides local, non-generative editing:

### Core editing

- Open, save and export common image formats
- Crop, rotate, flip and resize
- Perspective correction
- Exposure, brightness and contrast
- Highlights and shadows
- Temperature, tint and saturation
- Levels, histogram, curves and HSL
- Text, shapes and watermark
- Basic layers, masks and blend modes
- Metadata inspection and removal
- Batch resize, conversion and optimization
- Before/after comparison
- Non-destructive undo and redo history

### Offline enhancement

- Auto levels
- Auto contrast
- White balance
- Sharpen
- Unsharp mask
- Clarity
- Local contrast
- Edge enhancement
- Traditional denoise
- Basic deblur filters
- Interpolation-based upscale

These tools improve visible information already present in an image. They do not invent missing faces, textures or details.

### Background blur

- Subject/background selection
- Brush-based mask editing
- Gradient blur
- Radial blur
- Blur-strength control
- Feather and edge refinement
- Multiple bokeh shapes
- Background-mask preview
- Manual correction for difficult edges
- Before/after slider

Background blur uses local image processing and segmentation. No image is uploaded.

## PDF Studio

- Open, read, search and print PDFs
- Page thumbnails and navigation
- Merge and split
- Reorder, rotate and delete pages
- Image to PDF
- PDF to image
- Text and image extraction
- Compression
- Password protection and authorized unlocking
- Annotation, highlighting, drawing and stamps
- Text boxes, signatures and watermarks
- Page numbers, headers and footers
- Form filling
- Redaction
- OCR for scanned pages
- Searchable-PDF creation
- Export presets

Complex existing PDF layouts cannot always be edited like a Word document. AURORA must communicate those limits honestly.

## OCR Studio

- Bengali and English OCR
- Image OCR
- Scanned-PDF OCR
- Region selection
- Page orientation correction
- Basic preprocessing and noise cleanup
- Searchable PDF generation
- Copy and text export
- Batch OCR
- Side-by-side source and recognized-text view
- Manual correction before export

OCR accuracy depends on scan quality, font, resolution and page condition.

## Video Studio

The first release targets practical offline editing rather than replacing a professional nonlinear editor.

- Video playback and timeline
- Trim, cut and split
- Join multiple clips
- Crop, rotate and resize
- Speed control
- Mute and volume adjustment
- Audio extraction and replacement
- Text, title, logo and watermark overlays
- Fade in and fade out
- Basic transitions
- Brightness, contrast and saturation
- Sharpen and denoise filters
- Frame extraction
- Subtitle import and export
- GIF creation
- Format conversion
- Compression and export presets
- Hardware acceleration where supported

## File Commander

- File and folder browsing
- Search, sort and filtering
- Copy, move and rename
- Batch rename
- Folder creation
- Duplicate detection
- Large-file finder
- File comparison
- Hash and checksum
- ZIP creation and extraction
- File previews
- Recent files
- Storage analysis
- Operation history
- Undo where technically possible
- Confirmation before deletion or high-impact operations

Safe operation flow:

```text
SCAN → PREVIEW → PERMISSION → EXECUTE → VERIFY
```

## System Center

- CPU, RAM, disk and network monitoring
- Battery information
- Temperature where hardware exposes it
- Hardware and Windows information
- Running-process viewer
- Confirmed process termination
- Startup-app management
- Storage breakdown
- Temporary-file scanning
- Recycle Bin tools
- Network diagnostics
- Windows service inspection
- System report export
- Safe cache cleanup

Administrator permission is requested only for operations that genuinely require it. AURORA must not claim to increase physical RAM or perform impossible performance boosts.

## Aurora Tools

### Quick tools

- Calculator
- Unit converter
- Date and time calculator
- Timer and stopwatch

### Text and data

- Text cleanup
- Word and character counter
- JSON formatter and validator
- XML formatter
- Hash and checksum
- QR generator and reader

### Media and capture

- Screenshot
- Screen color picker
- Image converter
- Audio converter
- Video converter
- Metadata inspector

### Files and system

- Clipboard history
- Batch rename
- Duplicate finder
- Archive manager
- File comparison
- Storage analyzer
- Network check
- Process viewer

## Themes

Initial theme collection:

| Theme | Direction |
|---|---|
| Aurora | Cyan and violet signature theme |
| Obsidian | Neutral black and graphite |
| Nebula | Deep violet and cosmic blue |
| Arctic | Ice white and cool blue |
| Emerald | Dark green and teal |
| Crimson | Charcoal and controlled red |
| Solar | Warm amber and orange |
| Cyber | Cyan grid and dark navy |
| Minimal | Clean, low-glow interface |
| Midnight | Deep blue, reduced brightness |

Users can customize:

- Accent color
- Background
- Card appearance
- Glow intensity
- Font
- Animation level
- Wallpaper
- Compact mode
- Reduced motion
- High contrast

## Privacy and security

AURORA is local by design:

- No AI provider
- No analytics by default
- No personal file upload
- No hidden network processing
- No secrets in logs
- Clear file-access permissions
- Confirmation for destructive actions
- Recoverable operations where possible
- Privacy-safe diagnostic logs
- Optional update checks can be disabled

## Proposed technology

```text
C# + .NET
WinUI 3
PDFium or MuPDF
Tesseract / Windows OCR
OpenCV + ImageSharp
FFmpeg
SQLite
Windows system APIs
MSIX or signed Windows installer
```

All required runtimes, codecs, OCR language data and native libraries should ship inside the AURORA installer.

## Expected package size

A practical target without AI models is approximately:

```text
500 MB – 1.3 GB
```

Actual size depends on codecs, OCR language data, PDF engine, architecture packaging and bundled runtime choices.

## Development roadmap

1. Product identity, application shell and navigation
2. Theme system and startup experience
3. File Commander
4. Image Studio and background blur
5. PDF Studio
6. OCR Studio
7. System Center
8. Aurora Tools
9. Video Studio
10. Security, permissions, operation history and undo
11. Installer and update system
12. Performance, accessibility and full QA

## Product principles

- Offline first
- One installer
- No extra tool downloads
- Fast startup
- Honest capability boundaries
- Safe destructive actions
- Clear progress and errors
- No fabricated success
- Broad Windows hardware support
- Graceful performance scaling

## Final statement

> **AURORA — Create • Edit • Organize • Control**
>
> One private Windows application for offline document, media, file and system work.
