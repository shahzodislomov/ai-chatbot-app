@echo off
echo.
echo 🤖 AI Chatbot - Quick Start
echo ===========================
echo.

REM Check if Ollama is running
echo Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama not running!
    echo Please start Ollama first:
    echo   - Download from https://ollama.ai
    echo   - Run: ollama pull mistral
    echo   - Start the service
    pause
    exit /b 1
)
echo ✅ Ollama is running
echo.

REM Start backend
echo Starting backend...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
start "Backend" python main.py
cd ..

timeout /t 2 /nobreak

REM Start frontend
echo Starting frontend...
cd frontend
if not exist node_modules (
    npm install -q
)
start "Frontend" npm run dev
cd ..

echo.
echo 🚀 App is starting!
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo.
echo Close the windows to stop
echo.
pause
