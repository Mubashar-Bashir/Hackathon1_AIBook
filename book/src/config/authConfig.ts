// src/config/authConfig.ts
export const authConfig = {
  // BetterAuth API endpoint
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  
  // Token expiration settings
  tokenExpirationMinutes: 30,
  
  // OAuth providers configuration
  providers: {
    google: {
      enabled: process.env.REACT_APP_GOOGLE_CLIENT_ID ? true : false,
      clientId: process.env.REACT_APP_GOOGLE_CLIENT_ID,
    },
    github: {
      enabled: process.env.REACT_APP_GITHUB_CLIENT_ID ? true : false,
      clientId: process.env.REACT_APP_GITHUB_CLIENT_ID,
    }
  },
  
  // Local storage keys
  storageKeys: {
    accessToken: 'accessToken',
    userId: 'userId',
    refreshToken: 'refreshToken'
  }
};