@echo off
rem Double-click this to run Course Buddy on Windows.
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on PATH. Install Python 3 from python.org and try again.
    pause
    exit /b 1
)
python assistant.py
echo.
pause
