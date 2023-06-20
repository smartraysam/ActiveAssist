@echo off

REM Activate the virtual environment
call  C:\ActiveAssist\venv\Scripts\activate.bat

REM Start the Python script with minimized command prompt
start /min cmd /c "python C:\ActiveAssist\index.py"
