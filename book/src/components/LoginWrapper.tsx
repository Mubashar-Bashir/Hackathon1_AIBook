// src/components/LoginWrapper.tsx
import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import Login from './Login';

const LoginWrapper: React.FC = () => {
  return (
    <AuthProvider>
      <Login />
    </AuthProvider>
  );
};

export default LoginWrapper;