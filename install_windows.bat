@echo off
title UBO System - Installation
color 0B

echo ============================================
echo   UBO Analysis System - Installation
echo   LH Bank
echo ============================================
echo.

:: Change to script directory
cd /d "%~dp0"

:: Check if Python is installed
echo [STEP 1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed!
    echo.
    echo Please download and install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box:
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python is installed
echo.

:: Upgrade pip
echo [STEP 2/4] Upgrading pip...
python -m pip install --upgrade pip
echo.

:: Install dependencies
echo [STEP 3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

:: Test API connection
echo [STEP 4/4] Testing API connection...
python -c "import requests; r = requests.get('https://enlite.lhb.co.th', timeout=10); print('[OK] API is reachable')" 2>nul
if errorlevel 1 (
    echo [WARNING] Cannot reach API server
    echo Make sure you are connected to VPN
)
echo.

echo ============================================
echo   Installation Complete!
echo ============================================
echo.
echo To start the server:
echo   1. Double-click 'start_server.bat'
echo   2. Open browser to http://localhost:4444
echo.
echo ============================================
pause

