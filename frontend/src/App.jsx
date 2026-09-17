import React, { useState, useEffect } from 'react'
import axios from 'axios'
import ChatWindow from './components/ChatWindow'
import InputBox from './components/InputBox'
import Sidebar from './components/Sidebar'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sessionId, setSessionId] = useState(null)

  // Initialize session
  useEffect(() => {
    const initSession = async () => {
      try {
        const response = await axios.post(`${API_URL}/api/chat/session`)
        setSessionId(response.data.session_id)
        loadConversation(response.data.session_id)
      } catch (error) {
        console.error('Failed to initialize session:', error)
      }
    }

    initSession()
  }, [])

  const loadConversation = async (session) => {
    try {
      const response = await axios.get(`${API_URL}/api/chat/history/${session}`)
      setMessages(response.data.messages || [])
    } catch (error) {
      console.error('Failed to load conversation:', error)
    }
  }

  const handleSendMessage = async (userMessage) => {
    if (!sessionId) return

    // Add user message to UI
    const newMessages = [...messages, { user: userMessage }]
    setMessages(newMessages)
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/chat/message`, {
        session_id: sessionId,
        message: userMessage,
      })

      // Add bot response
      setMessages([...newMessages, { bot: response.data.response }])
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages([
        ...newMessages,
        { bot: 'Sorry, something went wrong. Please try again.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleNewConversation = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/chat/session`)
      setSessionId(response.data.session_id)
      setMessages([])
      setSidebarOpen(false)
    } catch (error) {
      console.error('Failed to create new conversation:', error)
    }
  }

  const handleClearMemory = async () => {
    if (window.confirm('Are you sure? This will clear all stored memories.')) {
      try {
        await axios.post(`${API_URL}/api/chat/clear-memory`)
        setMessages([])
        alert('Memory cleared!')
      } catch (error) {
        console.error('Failed to clear memory:', error)
      }
    }
  }

  return (
    <div className="app-container">
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewConversation={handleNewConversation}
        onClearMemory={handleClearMemory}
      />

      <div className="main-content">
        <header className="app-header">
          <button
            className="menu-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰
          </button>
          <h1>AI Chatbot</h1>
          <div className="header-spacer" />
        </header>

        <ChatWindow messages={messages} loading={loading} />
        <InputBox onSendMessage={handleSendMessage} disabled={loading} />
      </div>
    </div>
  )
}
