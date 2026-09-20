@echo off
setlocal
cd /d "%~dp0"
title AquaVigil Docker Launcher
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-aquavigil.ps1"
if errorlevel 1 (
  echo.
  echo AquaVigil could not start. Review the message above.
  pause
  exit /b 1
)
echo.
echo AquaVigil is ready. You may close this window.
pause

