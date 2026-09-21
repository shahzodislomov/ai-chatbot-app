"""Persistence resources initialized only during the application lifespan."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


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


@dataclass
class ApplicationResources:
    """Database and vector-store handles owned by one application instance."""

    engine: Engine
    session_factory: sessionmaker
    chroma_client: object
    memory_collection: object

    def close(self) -> None:
        self.engine.dispose()


def initialize_resources(
    database_url: str = "sqlite:///./chatbot.db",
    chroma_path: str = "./chroma_data",
) -> ApplicationResources:
    """Create persistence resources when FastAPI starts, not when modules import."""
    import chromadb
    from chromadb.config import Settings

    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(database_url, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Path(chroma_path).mkdir(parents=True, exist_ok=True)
    chroma_client = chromadb.Client(
        Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=chroma_path,
            anonymized_telemetry=False,
        )
    )

    try:
        memory_collection = chroma_client.get_collection("chat_memory")
    except Exception:
        memory_collection = chroma_client.create_collection(
            name="chat_memory",
            metadata={"hnsw:space": "cosine"},
        )

    return ApplicationResources(
        engine=engine,
        session_factory=session_factory,
        chroma_client=chroma_client,
        memory_collection=memory_collection,
    )
