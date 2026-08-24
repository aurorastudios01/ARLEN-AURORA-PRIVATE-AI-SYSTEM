@echo off
setlocal EnableExtensions
title ARLEN NEXUS v0.3 - One Click Portable Builder
cd /d "%~dp0"

set "BUILD_ENV=%CD%\.arlen_build_env"
set "BUILD_LOG=%CD%\ARLEN-BUILD-LOG.txt"
set "RELEASE_ROOT=%CD%\release"
set "RELEASE_DIR=%RELEASE_ROOT%\ARLEN-NEXUS-Portable-v0.3"
set "DIST_DIR=%CD%\dist\ARLEN NEXUS Portable"

echo ============================================================
echo            ARLEN NEXUS v0.3 PORTABLE BUILDER
echo ============================================================
echo.
echo This does not install an editor, Visual Studio, Node or Rust.
echo Build components stay inside this ARLEN project folder.
echo Internet and around 2 GB free disk space are required.
echo.
pause

echo [1/7] Checking Python...
python --version >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto no_python

echo [2/7] Creating private build environment...
python -m venv "%BUILD_ENV%" >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto failed

echo [3/7] Preparing private build components...
"%BUILD_ENV%\Scripts\python.exe" -m pip install --upgrade pip >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto failed
"%BUILD_ENV%\Scripts\python.exe" -m pip install PySide6 psutil Pillow pypdf pyinstaller pytest >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto failed

echo [4/7] Validating Python source...
"%BUILD_ENV%\Scripts\python.exe" -m py_compile main.py backend.py >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto failed

"%BUILD_ENV%\Scripts\python.exe" -m pytest -q >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto failed

echo [5/7] Building ARLEN NEXUS.exe without a terminal window...
"%BUILD_ENV%\Scripts\python.exe" -m PyInstaller --noconfirm --clean "ARLEN_NEXUS.spec" >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto failed

if not exist "%DIST_DIR%\ARLEN NEXUS.exe" goto missing_exe

echo [6/7] Creating portable release folder...
if not exist "%RELEASE_ROOT%" mkdir "%RELEASE_ROOT%"
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"
robocopy "%DIST_DIR%" "%RELEASE_DIR%" /E /NFL /NDL /NJH /NJS /NP >> "%BUILD_LOG%" 2>&1
if errorlevel 8 goto failed
copy /y "PORTABLE_RELEASE_CHECKLIST.md" "%RELEASE_DIR%\PORTABLE_RELEASE_CHECKLIST.md" >nul

echo [7/7] Creating ZIP and cleaning private build files...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$zip='%RELEASE_ROOT%\ARLEN-NEXUS-Portable-v0.3.zip'; if(Test-Path $zip){Remove-Item $zip -Force}; Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath $zip -CompressionLevel Optimal" >> "%BUILD_LOG%" 2>&1
if errorlevel 1 goto failed

rmdir /s /q "%BUILD_ENV%"

echo.
echo ============================================================
echo BUILD COMPLETED
echo ============================================================
echo Portable folder:
echo %RELEASE_DIR%
echo.
echo Start this file:
echo %RELEASE_DIR%\ARLEN NEXUS.exe
echo.
echo ZIP:
echo %RELEASE_ROOT%\ARLEN-NEXUS-Portable-v0.3.zip
echo.
echo Do not delete ARLEN-BUILD-LOG.txt until the app is tested.
start "" "%RELEASE_DIR%"
pause
exit /b 0

:no_python
echo.
echo Python was not found. Your earlier screenshot showed Python installed,
echo so first restart Windows and run this builder again.
goto show_log

:missing_exe
echo.
echo Build finished but ARLEN NEXUS.exe was not found.
goto show_log

:failed
echo.
echo The portable build stopped safely. No system-wide app was installed.

:show_log
echo Send ARLEN-BUILD-LOG.txt for diagnosis:
echo %BUILD_LOG%
pause
exit /b 1
