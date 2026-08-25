# ARLEN NEXUS — v0.1 to v0.8 Version History and Bug Audit

Last updated: 25 August 2026  
Owner: Jubaer Hossain  
Scope: known source behavior, verified workflow evidence and the v0.8 reprogram. “Fixed” means changed in source; “Verified” is reserved for a passing Windows workflow or manual evidence.

## Version history

| Version | Main work | Advantages | Disadvantages / remaining gaps |
|---|---|---|---|
| v0.1 | Product concept, ARLEN/NEXUS identity, offline-first and owner-control rules | Clear privacy/product direction | Planning/prototype; no production installer evidence |
| v0.2 | Early PySide6/QML shell and command backend | Native desktop foundation | UI and actions were prototype-grade; little validation |
| v0.3 | PIN/profile, policy, macro safety, image foundation, image-to-PDF, staged checksums | 17 tests; safer protected actions | Live Windows behavior, packs and update delivery incomplete |
| v0.4 | Windows CI, apply/rollback foundation, PDF merge/split, portable folder | 20 tests; build/launch verified in run 32768885259 | Portable folder was not the desired user installation flow |
| v0.5 | Single-file EXE experiment | Easy-looking distribution; run 32795779576 passed | Slow first launch, temporary extraction and older interface made it unsuitable |
| v0.6 | Per-user Inno Setup and responsive transition | Normal install/uninstall/shortcut path | Transitional interface and incomplete capability wiring |
| v0.7 | Official branding, Command Center, neural sphere, telemetry, battery, warnings and safe refresh | 22 tests plus build/install/launch/screenshot in run 32809263990 | Many custom controls were visual only; layout clipping; chat/voice pack gaps |
| v0.8 | Core reprogram: animated profile system, unified conversation, working custom-visual lifecycle, automation CRUD/schedules, image examples, PDF preview backend, richer backup and truthful packs | More coherent application and fewer fake-success states; upgrade-safe | Windows/QML/installer verification is still required before release; AI/voice/OCR remain optional packs |

## v0.7 bug audit and v0.8 disposition

| Area | v0.7 defect / cause | v0.8 correction | State |
|---|---|---|---|
| Admin layout | RowLayout constraints let the owner panel collapse and text overlap the sidebar | Rebuild as responsive scrollable settings/control sections with explicit widths | Source redesign pending Windows visual gate |
| Home usage | QML referenced `backend.sessionUsage` without calling the slot | Use `backend.sessionUsage()` | Fixed in new UI source |
| Telemetry | Right rail was too narrow; long values clipped | Wider responsive cards, wrapped text and reflow | Source redesign pending visual gate |
| Command routing | Quick actions and Home input bypassed a consistent router | Single `routeInput()` chooses safe command, custom trigger or chat | Fixed/backend compiled |
| Conversation | Home and Chat owned separate models and both consumed replies, causing ghost/mismatched history | One persisted conversation file and one UI model | Fixed/backend compiled |
| Chat pack | Adding a GGUF file could still fail because llama-cpp runtime was not in the base bundle | Validate a real >64 MB model and report missing runtime separately; capability-pack packaging remains required | Partial; pack not bundled |
| Voice | Existing UI could say ready when only a folder existed; microphone button was decorative | Require a Voice Pack manifest and explicitly say recording/STT/TTS are not bundled | Truthful status fixed; voice pack pending |
| Pack status | Folder existence was treated as readiness | Manifest/model validation with NOT INSTALLED status | Fixed foundation |
| Voice language | Preference was saved but not reliably restored in UI | Expose `voiceLanguage` property and bind selector | Fixed foundation |
| Core status | Dashboard could claim “all systems nominal” while packs were missing | Core status separated from optional pack readiness | Fixed design |
| Default sphere | Static/rotating PNG did not deliver core-origin energy motion | Supplied luminous orb plus independent pulse rings, particles, flashes and six profiles; whole image does not simply spin | New design pending visual gate |
| Sphere choices | Library buttons only changed a label; every choice used the same behavior | Profile name drives distinct particle/ring density, colour and tempo | New design pending visual gate |
| Custom sphere | Same filename caused QML caching; no remove/reset | Verified unique copy, modification query, safe deletion, default restore | Fixed/backend compiled |
| Background | Setting was stored but Main.qml did not render it | Apply custom background with opacity and privacy overlay | New UI source required/visual gate |
| Automation CRUD | UI could only save; no stable identity, enable, test/run, update or delete | IDs, validation, update, enable/disable, run and PIN-protected delete | Fixed/backend compiled |
| Automation results | Unsupported actions were “Skipped” but the macro still emitted success; missing apps could crash worker | Each action returns success/failure; partial failures are reported; launches are caught | Fixed/backend compiled |
| Scheduling | UI text implied schedules but there was no scheduler | Daily/Once in-app scheduler every 20 seconds; docs state ARLEN must stay open | Fixed/backend compiled |
| Image editing | Controls were incomplete and prompt editing sounded more intelligent than it was | Ready local presets, deterministic Bangla/English keywords, visible preview, non-destructive export, honest wording | Fixed foundation |
| Image reading | Page showed results but did not prioritize the selected image/page | Large selected-image viewer plus results pane | New UI source required/visual gate |
| PDF image tools | No in-app page render/export path | Inspect, render page via PyMuPDF and export pages to PNG | Fixed/backend compiled; UI/Windows validation pending |
| System refresh | Only legacy preview folder was cleared | Clear both legacy and v0.8 preview caches | Fixed/backend compiled |
| Backup | Schedules and conversation were absent | Backup format v2 includes settings, commands, schedules and conversation | Fixed/backend compiled |
| Version status | Updater message still hard-coded v0.3 | Read `app_version` (0.8.0) | Fixed/backend compiled |

