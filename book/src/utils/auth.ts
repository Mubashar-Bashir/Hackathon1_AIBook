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

    const response = await fetch(`${this.apiUrl}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Signup failed');
    }

    return response.json();
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    // Ensure we're in the browser before making requests
    if (typeof window === 'undefined') {
      throw new Error('Authentication methods can only be used in browser environment');
    }

    const response = await fetch(`${this.apiUrl}/auth/signin`, {
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

    return response.json();
  }

  async logout(): Promise<void> {
    // Remove token from localStorage
    if (typeof window !== 'undefined') {
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

    const response = await fetch(`${this.apiUrl}/auth/profile`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch profile');
    }

    return response.json();
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