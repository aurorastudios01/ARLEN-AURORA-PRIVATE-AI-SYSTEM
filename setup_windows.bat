@echo off
title ARLEN NEXUS Setup
cd /d "%~dp0"
echo Installing ARLEN NEXUS core dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto error
echo.
echo Core setup completed.
echo Double-click RUN_ARLEN_SILENT.vbs to launch without a terminal window.
pause
exit /b 0
:error
echo Setup failed. Take a screenshot of this window and send it for support.
pause
exit /b 1

