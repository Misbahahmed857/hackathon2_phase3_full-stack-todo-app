'use client';

import React from 'react';
import { useAuth } from './AuthProvider/AuthProvider';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login'); // Redirect to login if not authenticated
    }
  }, [isAuthenticated, loading, router]);

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  // If authenticated, render the protected content
  if (isAuthenticated) {
    return children;
  }

  // If not authenticated and not loading, return nothing or a redirect message
  return null;
};

export default ProtectedRoute;