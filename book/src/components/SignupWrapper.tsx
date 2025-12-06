// src/components/SignupWrapper.tsx
import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import Signup from './Signup';

const SignupWrapper: React.FC = () => {
  return (
    <AuthProvider>
      <Signup />
    </AuthProvider>
  );
};

export default SignupWrapper;