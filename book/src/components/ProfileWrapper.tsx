// src/components/ProfileWrapper.tsx
import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import Profile from './Profile';

const ProfileWrapper: React.FC = () => {
  return (
    <AuthProvider>
      <Profile />
    </AuthProvider>
  );
};

export default ProfileWrapper;