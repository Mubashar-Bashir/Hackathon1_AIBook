---
id: 101
title: ChatKit UI Clarification
stage: spec
date: 2025-12-19
surface: agent
model: Claude Sonnet 4.5
feature: 001-chatkit-ui-layer-2
branch: 001-chatkit-ui-layer-2
user: mubashar
command: sp.clarify
labels: ["clarification", "ui", "chatkit"]
links:
  spec: ../specs/001-chatkit-ui-layer-2/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - ../specs/001-chatkit-ui-layer-2/spec.md
tests:
 - null
---

## Prompt

AIBOOK ChatKit UI Frontend (Layer-2)
Target Goal: Implement a pixel-perfect, interactive Chatbot UI using OpenAI ChatKit SDK that supports "Active Reading" via text selection, while strictly isolating changes to avoid regressing existing Docusaurus features.

Focus: UI/UX Design (Purple Mockup), SDK Integration, and Frontend Interactivity.

Success Criteria:

Visual Parity: Matches "chatbot widget Ui_UX.png" (Violet/Indigo gradient, pill-shaped input, peeking mascot).

Active Reading: Highlighting text triggers an "Ask AI" tooltip that passes the selection into the Chatbot.

SSR Safety: Component is wrapped in <BrowserOnly> and builds without "window is not defined" errors.

Global Injection: Integrated via Docusaurus Root.js using a "Safe Wrapper" approach.

SDK Initialization: @openai/chatkit-react renders correctly using a mocked clientSecret.

Constraints:

Code Isolation: Do not alter or refactor existing Docusaurus components or logic. All new code must reside in src/components/Chatbot/ and be imported as a standalone module.

Regressions: Zero changes to existing CSS files; use Tailwind utility classes exclusively for Layer 2 components.

Stack: React, Tailwind CSS, daisyUI, shadcn/ui.

Positioning: Fixed to bottom-right with z-index: 1001.

Scoping: Styles must not leak into the main Docusaurus documentation layout.

Mocking: All responses are hardcoded "Mock Responses" (No FastAPI connection yet).

Not Building:

Backend/RAG: No FastAPI, Qdrant, or Neon DB integration.

Auth: No user login or session persistence.

Real Data: No live retrieval from the book's vector database.

🛠️ Execution Strategy for AI Agent
Component Encapsulation: Create a ChatContainer.tsx that acts as the only entry point.

Swizzle Protection: When editing src/theme/Root.js, only append the <ChatContainer /> as a sibling to {children}.

Event Bus: Use window.dispatchEvent to communicate between the book text and the chatbot to keep the implementation decoupled from the Docusaurus internal state.

## Response snapshot

I have successfully completed the clarification process for the AIBOOK ChatKit UI Frontend (Layer-2) feature. Here's what was accomplished:

**Questions Asked & Answered (5/5):**
1. Accessibility Requirements → WCAG 2.1 AA compliance required
2. Mobile Responsiveness → UI/UX both work for all device according to window size
3. Error Handling Strategy → Comprehensive error handling with fallback UI
4. Text Selection Length Limit → 200 characters max with truncation
5. Security Considerations → Standard frontend security practices

**Spec File Updated:**
- Path: `../specs/001-chatkit-ui-layer-2/spec.md`
- Added clarifications section with session details
- Updated Functional Requirements (FR-011 to FR-015 added)
- Updated Success Criteria (SC-006 to SC-010 added)
- Updated Edge Cases section to reflect new considerations

**Sections Touched:**
- Clarifications section (new)
- Functional Requirements
- Success Criteria
- Edge Cases

**Coverage Summary:**
- Functional Scope & Behavior: Resolved
- Domain & Data Model: Clear
- Interaction & UX Flow: Resolved
- Non-Functional Quality Attributes: Resolved
- Integration & External Dependencies: Resolved
- Edge Cases & Failure Handling: Resolved
- Constraints & Tradeoffs: Clear
- Terminology & Consistency: Clear
- Completion Signals: Clear
- Misc/Placeholders: Clear

All critical ambiguities have been resolved. The spec is now ready for the planning phase. I recommend proceeding with `/sp.plan` to create the implementation plan.

**Suggested Next Command:** `/sp.plan`

## Outcome

- ✅ Impact: Critical ambiguities resolved in feature specification, enhancing clarity for implementation
- 🧪 Tests: null
- 📁 Files: ../specs/001-chatkit-ui-layer-2/spec.md updated with clarifications
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Clarification process successfully reduced ambiguity in accessibility, mobile support, error handling, text limits, and security requirements

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null