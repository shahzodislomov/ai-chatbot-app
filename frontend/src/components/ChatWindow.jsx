import React, { useEffect, useRef } from 'react'
import Message from './Message'
import '../styles/ChatWindow.css'

export default function ChatWindow({ messages, loading }) {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="empty-state">
          <h2>Start a conversation</h2>
          <p>Ask me anything, and I'll help!</p>
        </div>
      ) : (
        messages.map((msg, idx) => (
          <Message key={idx} message={msg} />
        ))
      )}

      {loading && (
        <div className="message-container bot">
          <div className="message bot-message typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  )
}
