@echo off

REM Set up auto-start registry entry
echo Windows Registry Editor Version 5.00 > "%~dp0startup.reg"
echo. >> "%~dp0startup.reg"
echo [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run] >> "%~dp0startup.reg"
echo "ActiveAssistService"="python \"%~dp0index.py\" start" >> "%~dp0startup.reg"
regedit /s "%~dp0startup.reg"
del "%~dp0startup.reg"

REM Start the Windows service
python "%~dp0index.py" start

pause
