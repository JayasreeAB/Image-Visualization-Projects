@echo off
title Vision Hub Web App
echo ========================================================
echo Starting Vision Hub OpenCV Web Application...
echo ========================================================
cd /d "%~dp0"
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe run_app.py
) else (
    python run_app.py
)
pause
