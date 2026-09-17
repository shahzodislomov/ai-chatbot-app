# 🤖 AI Chatbot App

A **completely local, free, open-source AI chatbot** powered by Ollama. No API costs, no tracking, 100% private.

## Features

✅ **Local LLM** - Runs on your machine (Ollama)
✅ **Memory System** - Remembers conversations with ChromaDB
✅ **Vector Search** - Intelligent context retrieval
✅ **Privacy First** - Everything stays on your device
✅ **Beautiful UI** - Modern React interface
✅ **Responsive** - Works on desktop and mobile
✅ **Easy Setup** - No complex configuration

---

## Quick Start (5 minutes)

### Prerequisites
- **Node.js** 16+ ([download](https://nodejs.org))
- **Python** 3.8+ ([download](https://www.python.org/downloads/))
- **Ollama** ([download](https://ollama.ai))

### 1. Install & Run Ollama

```bash
# Download from https://ollama.ai
# Install and start Ollama
# Then pull a model (choose one):

ollama pull mistral      # Fast, good quality (recommended)
ollama pull neural-chat  # Smaller model
ollama pull llama2       # Larger, slower
```

Verify it's running:
```bash
curl http://localhost:11434/api/tags
```

### 2. Start Backend

```bash
cd ai-chatbot-app/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Backend runs on: **http://localhost:8000**

Browser access is restricted to `http://localhost:5173` by default. Set `CORS_ORIGINS` to a comma-separated list of explicit `http://` or `https://` origins for other deployments; wildcard origins are rejected while credentials are enabled.

### 3. Start Frontend

```bash
cd ai-chatbot-app/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend opens at: **http://localhost:5173**

### 4. Done! 🎉

Start chatting! The app will:
- Remember conversations
- Store everything locally
- Never send data to the cloud

---

## Project Structure

```
ai-chatbot-app/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt      # Python dependencies
│   └── chroma_data/          # Local memory database
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── components/       # React components
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── InputBox.jsx
│   │   │   ├── Message.jsx
│   │   │   └── Sidebar.jsx
│   │   └── styles/           # Component styles
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send a message |
| `GET` | `/conversation/{id}/{user_id}` | Get conversation history |
| `DELETE` | `/conversation/{id}/{user_id}` | Delete conversation |
| `POST` | `/clear-memory/{user_id}` | Clear all memory |
| `GET` | `/models` | List available models |

**Example request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello!",
    "user_id": "user123",
    "conversation_id": "conv123"
  }'
```

---

## Customization

### Change the Model

Edit `backend/main.py`:
```python
OLLAMA_MODEL = "neural-chat"  # Change this
```

Then restart the backend.

### Adjust Response Length

In `backend/main.py`:
```python
options={
    "num_predict": 256,      # Max tokens (increase for longer responses)
    "temperature": 0.7,      # 0-1: Lower = more focused, Higher = more creative
}
```

### Style the UI

Edit CSS files in `frontend/src/styles/` to customize colors, fonts, etc.

---

## Mobile App Setup (React Native)

### Option 1: React Native (Best)

```bash
# Install Expo CLI
npm install -g expo-cli

# Create new React Native project
expo init chatbot-mobile
cd chatbot-mobile

# Copy backend API logic to mobile
# Use same API endpoints from mobile app

expo start
```

### Option 2: Tauri (Desktop → Mobile)

```bash
# Install Tauri CLI
cargo install tauri-cli

# Convert web app to desktop/mobile app
cargo tauri init
cargo tauri dev
```

### Option 3: Capacitor (React → iOS/Android)

```bash
# Install Capacitor
npm install @capacitor/core @capacitor/cli

# Add iOS/Android
npx cap add ios
npx cap add android

# Build and deploy
npm run build
npx cap sync
```

### Option 4: Electron (Desktop App)

```bash
# Install Electron
npm install electron --save-dev

# Create main.js (Electron entry point)
# Package as standalone desktop app
npm run electron
```

---

## Memory System Explained

The app uses **ChromaDB** for intelligent memory:

1. **User sends message** → "What's 2+2?"
2. **Vector embedding created** → Converts text to numbers
3. **Search relevant past conversations** → Finds similar questions
4. **Include context in prompt** → "User previously asked about math..."
5. **Bot responds with context** → Smarter, more consistent answers

This means the bot learns from your conversation patterns!

---

## Performance Tips

- **Smaller model** = Faster responses (neural-chat, mistral)
- **Larger model** = Better quality (llama2, mistral-large)
- **GPU support**: Install CUDA for 10x faster responses
  ```bash
  # On Windows/Linux with NVIDIA GPU
  ollama pull mistral
  # Ollama auto-detects CUDA
  ```

---

## Troubleshooting

**Error: "Connection refused" (Ollama not running)**
```bash
# Make sure Ollama is running
ollama serve

# Or check if it's running in background
ps aux | grep ollama
```

**Error: "Model not found"**
```bash
# Pull a model first
ollama pull mistral
```

**Slow responses**
- Use smaller model: `ollama pull neural-chat`
- Add GPU (NVIDIA/AMD)
- Increase RAM allocation

**Frontend can't connect to backend**
- Check backend is running: `curl http://localhost:8000`
- Check CORS settings in `backend/main.py`
- Use same API URL in frontend

---

## Deployment

### Deploy Backend (Free Options)

**Option 1: Railway.app** (Free tier available)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Option 2: Render.com**
- Connect GitHub repo
- Auto-deploys on push
- Free tier available

**Option 3: Hugging Face Spaces**
- Upload code
- Auto-deploys with GPU options

### Deploy Frontend (Free Options)

**Vercel** (Recommended)
```bash
npm install -g vercel
vercel
```

**Netlify**
```bash
npm install -g netlify-cli
netlify deploy
```

---

## Contributing

Have ideas? Found a bug? Feel free to:
1. Open an issue
2. Submit a pull request
3. Suggest features

---

## License

MIT - Use freely in personal/commercial projects

---

## Free Alternatives to Paid AI

| Service | Cost | Our App |
|---------|------|---------|
| ChatGPT | $20/month | $0 |
| Claude | $20/month | $0 |
| Gemini | Free-$20 | Free |
| **Ollama** | **Free** | ✅ |

Save **$240+/year** with this setup! 💰

---

## Next Steps

- ✅ Build a mobile app with React Native
- ✅ Add voice input/output
- ✅ Fine-tune model on custom data
- ✅ Deploy to cloud with GPU
- ✅ Add multiple user support
- ✅ Create custom system prompts

---

## Support

Having issues?
1. Check [Ollama docs](https://github.com/ollama/ollama)
2. Check [FastAPI docs](https://fastapi.tiangolo.com)
3. Check [React docs](https://react.dev)

Happy chatting! 🚀
