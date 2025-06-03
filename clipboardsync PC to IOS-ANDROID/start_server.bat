@echo off
title Clipboard Sharing Server
color 0A

:: Set your working directory
set "WORKDIR=E:\MY APPS\clipboard"

:: Check if already running
tasklist /fi "imagename eq python.exe" /fi "windowtitle eq clipboard_server.py" | find "python.exe" > nul
if %errorlevel% equ 0 (
    echo Server is already running!
    pause
    exit /b
)

:: Change directory
cd /d "%WORKDIR%"

:: Check for required files
if not exist "clipboard_server.py" (
    echo Error: clipboard_server.py not found in %WORKDIR%
    pause
    exit /b
)

if not exist "public\index.html" (
    echo Error: public\index.html not found
    pause
    exit /b
)

:: Start the server
echo Starting Clipboard Sharing Server...
echo Public directory: %WORKDIR%\public
echo.
echo Access on your iPad: http://SIDDHARTHPC.local:3000
echo.
echo NOTE: Both devices must be on the SAME WiFi network!
echo Install Bonjour from Apple if ".local" doesn't work:
echo https://support.apple.com/kb/DL999
echo.
echo Press CTRL+C to stop the server
echo.

python clipboard_server.py

if %errorlevel% neq 0 pause