import React, { useState } from 'react'
import '../styles/InputBox.css'

export default function InputBox({ onSendMessage, disabled }) {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form className="input-box" onSubmit={handleSubmit}>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message... (Shift+Enter for new line)"
        disabled={disabled}
        rows="1"
      />
      <button type="submit" disabled={disabled || !input.trim()}>
        {disabled ? '⏳' : '➤'}
      </button>
    </form>
  )
}
