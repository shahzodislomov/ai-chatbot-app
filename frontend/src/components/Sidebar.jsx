import React from 'react'
import '../styles/Sidebar.css'

export default function Sidebar({ open, onClose, onNewConversation, onClearMemory }) {
  return (
    <>
      {open && <div className="sidebar-overlay" onClick={onClose} />}

      <aside className={`sidebar ${open ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Chatbot</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <nav className="sidebar-nav">
          <button className="nav-btn new-chat" onClick={onNewConversation}>
            + New Chat
          </button>

          <button className="nav-btn danger" onClick={onClearMemory}>
            🗑️ Clear Memory
          </button>
        </nav>

        <div className="sidebar-footer">
          <p>💡 Running on local Ollama</p>
          <p className="text-sm">No cloud, no tracking, 100% private</p>
        </div>
      </aside>
    </>
  )
}
