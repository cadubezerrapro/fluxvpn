@echo off
title FLUX VPN Desktop
cd /d "%~dp0"

:: Abre como Aplicativo Nativo no Microsoft Edge (Presente em 100% dos Windows 10 e 11)
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app="file://%~dp0index.html" --window-size=1040,700
    exit
)

if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" --app="file://%~dp0index.html" --window-size=1040,700
    exit
)

:: Abre como Aplicativo Nativo no Google Chrome
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app="file://%~dp0index.html" --window-size=1040,700
    exit
)

if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --app="file://%~dp0index.html" --window-size=1040,700
    exit
)

:: Fallback padrao
start "" "%~dp0index.html"
exit
