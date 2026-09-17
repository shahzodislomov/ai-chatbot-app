import uuid
from datetime import datetime
from typing import List
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import chromadb
from chromadb.config import Settings

from config import API_HOST, API_PORT, CORS_ORIGINS, OLLAMA_BASE_URL, OLLAMA_MODEL

DB_PATH = "./chroma_data"

# FastAPI Setup
app = FastAPI(title="AI Chatbot API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(CORS_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Setup
Base = declarative_base()
DATABASE_URL = "sqlite:///./chatbot.db"

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    session_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ChromaDB Setup
Path(DB_PATH).mkdir(exist_ok=True)
chroma_settings = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=DB_PATH,
    anonymized_telemetry=False,
)
chroma_client = chromadb.Client(chroma_settings)

try:
    memory_collection = chroma_client.get_collection("chat_memory")
except Exception:
    memory_collection = chroma_client.create_collection(
        name="chat_memory",
        metadata={"hnsw:space": "cosine"}
    )

# Pydantic Models
class ChatMessageRequest(BaseModel):
    session_id: str
    message: str

class SessionResponse(BaseModel):
    session_id: str

class ChatResponse(BaseModel):
    response: str

class ConversationHistory(BaseModel):
    messages: List[dict]

# Utilities
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def call_ollama(prompt: str, context: str = "") -> str:
    """Call Ollama LLM with optional context"""
    full_prompt = f"""You are a helpful AI assistant.

{f'Previous context: {context}' if context else ''}

User: {prompt}
Assistant:"""

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=300,
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        return f"Error calling Ollama: {str(e)}"

def retrieve_context(query: str, limit: int = 3) -> str:
    """Retrieve relevant context from memory using ChromaDB"""
    try:
        results = memory_collection.query(
            query_texts=[query],
            n_results=limit,
        )

        if results and results["documents"]:
            return "\n".join(results["documents"][0])
        return ""
    except Exception:
        return ""

def store_memory(session_id: str, message: str, response: str):
    """Store conversation in vector database for future retrieval"""
    try:
        memory_id = str(uuid.uuid4())
        memory_text = f"Session {session_id}: User said '{message}', Assistant replied '{response}'"
        memory_collection.add(
            ids=[memory_id],
            documents=[memory_text],
            metadatas=[{"session_id": session_id, "timestamp": datetime.utcnow().isoformat()}],
        )
    except Exception as e:
        print(f"Error storing memory: {e}")

# Routes
@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model": OLLAMA_MODEL}

@app.post("/api/chat/session", response_model=SessionResponse)
def create_session(db: Session = None):
    """Create a new chat session"""
    db = SessionLocal()
    session_id = str(uuid.uuid4())

    session = ChatSession(session_id=session_id)
    db.add(session)
    db.commit()
    db.close()

    return {"session_id": session_id}

@app.post("/api/chat/message", response_model=ChatResponse)
def send_message(request: ChatMessageRequest, db: Session = None):
    """Send a message and get a response"""
    db = SessionLocal()

    # Check if session exists
    session = db.query(ChatSession).filter(
        ChatSession.session_id == request.session_id
    ).first()

    if not session:
        db.close()
        raise HTTPException(status_code=404, detail="Session not found")

    # Retrieve context from memory
    context = retrieve_context(request.message)

    # Get response from Ollama
    response = call_ollama(request.message, context)

    # Store messages in database
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=request.session_id,
        role="user",
        content=request.message,
    )
    assistant_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=request.session_id,
        role="assistant",
        content=response,
    )

    db.add(user_msg)
    db.add(assistant_msg)
    db.commit()
    db.close()

    # Store in vector database for RAG
    store_memory(request.session_id, request.message, response)

    return {"response": response}

@app.get("/api/chat/history/{session_id}", response_model=ConversationHistory)
def get_history(session_id: str, db: Session = None):
    """Get conversation history for a session"""
    db = SessionLocal()

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp).all()

    db.close()

    history = []
    for msg in messages:
        if msg.role == "user":
            history.append({"user": msg.content})
        else:
            history.append({"bot": msg.content})

    return {"messages": history}

@app.post("/api/chat/clear-memory")
def clear_memory(db: Session = None):
    """Clear all memory and conversation history"""
    db = SessionLocal()

    # Clear database
    db.query(ChatMessage).delete()
    db.query(ChatSession).delete()
    db.commit()
    db.close()

    # Clear vector database
    try:
        chroma_client.delete_collection("chat_memory")
        global memory_collection
        memory_collection = chroma_client.create_collection(
            name="chat_memory",
            metadata={"hnsw:space": "cosine"}
        )
    except Exception as e:
        print(f"Error clearing memory: {e}")

    return {"message": "Memory cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
