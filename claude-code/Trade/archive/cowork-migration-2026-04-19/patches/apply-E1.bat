@echo off
REM Double-click launcher for apply-E1.ps1
REM Runs the PowerShell script with ExecutionPolicy Bypass and pauses so you can read the output.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0apply-E1.ps1"
echo.
pause
