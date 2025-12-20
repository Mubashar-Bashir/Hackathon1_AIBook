// src/config/authConfig.ts
export const authConfig = {
  // BetterAuth API endpoint
  apiUrl: typeof window !== 'undefined'
    ? (window as any)._env_?.REACT_APP_API_URL || 'http://localhost:8000'
    : process.env.REACT_APP_API_URL || 'http://localhost:8000',

  // Token expiration settings
  tokenExpirationMinutes: 30,

  // OAuth providers configuration
  providers: {
    google: {
      enabled: typeof window !== 'undefined'
        ? !!(window as any)._env_?.REACT_APP_GOOGLE_CLIENT_ID
        : !!process.env.REACT_APP_GOOGLE_CLIENT_ID,
      clientId: typeof window !== 'undefined'
        ? (window as any)._env_?.REACT_APP_GOOGLE_CLIENT_ID
        : process.env.REACT_APP_GOOGLE_CLIENT_ID,
    },
    github: {
      enabled: typeof window !== 'undefined'
        ? !!(window as any)._env_?.REACT_APP_GITHUB_CLIENT_ID
        : !!process.env.REACT_APP_GITHUB_CLIENT_ID,
      clientId: typeof window !== 'undefined'
        ? (window as any)._env_?.REACT_APP_GITHUB_CLIENT_ID
        : process.env.REACT_APP_GITHUB_CLIENT_ID,
    }
  },

  // Local storage keys
  storageKeys: {
    accessToken: 'accessToken',
    userId: 'userId',
    refreshToken: 'refreshToken'
  }
};