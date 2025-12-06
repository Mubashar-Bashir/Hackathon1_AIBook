// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, LoginResponse } from '../utils/auth';
import authService from '../utils/auth';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<LoginResponse>;
  signup: (userData: any) => Promise<LoginResponse>; // Using any for simplicity
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Only run on client-side to avoid SSR issues
    if (typeof window !== 'undefined') {
      // Check if user is already logged in on initial load
      const initAuth = async () => {
        if (authService.isAuthenticated()) {
          try {
            const profile = await authService.getProfile();
            setUser(profile);
          } catch (error) {
            console.error('Failed to fetch user profile:', error);
            // Token might be invalid, clear it
            await authService.logout();
          }
        }
        setLoading(false);
      };

      initAuth();
    } else {
      // On server-side, set loading to false immediately
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const response = await authService.login(email, password);
    authService.setToken(response.accessToken, response.userId);
    const profile = await authService.getProfile();
    setUser(profile);
    return response;
  };

  const signup = async (userData: any) => {
    const response = await authService.signup(userData);
    authService.setToken(response.accessToken, response.userId);
    const profile = await authService.getProfile();
    setUser(profile);
    return response;
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  // Only check authentication status on client-side
  const isAuthenticated = typeof window !== 'undefined' ? authService.isAuthenticated() : false;

  const value = {
    user,
    loading,
    login,
    signup,
    logout,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};