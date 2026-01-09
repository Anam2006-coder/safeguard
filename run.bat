@echo off
echo ========================================
echo        SafeGuard Application
echo ========================================
echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install Flask==2.3.3 Werkzeug==2.3.7

echo.
echo Starting SafeGuard application...
echo.
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py