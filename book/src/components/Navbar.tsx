// src/components/Navbar.tsx
import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import Link from '@docusaurus/Link';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    window.location.href = '/'; // Redirect to home after logout
  };

  return (
    <nav style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center', 
      padding: '1rem',
      backgroundColor: '#f5f5f5',
      marginBottom: '2rem'
    }}>
      <div>
        <Link to="/" style={{ fontWeight: 'bold', textDecoration: 'none', color: '#333' }}>
          AI Robotics Textbook
        </Link>
      </div>
      <div>
        {isAuthenticated ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span>Welcome, {user?.email}</span>
            <Link to="/profile" style={{ marginRight: '1rem', textDecoration: 'none', color: '#007acc' }}>
              Profile
            </Link>
            <button 
              onClick={handleLogout}
              style={{ 
                padding: '0.5rem 1rem', 
                backgroundColor: '#007acc', 
                color: 'white', 
                border: 'none', 
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '1rem' }}>
            <Link 
              to="/login" 
              style={{ 
                textDecoration: 'none', 
                color: '#007acc',
                padding: '0.5rem 1rem',
                border: '1px solid #007acc',
                borderRadius: '4px'
              }}
            >
              Login
            </Link>
            <Link 
              to="/signup" 
              style={{ 
                textDecoration: 'none', 
                color: 'white',
                backgroundColor: '#007acc',
                padding: '0.5rem 1rem',
                borderRadius: '4px'
              }}
            >
              Sign Up
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;