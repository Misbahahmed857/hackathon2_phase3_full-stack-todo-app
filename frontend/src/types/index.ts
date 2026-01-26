/**
 * TypeScript interfaces for the task management application
 */

export interface UserSession {
  userId: string;
  token: string;
  expiresAt: Date;
  isLoggedIn: boolean;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskCreate {
  title: string;
  description?: string;
  is_completed?: boolean;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  statusCode?: number;
}

export interface APIRequest {
  url: string;
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface AuthState {
  user: any;
  token: string | null;
  loading: boolean;
  isAuthenticated: boolean;
}