@echo off

REM Set the directory path
set "dest=C:\ActiveAssist"

REM Check if the directory exists
IF NOT EXIST "%dest%" (
    REM Create the directory
    mkdir "%dest%"
    echo Directory created successfully.
) else (
    echo Directory already exists.
)

set "src=%~dp0"

echo Copying folders from %src% to %dest%...
xcopy /E /I "%src%" "%dest%"

echo Starting Python Windows service...
python "%dest%\main.py" install
python "%dest%\main.py" start

echo Configuring automatic startup for the service...
sc config ActiveAssist start=auto

REM Set the path to the batch file
set "batchFilePath=%dest%\settings\setting.bat"

REM Set the path to the shortcut file
set "shortcutPath=%USERPROFILE%\Desktop\ProxySetting.lnk"

REM Set the path to the icon file
set "iconPath=%dest%\assets\setting.ico"

REM Create the shortcut with icon
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcutPath%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%batchFilePath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "%iconPath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"
cscript /nologo "%temp%\CreateShortcut.vbs"
del "%temp%\CreateShortcut.vbs"

echo Installation process completed.

pause
