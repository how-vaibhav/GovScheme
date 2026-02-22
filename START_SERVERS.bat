@echo off
REM Start both Django and RASA servers automatically
REM This batch file is for Windows systems

echo.
echo ====================================================
echo    GOVERNMENT SCHEMES PORTAL - AUTO STARTUP
echo ====================================================
echo.

cd /d "C:\Users\LENOVO\OneDrive\Desktop\GovScheme"

echo Activating Python virtual environment (if exists)...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo Starting servers...
python run_all_servers.py

pause
