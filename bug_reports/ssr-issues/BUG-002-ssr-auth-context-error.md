---
id: "BUG-002"
title: "Static Site Generation Error with AuthContext"
date: "2025-12-14"
status: "resolved"
severity: "critical"
affected_components: ["PersonalizationToggle.tsx", "TranslationToggle.tsx", "Chatbot.tsx"]
tags: ["ssr", "auth", "context", "build", "docusaurus"]
---

## Description
During static site generation, the following error occurred:
```
Error: Docusaurus static site generation failed for 1 paths:
- "/docs/sample_translation_demo"
[cause]: Error: useAuth must be used within an AuthProvider
```

This prevented the site from building successfully for production deployment.

## Root Cause
Components that used the `useAuth` hook were being rendered during static site generation (SSG) when the AuthProvider context was not available. Docusaurus tries to pre-render pages during build time, but the authentication context is only available on the client-side after hydration.

## Solution
Implemented proper SSR handling by:
1. Adding client-side detection using `isClient` state
2. Using useEffect to set client state after mounting
3. Adding early return for server-side rendering
4. Only calling `useAuth` hook after client detection

## Files Changed
- PersonalizationToggle.tsx
- TranslationToggle.tsx
- Chatbot.tsx

## Code Pattern Applied
```typescript
const [isClient, setIsClient] = useState(false);

useEffect(() => {
  setIsClient(true);
}, []);

if (!isClient) {
  return null; // Don't render during SSR
}

const { isAuthenticated, user } = useAuth(); // Safe to call after client detection
```

## Testing
- Build process completes successfully
- Development server runs without errors
- Components render properly after client hydration
- No SSR errors during static generation