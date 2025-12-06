// src/client-modules/Root.js
import React from 'react';
import {AuthProvider} from '../contexts/AuthContext';

// Browser check function
function isBrowser() {
  return typeof window !== 'undefined';
}

// Client-only Chatbot component wrapper
function ClientChatbot() {
  if (!isBrowser()) {
    return null;
  }

  const Chatbot = require('../components/Chatbot').default;
  return <Chatbot />;
}

export default function Root({children}) {
  return (
    <AuthProvider>
      {children}
      <ClientChatbot />
    </AuthProvider>
  );
}