## v0.8 advantages

- One coherent routing and history path reduces duplicate responses.
- Real lifecycle controls make custom visuals and automations reversible.
- Optional packs are modular, keeping the Core usable on an 8 GB PC.
- The new default artwork and logo are owner-supplied and consistent across identity surfaces.
- Image/PDF operations remain local and non-destructive.
- UserData stays outside the installation directory, so replacing program files does not erase owner settings.

## v0.8 disadvantages and honest limits

- Richer animation increases GPU use; Reduced animation mode should be used on weak graphics or battery power.
- An 8 GB PC can run the Core, but local chat and voice together may be slow; 16 GB is recommended for larger packs.
- In-app schedules do not run after ARLEN closes or Windows logs out.
- Image “prompt” operations are keyword-driven Pillow transforms, not generative AI.
- PDF page rendering increases installer size because PyMuPDF is bundled.
- Chat is not complete until a compatible licensed GGUF and working llama-cpp runtime are packaged and tested.
- Voice remains unavailable until microphone capture, offline STT and TTS are bundled and verified.
- OCR quality depends on optional language data and is not yet release-verified.
- Without a purchased code-signing certificate, Windows SmartScreen may show an unknown-publisher warning.

## Release gates for v0.8

The v0.8 tag and installer must not be published as verified until all are green:

1. Python compile and automated tests.
2. QML lint.
3. PyInstaller Windows one-folder build.
4. Inno Setup v0.8 installer build with the fixed AppId.
5. Silent upgrade/install and installed EXE launch.
6. 100% and 125% DPI screenshots of Home, Image Studio, Automation and Settings.
7. Logo verification on opening screen, window, EXE, taskbar, shortcut and installer.
8. Manual Dell Latitude 7490 test for resizing, battery/charger, hotkey and safe commands.
9. SHA-256 file published beside the installer.

## PC requirements

For the final packaged Core, the owner normally installs only the v0.8 Setup EXE. Python, VS Code, Git and Visual Studio are development tools, not runtime requirements. The exact optional Local Brain/Voice/OCR pack prerequisites must be published only after those packs pass Windows validation.

