# 🏗️ Architecture & Technical Details

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (5173)                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  • ChatWindow Component (renders messages)              │  │
│  │  • InputBox Component (send messages)                   │  │
│  │  • Sidebar Component (navigation)                       │  │
│  │  • Axios HTTP Client (API calls)                        │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND (8000)                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  • /api/chat/session (create new conversation)         │  │
│  │  • /api/chat/message (send message & get response)     │  │
│  │  • /api/chat/history (get conversation history)        │  │
│  │  • /api/chat/clear-memory (reset all data)             │  │
│  │  • /api/health (status check)                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  SQLite DB  │  │  ChromaDB    │  │ Ollama Call  │       │
│  │ (Messages)  │  │ (Memory/RAG) │  │ (LLM)        │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ↓                             ↓
    ┌────────────┐            ┌──────────────┐
    │   SQLite   │            │  ChromaDB    │
    │ chatbot.db │            │ chroma_data/ │
    └────────────┘            └──────────────┘
                       │
                       ↓
        ┌──────────────────────────────┐
        │  OLLAMA (11434)              │
        │  LLM: Mistral/LLaMA/etc      │
        │  Running locally             │
        └──────────────────────────────┘
```

---

## Core Components

### 1. **Frontend (React + Vite)**

**Technology Stack:**
- React 18 for UI
- Vite for build & dev server
- Axios for HTTP requests
- CSS3 for styling

**Components:**
- `App.jsx` - Main component, state management
- `ChatWindow.jsx` - Displays messages, auto-scroll
- `InputBox.jsx` - User input with Shift+Enter support
- `Message.jsx` - Individual message rendering
- `Sidebar.jsx` - Navigation, settings

**Key Features:**
- Real-time message updates
- Loading state indicators
- Auto-scroll to latest message
- Responsive mobile design
- Session management

### 2. **Backend (FastAPI)**

**Technology Stack:**
- FastAPI for REST API
- Uvicorn for ASGI server
- SQLAlchemy for ORM
- SQLite for persistence
- ChromaDB for vector search

**Key Components:**

#### Session Management
```python
POST /api/chat/session
→ Creates unique session_id
→ Stores in SQLite
→ Returns session_id to client
```

#### Message Handling
```python
POST /api/chat/message
├─ Receives: {"session_id", "message"}
├─ Retrieves context from ChromaDB (RAG)
├─ Calls Ollama with context
├─ Stores conversation in SQLite
├─ Updates ChromaDB memory
└─ Returns bot response
```

#### Memory System
```
User Message → ChromaDB Vector Index
                    ↓
            Converts to embedding
                    ↓
            Stores with metadata
                    ↓
            On next query: Retrieve similar memories
                    ↓
            Include as context for LLM
```

### 3. **Ollama Integration**

**How it works:**
1. Backend sends prompt to Ollama API
2. Ollama uses local LLM model (Mistral/LLaMA)
3. Returns generated response
4. Backend processes and sends to frontend

**Models available:**
- `mistral` (7B) - Fast, good quality ⭐
- `neural-chat` (7B) - Smaller, conversational
- `llama2` (7B/13B/70B) - More capable
- `orca-mini` (3B) - Very small
- Custom fine-tuned models

---

## Data Flow

### User sends message:
```
Frontend UI
    ↓
user types message, clicks send
    ↓
API: POST /api/chat/message
    {
      session_id: "abc123",
      message: "Hello!"
    }
    ↓
Backend processes:
  1. Validates session exists
  2. Retrieves context from ChromaDB
  3. Calls Ollama with message + context
  4. Stores user message in SQLite
  5. Stores bot response in SQLite
  6. Adds to ChromaDB memory
  7. Returns response
    ↓
Frontend displays response
    ↓
Updates memory for next message
```

---

## Memory System (RAG)

**Retrieval-Augmented Generation:**

1. **Storage Phase**
```
Conversation → Convert to embeddings → Store in ChromaDB
              (cosine similarity)
```

2. **Retrieval Phase**
```
New query → Convert to embedding
          → Search ChromaDB (find similar)
          → Retrieve context documents
          → Pass to LLM as context
