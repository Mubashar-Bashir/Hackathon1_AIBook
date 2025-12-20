---
id: "BUG-001"
title: "TypeScript Error with styled-jsx in PersonalizationToggle Component"
date: "2025-12-14"
status: "resolved"
severity: "high"
affected_components: ["PersonalizationToggle.tsx", "TranslationToggle.tsx", "Chatbot.tsx"]
tags: ["typescript", "styling", "jsx", "docusaurus"]
---

## Description
TypeScript error occurred in PersonalizationToggle.tsx:
```
Type '{ children: string; jsx: true; }' is not assignable to type 'DetailedHTMLProps<StyleHTMLAttributes<HTMLStyleElement>, HTMLStyleElement>'.
Property 'jsx' does not exist on type 'DetailedHTMLProps<StyleHTMLAttributes<HTMLStyleElement>, HTMLStyleElement>'.
```

This error was also present in TranslationToggle.tsx and Chatbot.tsx components that used styled-jsx syntax.

## Root Cause
The Docusaurus project was using styled-jsx syntax which is not properly configured for TypeScript in the current setup. The jsx attribute was being added by the build system but TypeScript was not recognizing it properly.

## Solution
Converted from styled-jsx to CSS modules approach:
1. Created corresponding .module.css files for each component
2. Updated component imports to use CSS modules
3. Replaced className strings with module-based class names
4. Removed styled-jsx syntax entirely

## Files Changed
- PersonalizationToggle.tsx → PersonalizationToggle.module.css
- TranslationToggle.tsx → TranslationToggle.module.css
- Chatbot.tsx → Chatbot.module.css

## Testing
- TypeScript type checking passes
- Development server runs without errors
- Build process completes successfully
- Components render with correct styling in browser