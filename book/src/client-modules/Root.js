// src/client-modules/Root.js
import React from 'react';
import {AuthProvider} from '../contexts/AuthContext';

// Simple client-side check for Chatbot
function ClientChatbot() {
  if (typeof window === 'undefined') {
    return null;
  }

  // Dynamically import and render the Chatbot
  const Chatbot = require('../components/Chatbot').default;
  return <Chatbot />;
}

// Personalization provider component
function PersonalizationProvider({children}) {
  // In a real implementation, this would wrap content with personalization context
  // For now, we'll just return the children
  return <>{children}</>;
}

export default function Root({children}) {
  return (
    <AuthProvider>
      <PersonalizationProvider>
        {children}
        <ClientChatbot />
      </PersonalizationProvider>
    </AuthProvider>
  );
}