@echo off
title ARLEN NEXUS Release Builder
cd /d "%~dp0"
echo Controlled Windows release environment only.
echo End users do not run this file or install build tools.
python -m PyInstaller --noconfirm "ARLEN_NEXUS.spec"
if errorlevel 1 goto error
echo Portable build completed. Run PORTABLE_RELEASE_CHECKLIST.md before publishing.
pause
exit /b 0
:error
echo Build failed. Do not publish an end-user ZIP.
pause
exit /b 1
