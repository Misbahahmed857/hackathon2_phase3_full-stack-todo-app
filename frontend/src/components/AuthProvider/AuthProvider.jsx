'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '../../lib/api';

// Create Auth Context
const AuthContext = createContext(null);

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('auth-token');
    if (storedToken) {
      setToken(storedToken);
      // Optionally verify token and fetch user data
      verifyTokenAndFetchUser(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const verifyTokenAndFetchUser = async (token) => {
    try {
      // In a real app, you'd make an API call to verify the token
      // For now, we'll just assume the token is valid and set loading to false
      setLoading(false);
    } catch (error) {
      console.error('Token verification failed:', error);
      logout();
    }
  };

  const login = async (credentials) => {
    try {
      const response = await apiClient.login(credentials);
      const { access_token } = response;

      // Store token
      localStorage.setItem('auth-token', access_token);
      setToken(access_token);

      // Set user data (you might want to fetch user details here)
      setUser({ email: credentials.email });

      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      return { success: false, error: error.message };
    }
  };

  const register = async (userData) => {
    try {
      const response = await apiClient.register(userData);
      return { success: true, data: response };
    } catch (error) {
      console.error('Registration failed:', error);
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('auth-token');
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};