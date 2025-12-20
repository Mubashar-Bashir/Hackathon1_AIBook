---
id: 101
title: implement-chatkit-ui-layer-2-spec
stage: spec
date_iso: 2025-12-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: chatkit-ui-layer-2
branch: 001-chatkit-ui-layer-2
user: mubashar
command: sp.specify
labels:
  - specification
  - chatkit
  - ui
  - docusaurus
links:
  spec: ../specs/001-chatkit-ui-layer-2/spec.md
  checklist: ../specs/001-chatkit-ui-layer-2/checklists/requirements.md
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - ../specs/001-chatkit-ui-layer-2/spec.md
  - ../specs/001-chatkit-ui-layer-2/checklists/requirements.md
tests_yaml: |
  - User scenarios defined for text selection tooltip
  - User scenarios defined for chatbot window integration
  - User scenarios defined for suggested prompts
  - Functional requirements validated
  - Success criteria defined and measurable
prompt_text: |
  Implement OpenAI ChatKit UI Layer (Layer-2) for AIBOOK

  # 🎯 Objective
  Create a standalone, high-fidelity Frontend UI for the Chatbot using the OpenAI ChatKit SDK. This layer focuses on visuals, interaction, and SSR compatibility.

  # 📦 Dependencies
  - Install: `@openai/chatkit-react`, `lucide-react`
  - Use existing: `tailwind`, `shadcn`, `daisyUI`

  # 🏗️ Architecture
  1. **Component A: `src/components/Chatbot/SelectionTooltip.tsx`**
     - Detects text selection in the browser.
     - Shows a "Ask AI" floating button (Purple gradient).
     - On click: Dispatches a custom 'aibook:open-with-context' event with the selected text.

  2. **Component B: `src/components/Chatbot/ChatWindow.tsx`**
     - Wraps the `<ChatKit />` component from `@openai/chatkit-react`.
     - **Mock API Logic:** For this layer, mock the `getClientSecret` function to return a dummy string so the UI renders without a live backend.
     - **Styling:** Match "chatbot widget Ui_UX.png" using Tailwind.
       - Background: `bg-gradient-to-b from-violet-700 via-purple-600 to-indigo-900`.
       - Mascot: Absolute-positioned image peeking over the top chat bubble.
       - Input: Rounded pill-shaped composer.

  3. **Component C: `src/theme/Root.js`**
     - Swizzle the Docusaurus Root component.
     - Wrap both components in `<BrowserOnly>` to prevent SSR crashes.

  # ✨ Custom Logic (OpenAI SDK Integration)
  - Listen for 'aibook:open-with-context' event.
  - Use the `control.sendUserMessage({ text: ... })` method from ChatKit to programmatically start a chat with the selected text.
  - Configure `suggestion chips` in the ChatKit `startScreen` for: "Explain SDD", "AI-Native Level 4", "Agentic Loops".

  # ✔️ Success Criteria
  - [ ] Tooltip appears when highlighting book text.
  - [ ] Tooltip click opens the Chatbot and pre-fills the message.
  - [ ] Purple mascot is visible and properly layered (z-index).
  - [ ] Zero 'window is not defined' errors during build.
response_text: |
  Successfully created the feature specification for OpenAI ChatKit UI Layer (Layer-2) for AIBOOK.
  - Created branch 001-chatkit-ui-layer-2
  - Generated comprehensive spec with user scenarios, functional requirements, and success criteria
  - Created validation checklist
  - All requirements from the feature description have been captured in a technology-agnostic specification
outcome: |
  Specification created successfully with all mandatory sections completed.
  The spec captures the requirements for implementing a text selection tooltip, chatbot window with proper styling,
  suggested prompts, and SSR compatibility requirements.
---

## User Input

```text
Implement OpenAI ChatKit UI Layer (Layer-2) for AIBOOK

# 🎯 Objective
Create a standalone, high-fidelity Frontend UI for the Chatbot using the OpenAI ChatKit SDK. This layer focuses on visuals, interaction, and SSR compatibility.

# 📦 Dependencies
- Install: `@openai/chatkit-react`, `lucide-react`
- Use existing: `tailwind`, `shadcn`, `daisyUI`

# 🏗️ Architecture
1. **Component A: `src/components/Chatbot/SelectionTooltip.tsx`**
   - Detects text selection in the browser.
   - Shows a "Ask AI" floating button (Purple gradient).
   - On click: Dispatches a custom 'aibook:open-with-context' event with the selected text.

2. **Component B: `src/components/Chatbot/ChatWindow.tsx`**
   - Wraps the `<ChatKit />` component from `@openai/chatkit-react`.
   - **Mock API Logic:** For this layer, mock the `getClientSecret` function to return a dummy string so the UI renders without a live backend.
   - **Styling:** Match "chatbot widget Ui_UX.png" using Tailwind.
     - Background: `bg-gradient-to-b from-violet-700 via-purple-600 to-indigo-900`.
     - Mascot: Absolute-positioned image peeking over the top chat bubble.
     - Input: Rounded pill-shaped composer.

3. **Component C: `src/theme/Root.js`**
   - Swizzle the Docusaurus Root component.
   - Wrap both components in `<BrowserOnly>` to prevent SSR crashes.

# ✨ Custom Logic (OpenAI SDK Integration)
- Listen for 'aibook:open-with-context' event.
- Use the `control.sendUserMessage({ text: ... })` method from ChatKit to programmatically start a chat with the selected text.
- Configure `suggestion chips` in the ChatKit `startScreen` for: "Explain SDD", "AI-Native Level 4", "Agentic Loops".

# ✔️ Success Criteria
- [ ] Tooltip appears when highlighting book text.
- [ ] Tooltip click opens the Chatbot and pre-fills the message.
- [ ] Purple mascot is visible and properly layered (z-index).
- [ ] Zero 'window is not defined' errors during build.
```

## Implementation Summary

Successfully created the feature specification for OpenAI ChatKit UI Layer (Layer-2) for AIBOOK.

- Created branch 001-chatkit-ui-layer-2
- Generated comprehensive spec with user scenarios, functional requirements, and success criteria
- Created validation checklist
- All requirements from the feature description have been captured in a technology-agnostic specification

The specification includes:
- User Story 1: Text Selection Tooltip (Priority: P1)
- User Story 2: Chatbot Window Integration (Priority: P1)
- User Story 3: Suggested Prompts (Priority: P2)
- 10 functional requirements covering all aspects of the feature
- 5 measurable success criteria
- Key entities and edge cases identified