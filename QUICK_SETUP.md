# 🚀 QUICK SETUP GUIDE - AI Chatbot

Get your local AI chatbot running in 10 minutes!

## System Requirements
- **Node.js** 16+ - [Download](https://nodejs.org)
- **Python** 3.8+ - [Download](https://www.python.org)
- **Ollama** - [Download](https://ollama.ai)
- **RAM**: 8GB minimum (16GB recommended)

---

## Step 1: Install & Start Ollama (3 min)

1. Download and install **Ollama** from https://ollama.ai
2. Start the Ollama service
3. Open terminal and pull a model:

```bash
# Recommended - Fast & Good Quality
ollama pull mistral

# Alternatives:
ollama pull neural-chat    # Smaller & faster
ollama pull llama2         # Larger & slower
```

✅ Verify it's running:
```bash
curl http://localhost:11434/api/tags
```

---

## Step 2: Start Backend Server (2 min)

```bash
cd ai-chatbot-app/backend

# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is ready at **http://localhost:8000**

---

## Step 3: Start Frontend (2 min)

Open **another terminal** and run:

```bash
cd ai-chatbot-app/frontend

npm install
npm run dev
```

**Expected output:**
```
VITE v5.0.8  ready in 123 ms
➜  Local: http://localhost:5173/
```

✅ Frontend is ready at **http://localhost:5173**

---

## Step 4: Start Chatting! 🎉

Visit http://localhost:5173 and start chatting!

---

## Quick Start Scripts (Optional)

### On Mac/Linux
```bash
cd ai-chatbot-app
chmod +x start.sh
./start.sh
```

### On Windows
```bash
cd ai-chatbot-app
start.bat
```

---

## Troubleshooting

### ❌ "Ollama not running"
- Make sure Ollama is installed and started
- Check: `curl http://localhost:11434/api/tags`
- Restart Ollama if needed

### ❌ "Port 8000 already in use"
```bash
# Change backend port in backend/main.py
API_PORT=8001  # Change to different port
```

### ❌ "Port 5173 already in use"
```bash
# Vite will automatically use next available port
# Or change in frontend/vite.config.js
```

### ❌ "Module not found" errors
```bash
# Reinstall dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### ❌ Slow responses
- Ollama uses CPU by default
- For GPU acceleration, check Ollama docs
- First response is slower (model loading)

---

## Next Steps

### To Deploy to Cloud
See **DEPLOYMENT.md** for:
- Docker setup
- AWS deployment
- Heroku setup
- DigitalOcean VPS

### To Build Mobile App
See **MOBILE_SETUP.md** for:
- React Native setup
- iOS/Android deployment
- Share same backend API

### To Customize
- Change model: Edit `backend/main.py` → `OLLAMA_MODEL`
- Customize UI: Edit CSS in `frontend/src/styles/`
- Add features: Extend API in `backend/main.py`

---

## Key Features Included

✅ **Local-first** - Everything runs on your device
✅ **Memory system** - Uses ChromaDB for intelligent context
✅ **Privacy** - No data sent to cloud
✅ **Free** - No API costs ($0 vs $5-50/month with ChatGPT)
✅ **Beautiful UI** - Modern, responsive design
✅ **Easy to modify** - Well-commented code

---

## File Structure

```
ai-chatbot-app/
├── backend/
│   ├── main.py              ← FastAPI server
│   ├── requirements.txt
│   └── chroma_data/         ← Local memory storage
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/      ← Chat UI components
│   │   └── styles/
│   ├── package.json
│   └── vite.config.js
├── start.sh / start.bat      ← Quick start scripts
├── README.md
├── QUICK_SETUP.md           ← You are here
├── MOBILE_SETUP.md
└── DEPLOYMENT.md
```

---

## Getting Help

1. Check **Troubleshooting** section above
2. Check **Ollama docs**: https://ollama.ai
3. Check **FastAPI docs**: https://fastapi.tiangolo.com
4. Check **React docs**: https://react.dev

---

**Happy chatting! 🚀**
