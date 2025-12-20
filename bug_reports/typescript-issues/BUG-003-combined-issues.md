---
id: "BUG-003"
title: "Combined CSS and SSR Issues in Authentication Components"
date: "2025-12-14"
status: "resolved"
severity: "critical"
affected_components: ["PersonalizationToggle.tsx", "TranslationToggle.tsx", "Chatbot.tsx"]
tags: ["typescript", "styling", "ssr", "auth", "context", "docusaurus"]
---

## Description
Multiple issues were present in the same components:
1. TypeScript error with styled-jsx syntax
2. Static site generation failure due to auth context
3. Improper handling of client-side rendering

## Root Cause
The components were using styled-jsx which isn't properly configured for TypeScript in the Docusaurus setup, and they were calling `useAuth` hook during static generation when the AuthProvider context was not available.

## Solution
Combined approach addressing both issues:
1. Converted styled-jsx to CSS modules for proper TypeScript support
2. Implemented SSR-safe patterns for auth context usage
3. Added client-side detection to prevent SSR errors

## Files Changed
- PersonalizationToggle.tsx → PersonalizationToggle.module.css
- TranslationToggle.tsx → TranslationToggle.module.css
- Chatbot.tsx → Chatbot.module.css

## Testing
- TypeScript type checking passes
- Build process completes successfully
- Development server runs without errors
- Components render properly after client hydration
- No SSR errors during static generation
- All styling preserved and working correctly