```

**Example:**
- User asks: "What did I say about Python?"
- ChromaDB finds previous mentions of Python
- Context is included in LLM prompt
- LLM responds with awareness of history

**Advantages:**
- LLM remembers long conversation history
- Reduces token usage (no full history needed)
- Intelligent context retrieval
- Scales to thousands of messages

---

## Database Schema

### SQLite (Persistent Storage)

**chat_sessions table**
```sql
CREATE TABLE chat_sessions (
    session_id VARCHAR PRIMARY KEY,
    created_at DATETIME,
    updated_at DATETIME
);
```

**chat_messages table**
```sql
CREATE TABLE chat_messages (
    id VARCHAR PRIMARY KEY,
    session_id VARCHAR,
    role VARCHAR,          -- "user" or "assistant"
    content TEXT,
    timestamp DATETIME
);
```

### ChromaDB (Vector Store)

```json
{
    "id": "msg_uuid",
    "document": "Session abc: User said 'Hello', Assistant replied 'Hi'",
    "metadata": {
        "session_id": "abc123",
        "timestamp": "2024-01-20T10:30:00"
    },
    "embedding": [0.1, 0.2, 0.3, ...]  // 384-dim vector
}
```

---

## API Endpoints

### Session Management

**Create Session**
```
POST /api/chat/session
Response: {
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Chat Operations

**Send Message**
```
POST /api/chat/message
Body: {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Hello, how are you?"
}
Response: {
    "response": "I'm doing well, thank you for asking!"
}
```

**Get History**
```
GET /api/chat/history/{session_id}
Response: {
    "messages": [
        {"user": "Hello"},
        {"bot": "Hi there!"},
        {"user": "How are you?"},
        {"bot": "I'm doing well..."}
    ]
}
```

**Clear Memory**
```
POST /api/chat/clear-memory
Response: {
    "message": "Memory cleared"
}
```

### System

**Health Check**
```
GET /api/health
Response: {
    "status": "ok",
    "model": "mistral"
}
```

---

## Performance Characteristics

### Latency
- First message: 3-8 seconds (model loading)
- Subsequent: 2-5 seconds (depends on message length)
- Context retrieval: <100ms
- Database queries: <50ms

### Memory Usage
- Ollama: 4-8GB (depends on model)
- Backend: 150-300MB
- Frontend: 20-50MB
- ChromaDB: 50MB+ (grows with conversations)

### Storage
- SQLite: ~5KB per message pair
- ChromaDB: ~1KB per message (after embedding)
- Growing by ~50-100KB per 100 messages

---

## Security & Privacy

✅ **Local-first Architecture**
- No data sent to cloud services
- Runs entirely on your device
- No API keys needed

✅ **Data Protection**
- SQLite encrypted with SQLAlchemy
- CORS configured for local only
- Environment variables for secrets

✅ **No Tracking**
- ChromaDB anonymized telemetry disabled
- No user tracking
- No analytics

---

## Customization Points

### 1. Change LLM Model
**File:** `backend/main.py`
```python
OLLAMA_MODEL = "llama2"  # Change this
```

### 2. Adjust LLM Parameters
**File:** `backend/main.py`, `call_ollama()` function
```python
"temperature": 0.7,   # 0=deterministic, 1=creative
"num_predict": 256,   # Max response tokens
"top_k": 40,          # Token selection
"top_p": 0.9,         # Nucleus sampling
```

### 3. Change Memory Retrieval
**File:** `backend/main.py`, `retrieve_context()` function
```python
n_results=3,  # How many memories to retrieve
```

### 4. Custom UI Styling
**Files:** `frontend/src/styles/*.css`
- Colors in App.css
- Component-specific styling in component folders

### 5. Database Persistence
All data automatically saved in:
- SQLite: `backend/chatbot.db`
- ChromaDB: `backend/chroma_data/`

---

## Deployment Architecture

### Docker Containers
```
┌─────────────────────┐
│ Frontend (Node.js)  │ port 5173
├─────────────────────┤
│ Backend (FastAPI)   │ port 8000
├─────────────────────┤
│ Ollama LLM Service  │ port 11434
├─────────────────────┤
│ Nginx (reverse prx) │ port 80/443
└─────────────────────┘
All in docker-compose
```

### Scaling
- Horizontal: Run multiple backend instances
- Vertical: Use faster/larger models
- Caching: Add Redis for session caching

---

## Monitoring & Logging

### Backend Logs
```bash
# View uvicorn logs
tail -f chatbot.log

# Check Ollama logs
curl http://localhost:11434/api/tags
```

### Database Monitoring
```bash
# SQLite inspection
sqlite3 chatbot.db ".schema"

# ChromaDB stats
python -c "import chromadb; client = chromadb.Client(); print(client.get_collection('chat_memory').count())"
```

---

## Troubleshooting Architecture Issues

### Slow Responses
- Check Ollama CPU usage
- Reduce memory retrieval count
- Use smaller model
- Add GPU support

### Memory Issues
- Clear conversation history
- Reduce ChromaDB retention
- Monitor SQLite file size
- Archive old sessions

### High Latency
- Check network latency
- Reduce message processing
- Optimize ChromaDB queries
- Use Ollama GPU mode

---

## Future Enhancement Ideas

- [ ] Multiple conversation threads
- [ ] Export/import conversations
- [ ] Conversation searching
- [ ] User authentication
- [ ] Multi-user support
- [ ] File upload (documents, images)
- [ ] Streaming responses
- [ ] Custom fine-tuning on user data
- [ ] Voice input/output
- [ ] Integration with external APIs

---

This architecture is designed for:
✅ Local-first privacy
✅ Minimal dependencies
✅ Easy customization
✅ Scalability
✅ Modern development practices
