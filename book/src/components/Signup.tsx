// src/components/Signup.tsx
import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Signup: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [softwareExperience, setSoftwareExperience] = useState('');
  const [hardwareExperience, setHardwareExperience] = useState('');
  const [interests, setInterests] = useState('');
  const [error, setError] = useState('');
  const { signup } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const interestsArray = interests.split(',').map(i => i.trim()).filter(i => i);
      
      await signup({
        email,
        password,
        softwareExperience,
        hardwareExperience,
        interests: interestsArray
      });
      setError('');
      // Redirect or show success message
      window.location.href = '/dashboard'; // Or wherever you want to redirect
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto', padding: '2rem' }}>
      <h2>Sign Up</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="softwareExperience">Software Experience:</label>
          <input
            type="text"
            id="softwareExperience"
            value={softwareExperience}
            onChange={(e) => setSoftwareExperience(e.target.value)}
            placeholder="e.g., Python, React"
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="hardwareExperience">Hardware Experience:</label>
          <input
            type="text"
            id="hardwareExperience"
            value={hardwareExperience}
            onChange={(e) => setHardwareExperience(e.target.value)}
            placeholder="e.g., Arduino, Raspberry Pi"
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="interests">Interests (comma-separated):</label>
          <input
            type="text"
            id="interests"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            placeholder="e.g., robotics, AI"
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <button type="submit" style={{ padding: '0.5rem 1rem' }}>
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default Signup;