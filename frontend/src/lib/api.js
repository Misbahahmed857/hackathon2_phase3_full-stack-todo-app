/**
 * Centralized API client with JWT handling for the task management application
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Creates a request configuration with JWT token
   */
  async createRequestConfig(method = 'GET', body = null, customHeaders = {}) {
    // Get token from wherever it's stored (localStorage, cookies, etc.)
    const token = await this.getToken();

    const headers = {
      'Content-Type': 'application/json',
      ...customHeaders,
    };

    // Add authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      method,
      headers,
    };

    if (body !== null) {
      config.body = JSON.stringify(body);
    }

    return config;
  }

  /**
   * Gets the JWT token from storage
   */
  async getToken() {
    // In a real app, this might come from a cookie, localStorage, or auth provider
    if (typeof window !== 'undefined') {
      // Client-side
      return localStorage.getItem('auth-token');
    }
    // Server-side would need different implementation
    return null;
  }

  /**
   * Makes an API request
   */
  async request(endpoint, method = 'GET', data = null, customHeaders = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = await this.createRequestConfig(method, data, customHeaders);

    try {
      const response = await fetch(url, config);
      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || `HTTP error! status: ${response.status}`);
      }

      return responseData;
    } catch (error) {
      console.error(`API request failed: ${method} ${endpoint}`, error);
      throw error;
    }
  }

  // Authentication methods
  async login(credentials) {
    return this.request('/api/v1/auth/login', 'POST', credentials);
  }

  async register(userData) {
    return this.request('/api/v1/auth/register', 'POST', userData);
  }

  // Task methods
  async getTasks() {
    return this.request('/api/v1/tasks', 'GET');
  }

  async createTask(taskData) {
    return this.request('/api/v1/tasks', 'POST', taskData);
  }

  async getTaskById(taskId) {
    return this.request(`/api/v1/tasks/${taskId}`, 'GET');
  }

  async updateTask(taskId, taskData) {
    return this.request(`/api/v1/tasks/${taskId}`, 'PUT', taskData);
  }

  async patchTask(taskId, taskData) {
    return this.request(`/api/v1/tasks/${taskId}`, 'PATCH', taskData);
  }

  async deleteTask(taskId) {
    return this.request(`/api/v1/tasks/${taskId}`, 'DELETE');
  }
}

export const apiClient = new ApiClient();

// Export individual methods for convenience
export const {
  login,
  register,
  getTasks,
  createTask,
  getTaskById,
  updateTask,
  patchTask,
  deleteTask
} = apiClient;