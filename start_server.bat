@echo off
title UBO Analysis System - LH Bank
color 0A

echo ============================================
echo   UBO Analysis System - LH Bank
echo   Starting Server...
echo ============================================
echo.

:: Change to script directory
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if requirements are installed
echo [INFO] Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo [INFO] Starting UBO Analysis System...
echo [INFO] Server will be available at: http://localhost:4444
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ============================================

:: Start the Flask application
python enhanced_app.py

:: If server stops
echo.
echo [INFO] Server stopped.
pause

