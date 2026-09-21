import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Callable, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

if __package__:
    from .config import API_HOST, API_PORT, CORS_ORIGINS, OLLAMA_MODEL
    from .ollama_client import OllamaServiceError, call_ollama
    from .storage import ApplicationResources, ChatMessage, ChatSession, initialize_resources
else:  # Support running ``python backend/main.py``.
    from config import API_HOST, API_PORT, CORS_ORIGINS, OLLAMA_MODEL
    from ollama_client import OllamaServiceError, call_ollama
    from storage import ApplicationResources, ChatMessage, ChatSession, initialize_resources

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

def get_resources(request: Request) -> ApplicationResources:
    """Return resources owned by the running application lifespan."""
    return request.app.state.resources


def retrieve_context(resources: ApplicationResources, query: str, limit: int = 3) -> str:
    """Retrieve relevant context from memory using ChromaDB"""
    try:
        results = resources.memory_collection.query(
            query_texts=[query],
            n_results=limit,
        )

        if results and results["documents"]:
            return "\n".join(results["documents"][0])
        return ""
    except Exception:
        return ""

def store_memory(resources: ApplicationResources, session_id: str, message: str, response: str):
    """Store conversation in vector database for future retrieval"""
    try:
        memory_id = str(uuid.uuid4())
        memory_text = f"Session {session_id}: User said '{message}', Assistant replied '{response}'"
        resources.memory_collection.add(
            ids=[memory_id],
            documents=[memory_text],
            metadatas=[{"session_id": session_id, "timestamp": datetime.utcnow().isoformat()}],
        )
    except Exception as e:
        print(f"Error storing memory: {e}")

def create_app(
    resource_factory: Callable[[], ApplicationResources] = initialize_resources,
) -> FastAPI:
    """Construct the API without opening databases or creating local files."""

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        resources = resource_factory()
        application.state.resources = resources
        try:
            yield
        finally:
            resources.close()
            del application.state.resources

    application = FastAPI(title="AI Chatbot API", version="1.0.0", lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(CORS_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/api/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "ok", "model": OLLAMA_MODEL}

    @application.post("/api/chat/session", response_model=SessionResponse)
    def create_session(http_request: Request):
        """Create a new chat session."""
        resources = get_resources(http_request)
        db = resources.session_factory()
        try:
            session_id = str(uuid.uuid4())
            db.add(ChatSession(session_id=session_id))
            db.commit()
            return {"session_id": session_id}
        finally:
            db.close()

    @application.post("/api/chat/message", response_model=ChatResponse)
    def send_message(request: ChatMessageRequest, http_request: Request):
        """Send a message and get a response."""
        resources = get_resources(http_request)
        db = resources.session_factory()
        try:
            session = db.query(ChatSession).filter(
                ChatSession.session_id == request.session_id
            ).first()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")

            context = retrieve_context(resources, request.message)
            try:
                response = call_ollama(request.message, context)
            except OllamaServiceError as error:
                raise HTTPException(
                    status_code=503,
                    detail="AI service is temporarily unavailable",
                ) from error

            db.add(
                ChatMessage(
                    id=str(uuid.uuid4()),
                    session_id=request.session_id,
                    role="user",
                    content=request.message,
                )
            )
            db.add(
                ChatMessage(
                    id=str(uuid.uuid4()),
                    session_id=request.session_id,
                    role="assistant",
                    content=response,
                )
            )
            db.commit()
        finally:
            db.close()

        store_memory(resources, request.session_id, request.message, response)
        return {"response": response}

    @application.get("/api/chat/history/{session_id}", response_model=ConversationHistory)
    def get_history(session_id: str, http_request: Request):
        """Get conversation history for a session."""
        resources = get_resources(http_request)
        db = resources.session_factory()
        try:
            messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.timestamp).all()
            history = [
                {"user": message.content} if message.role == "user" else {"bot": message.content}
                for message in messages
            ]
            return {"messages": history}
        finally:
            db.close()

    @application.post("/api/chat/clear-memory")
    def clear_memory(http_request: Request):
        """Clear all memory and conversation history."""
        resources = get_resources(http_request)
        db = resources.session_factory()
        try:
            db.query(ChatMessage).delete()
            db.query(ChatSession).delete()
            db.commit()
        finally:
            db.close()

        try:
            resources.chroma_client.delete_collection("chat_memory")
            resources.memory_collection = resources.chroma_client.create_collection(
                name="chat_memory",
                metadata={"hnsw:space": "cosine"},
            )
        except Exception as error:
            print(f"Error clearing memory: {error}")

        return {"message": "Memory cleared"}

    return application


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
