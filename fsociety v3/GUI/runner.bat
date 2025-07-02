@echo off
title Installing FsocietyV3 Requirements
color 0A


:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not added to PATH.
    echo     Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

:: Check if pip is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] pip is not installed or not added to PATH.
    echo     You can reinstall Python and make sure to check the box:
    echo     [Add Python to PATH] during installation.
    pause
    exit /b
)

echo [+] Installing required Python packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [!] Failed to install required packages. Check the error above.
    pause
    exit /b
)

echo [+] Starting FsocietyV3...
python FsocietyDDoS.py
pause
