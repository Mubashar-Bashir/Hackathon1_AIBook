import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import UserDashboard from '../components/UserDashboard';

// Create a client-only component that delays auth access until after mount
function DashboardPage() {
  const [authState, setAuthState] = useState({
    user: null,
    isAuthenticated: false,
    loading: true
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    // Only run on client-side
    if (typeof window === 'undefined') {
      // During SSR, set initial state that won't cause errors
      setAuthState({
        user: null,
        isAuthenticated: false,
        loading: false
      });
      return;
    }

    // On client-side, try to access auth context
    let authModule;
    try {
      // Dynamically import the auth context module
      authModule = require('../contexts/AuthContext');
    } catch (err) {
      console.error('Failed to load auth module:', err);
      setError(err.message);
      setAuthState({
        user: null,
        isAuthenticated: false,
        loading: false
      });
      return;
    }

    try {
      // Access the auth hook
      const auth = authModule.useAuth();
      setAuthState({
        user: auth.user,
        isAuthenticated: auth.isAuthenticated,
        loading: auth.loading
      });
    } catch (err) {
      console.error('Error accessing auth context:', err);
      setError(err.message);
      setAuthState({
        user: null,
        isAuthenticated: false,
        loading: false
      });
    }
  }, []);

  const { user, isAuthenticated, loading } = authState;

  if (loading) {
    return (
      <Layout title="Loading" description="Loading dashboard...">
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <p>Loading...</p>
        </div>
      </Layout>
    );
  }

  if (error || !isAuthenticated) {
    // Redirect to login if not authenticated or if there's an error
    if (typeof window !== 'undefined' && (!isAuthenticated || error)) {
      window.location.href = '/login';
    }
    return null;
  }

  return (
    <Layout title="User Dashboard" description="Your personalized learning dashboard">
      <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <h1>Welcome, {user?.name || user?.email || 'User'}!</h1>
        <p>Your personalized learning dashboard</p>

        <UserDashboard />
      </div>
    </Layout>
  );
}

export default DashboardPage;