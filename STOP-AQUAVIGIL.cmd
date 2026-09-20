@echo off
setlocal
cd /d "%~dp0"
title Stop AquaVigil
docker compose down --remove-orphans
if errorlevel 1 (
  echo.
  echo AquaVigil could not be stopped cleanly.
  pause
  exit /b 1
)
echo.
echo AquaVigil services have stopped.
pause

