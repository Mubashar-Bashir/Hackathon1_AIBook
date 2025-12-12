// src/config/authConfig.ts
export const authConfig = {
  // BetterAuth API endpoint - default to localhost:8000 for development
  apiUrl: 'http://localhost:8000',

  // Token expiration settings
  tokenExpirationMinutes: 30,

  // OAuth providers configuration
  providers: {
    google: {
      enabled: false, // Set to true when you have a client ID
      clientId: undefined,
    },
    github: {
      enabled: false, // Set to true when you have a client ID
      clientId: undefined,
    }
  },

  // Local storage keys
  storageKeys: {
    accessToken: 'accessToken',
    userId: 'userId',
    refreshToken: 'refreshToken'
  }
};