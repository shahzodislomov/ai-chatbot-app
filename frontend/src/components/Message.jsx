import React from 'react'
import '../styles/Message.css'

export default function Message({ message }) {
  const isBot = !!message.bot
  const text = message.bot || message.user

  return (
    <div className={`message-container ${isBot ? 'bot' : 'user'}`}>
      <div className={`message ${isBot ? 'bot-message' : 'user-message'}`}>
        {text}
      </div>
    </div>
  )
}
