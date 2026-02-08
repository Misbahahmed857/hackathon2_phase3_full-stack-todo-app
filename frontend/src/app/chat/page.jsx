'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatKit from '../../components/ChatKit';

const ChatPage = () => {
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated by looking for token in localStorage
    const token = localStorage.getItem('access_token');
    if (!token) {
      // Redirect to login if not authenticated
      router.push('/login');
      return;
    }

    // Get user info from localStorage or decode from token
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      setUserId(user.id);
    } else {
      // If no user info in localStorage, we could decode the JWT token to get user ID
      // For now, we'll assume the user ID is available somehow
      // You might need to adjust this based on how your auth system stores user info
      try {
        // Decode JWT to get user ID (simple base64 decoding of payload)
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          setUserId(payload.sub || payload.userId || payload.id);
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        router.push('/login');
      }
    }

    setLoading(false);
  }, [router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!userId) {
    return <div>Please log in to access the chat.</div>;
  }

  return (
    <div className="chat-page">
      <h1>Chat Interface</h1>
      <div className="chat-wrapper">
        <ChatKit userId={userId} />
      </div>
    </div>
  );
};

export default ChatPage;