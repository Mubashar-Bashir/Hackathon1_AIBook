// src/utils/auth.ts
import { authConfig } from '../config/authConfig';

export interface User {
  userId: string;
  email: string;
  background?: string; // 'beginner', 'intermediate', 'expert'
  softwareExperience?: string;
  hardwareExperience?: string;
  interests?: string[];
  createdAt?: string;
}

export interface LoginResponse {
  message: string;
  accessToken: string;
  userId: string;
}

export interface SignupData {
  email: string;
  password: string;
  softwareExperience?: string;
  hardwareExperience?: string;
  interests?: string[];
}

class AuthService {
  private apiUrl: string;

  constructor() {
    // Only set apiUrl if window is available (browser environment)
    if (typeof window !== 'undefined') {
      this.apiUrl = authConfig.apiUrl;
    } else {
      // For SSR, set a default value that won't cause errors
      this.apiUrl = '';
    }
  }

  async signup(userData: SignupData): Promise<LoginResponse> {
    // Ensure we're in the browser before making requests
    if (typeof window === 'undefined') {
      throw new Error('Authentication methods can only be used in browser environment');
    }

    const response = await fetch(`${this.apiUrl}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        name: userData.email.split('@')[0], // Use part of email as name if not provided
        password: userData.password,
        background: 'beginner' // Default background level
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Signup failed');
    }

    const data = await response.json();

    // Return the expected format for LoginResponse
    return {
      message: 'Registration successful',
      accessToken: data.session_token,
      userId: data.user_id
    };
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    // Ensure we're in the browser before making requests
    if (typeof window === 'undefined') {
      throw new Error('Authentication methods can only be used in browser environment');
    }

    const response = await fetch(`${this.apiUrl}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Login failed');
    }

    const data = await response.json();

    // Return the expected format for LoginResponse
    return {
      message: 'Login successful',
      accessToken: data.session_token,
      userId: data.user_id
    };
  }

  async logout(): Promise<void> {
    // Call the backend logout endpoint to invalidate the session
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem(authConfig.storageKeys.accessToken);
      if (token) {
        try {
          await fetch(`${this.apiUrl}/api/auth/logout`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });
        } catch (error) {
          console.error('Error calling logout endpoint:', error);
          // Continue with local cleanup even if backend call fails
        }
      }

      // Remove token from localStorage
      localStorage.removeItem(authConfig.storageKeys.accessToken);
      localStorage.removeItem(authConfig.storageKeys.userId);
    }
  }

  async getProfile(): Promise<User> {
    if (typeof window === 'undefined') {
      throw new Error('No access token found');
    }

    const token = localStorage.getItem(authConfig.storageKeys.accessToken);
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch(`${this.apiUrl}/api/auth/profile`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch profile');
    }

    const data = await response.json();

    // Map the backend response to the frontend User interface
    return {
      userId: data.user_id,
      email: data.email,
      background: data.background
    };
  }

  // Store token in localStorage
  setToken(accessToken: string, userId: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(authConfig.storageKeys.accessToken, accessToken);
      localStorage.setItem(authConfig.storageKeys.userId, userId);
    }
  }

  // Get token from localStorage
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(authConfig.storageKeys.accessToken);
    }
    return null;
  }

  getUserId(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(authConfig.storageKeys.userId);
    }
    return null;
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    if (typeof window === 'undefined') {
      return false; // Server-side rendering - no authentication possible
    }

    const token = this.getToken();
    if (!token) return false;

    // Check if token is expired
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch (e) {
      return false;
    }
  }
}

export default new AuthService();