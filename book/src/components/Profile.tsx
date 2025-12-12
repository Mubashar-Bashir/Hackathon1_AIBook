// src/components/Profile.tsx
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { User } from '../utils/auth';

const Profile: React.FC = () => {
  const { user, loading, logout } = useAuth();
  const [profile, setProfile] = useState<User | null>(null);

  useEffect(() => {
    setProfile(user);
  }, [user]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!profile) {
    return <div>Please log in to view your profile.</div>;
  }

  return (
    <div style={{ maxWidth: '600px', margin: '2rem auto', padding: '2rem' }}>
      <h2>User Profile</h2>
      <div style={{ marginBottom: '1rem' }}>
        <strong>Email:</strong> {profile.email}
      </div>
      <div style={{ marginBottom: '1rem' }}>
        <strong>User ID:</strong> {profile.userId}
      </div>
      {profile.softwareExperience && (
        <div style={{ marginBottom: '1rem' }}>
          <strong>Software Experience:</strong> {profile.softwareExperience}
        </div>
      )}
      {profile.hardwareExperience && (
        <div style={{ marginBottom: '1rem' }}>
          <strong>Hardware Experience:</strong> {profile.hardwareExperience}
        </div>
      )}
      {profile.interests && profile.interests.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <strong>Interests:</strong> {profile.interests.join(', ')}
        </div>
      )}
      {profile.createdAt && (
        <div style={{ marginBottom: '1rem' }}>
          <strong>Member Since:</strong> {new Date(profile.createdAt).toLocaleDateString()}
        </div>
      )}
      <button 
        onClick={() => logout()} 
        style={{ padding: '0.5rem 1rem', backgroundColor: '#ff4444', color: 'white', border: 'none', borderRadius: '4px' }}
      >
        Logout
      </button>
    </div>
  );
};

export default Profile;