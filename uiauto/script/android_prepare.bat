@echo off
taskkill /F /im node.exe
taskkill /F /im adb.exe
adb kill-server
ping 127.0.0.1 -n  2 >NUL
adb start-server
ping 127.0.0.1 -n  2 >NUL