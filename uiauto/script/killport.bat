@echo off
set port=%1
setlocal enabledelayedexpansion
for /f "delims=  tokens=1" %%i in ('netstat -aon ^| findstr %port%') do (
set a=%%i
goto js
)
:js
taskkill /F /pid "!a:~71,5!"
pause>nul