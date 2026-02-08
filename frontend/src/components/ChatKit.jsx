import React, { useState, useEffect, useRef } from 'react';
import ChatAPIClient from '../lib/chat';

const ChatKit = ({ userId }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  // Initialize the API client
  const apiClient = new ChatAPIClient('/api/v1'); // Adjust the base URL as needed

  // Scroll to bottom of messages when they update
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message to UI immediately
      const userMessage = {
        id: Date.now().toString(),
        content: inputValue,
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'text'
      };

      setMessages(prev => [...prev, userMessage]);
      const tempInputValue = inputValue;
      setInputValue('');

      // Send message to backend
      const response = await apiClient.sendMessage(
        userId,
        { content: tempInputValue, role: 'user' },
        conversationId
      );

      if (response.success) {
        // Update conversation ID if new conversation was created
        if (response.conversation_id && !conversationId) {
          setConversationId(response.conversation_id);
        }

        // Add AI response to messages
        const aiMessage = {
          id: response.message.id,
          content: response.message.content,
          role: response.message.role,
          timestamp: response.message.timestamp,
          type: response.message.type
        };

        setMessages(prev => [...prev, aiMessage]);

        // Handle any tool calls if present
        if (response.tool_calls && response.tool_calls.length > 0) {
          console.log('Tool calls received:', response.tool_calls);
          // In a real implementation, you would handle these tool calls
        }
      } else {
        setError(response.error || 'Failed to get response from AI');
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'An error occurred while sending the message');
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h3>Chat</h3>
        {conversationId && <span className="conversation-id">Conversation: {conversationId.substring(0, 8)}...</span>}
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>Start a conversation by sending a message!</p>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.role}`}
              >
                <div className="message-content">
                  <div className="message-text">{message.content}</div>
                  <div className="message-meta">
                    <span className="timestamp">{formatTime(message.timestamp)}</span>
                    <span className="sender">{message.role}</span>
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-content">
                  <div className="message-text">Thinking...</div>
                  <div className="message-meta">
                    <span className="timestamp">{formatTime(new Date().toISOString())}</span>
                    <span className="sender">assistant</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          className="message-input"
        />
        <button type="submit" disabled={!inputValue.trim() || isLoading} className="send-button">
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatKit;