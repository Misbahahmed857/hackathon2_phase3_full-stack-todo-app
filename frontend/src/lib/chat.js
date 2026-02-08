/**
 * Chat API client for the ChatKit integration
 */

class ChatAPIClient {
  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
  }

  /**
   * Send a message to the chat endpoint
   * @param {string} userId - The ID of the user sending the message
   * @param {Object} message - The message to send
   * @param {string} message.content - The content of the message
   * @param {string} [message.role='user'] - The role of the message sender
   * @param {string} [conversationId] - The ID of the conversation (optional, creates new if not provided)
   * @returns {Promise<Object>} The response from the AI agent
   */
  async sendMessage(userId, message, conversationId = null) {
    const token = localStorage.getItem('access_token'); // Assuming JWT token is stored in localStorage

    const response = await fetch(`${this.baseURL}/chat/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        message: message,
        conversation_id: conversationId
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Get conversation history
   * @param {string} userId - The ID of the user
   * @param {string} conversationId - The ID of the conversation
   * @returns {Promise<Object>} The conversation data
   */
  async getConversationHistory(userId, conversationId) {
    const token = localStorage.getItem('access_token');

    const response = await fetch(`${this.baseURL}/chat/${userId}/conversations/${conversationId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Create a new conversation
   * @param {string} userId - The ID of the user
   * @param {string} title - The title of the new conversation
   * @returns {Promise<Object>} The created conversation data
   */
  async createConversation(userId, title = '') {
    const token = localStorage.getItem('access_token');

    const response = await fetch(`${this.baseURL}/chat/${userId}/conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ title })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }
}

export default ChatAPIClient;