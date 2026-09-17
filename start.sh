#!/bin/bash

echo "🤖 AI Chatbot - Quick Start"
echo "=========================="
echo ""

# Check if Ollama is running
echo "Checking Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama not running!"
    echo "Please start Ollama first:"
    echo "  - Download from https://ollama.ai"
    echo "  - Run: ollama pull mistral"
    echo "  - Start the service"
    exit 1
fi
echo "✅ Ollama is running"
echo ""

# Start backend
echo "Starting backend..."
cd backend
python -m venv venv 2>/dev/null || true
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
pip install -q -r requirements.txt 2>/dev/null || true
python main.py &
BACKEND_PID=$!
cd ..

sleep 2

# Start frontend
echo "Starting frontend..."
cd frontend
npm install -q > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🚀 App is starting!"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Wait for both processes
wait
