@echo off

REM Set the directory path
set "dest=C:\ActiveAssist"
set "src=%~dp0"

echo Checking if Python is installed...
REM Install Python
echo Installing Python...
"%src%\packages\python-installer.exe" /wait /quiet /passive PrependPath=1 AppendPath=1 Include_exe=1 Include_tcltk=1 Include_pip=1 Include_lib=1

REM Check the installation status
python --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python installation completed successfully.
) else (
    echo Python installation failed, please install it manually.
)
 

REM Check if the directory exists
IF NOT EXIST "%dest%" (
    REM Create the directory
    mkdir "%dest%"
    echo Directory created successfully.
) else (
    echo Directory already exists.
)

echo Copying folders from %src% to %dest%...
xcopy /E /I "%src%" "%dest%"

echo Installing Python packages from requirements file...
"python.exe" -m pip install -r "%src%\requirements.txt"


echo Starting Python Windows service...
"python.exe" "%dest%\main.py" install
"python.exe" "%dest%\main.py" start

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
