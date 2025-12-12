import React from 'react';
import Layout from '@theme/Layout';
import UserDashboard from '../components/UserDashboard';
import { useAuth } from '../contexts/AuthContext';

function DashboardPage() {
  const { user, isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <Layout title="Loading" description="Loading dashboard...">
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <p>Loading...</p>
        </div>
      </Layout>
    );
  }

  if (!isAuthenticated) {
    // Redirect to login if not authenticated
    if (typeof window !== 'undefined') {
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