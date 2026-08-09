@echo off
cd /d "%~dp0backend"
echo Installing dependencies (only needed the first time)...
pip install -r requirements.txt
echo.
echo Starting GATECHECK server...
echo.
echo Once you see "Running on http://127.0.0.1:5000", open this in your browser:
echo     http://127.0.0.1:5000
echo.
python app.py
pause
