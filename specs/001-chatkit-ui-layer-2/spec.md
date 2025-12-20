# Feature Specification: OpenAI ChatKit UI Layer (Layer-2) for AIBOOK

**Feature Branch**: `001-chatkit-ui-layer-2`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "Implement OpenAI ChatKit UI Layer (Layer-2) for AIBOOK"

## Clarifications

### Session 2025-12-19

- Q: Should the chatbot UI meet specific accessibility standards? → A: WCAG 2.1 AA compliance required - keyboard navigation, ARIA labels, focus management
- Q: What are the specific requirements for mobile device support? → A: UI/UX both work for all device according to window size
- Q: How should the system handle ChatKit initialization failures? → A: Comprehensive error handling - fallback UI, retry mechanisms, user notifications
- Q: What is the maximum length of selected text that should be handled? → A: 200 characters max with truncation
- Q: Are there specific security requirements for handling user selections? → A: Standard frontend security - no secrets in client, proper input sanitization
- Q: What is the recommended UI library integration strategy? → A: Use Tailwind as primary framework with daisyUI and shadCN components as needed, ensuring no conflicts with Docusaurus styling
- Q: How should the mascot image be implemented? → A: SVG component with subtle animation - lightweight and scalable with visual appeal
- Q: What mock implementation strategy should be used? → A: Comprehensive mock with simulated responses and state - enables full UI development without backend

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Text Selection Tooltip (Priority: P1)

As a reader of the AIBOOK textbook, I want to be able to select text on any page and see a floating "Ask AI" button so that I can get immediate clarification or explanation about the selected content.

**Why this priority**: This is the core functionality that enables users to interact with the AI chatbot directly from the textbook content, providing immediate value.

**Independent Test**: Can be fully tested by selecting text on a book page and verifying that a floating purple "Ask AI" button appears. The button should be positioned near the selected text and be easily clickable.

**Acceptance Scenarios**:

1. **Given** user has selected text on a book page, **When** user releases the mouse, **Then** a floating "Ask AI" button appears near the selected text
2. **Given** user has selected text on a book page, **When** user clicks the "Ask AI" button, **Then** a custom event 'aibook:open-with-context' is dispatched with the selected text

---

### User Story 2 - Chatbot Window Integration (Priority: P1)

As a user who has clicked the "Ask AI" button, I want to see an AI chatbot window appear that is pre-filled with my selected text so that I can continue the conversation and get answers to my questions.

**Why this priority**: This completes the core user journey from text selection to AI interaction, delivering the primary value proposition.

**Independent Test**: Can be fully tested by opening the chatbot window and verifying it renders properly with the correct styling, mascot image, and input field. The chatbot should accept and process user messages.

**Acceptance Scenarios**:

1. **Given** user has clicked the "Ask AI" button, **When** chatbot window appears, **Then** it displays with the correct purple gradient background styling
2. **Given** chatbot window is open, **When** user sees the mascot image, **Then** it appears as an absolute-positioned element peeking over the top chat bubble
3. **Given** user wants to ask a follow-up question, **When** user types in the input field, **Then** the pill-shaped composer input field functions properly

---

### User Story 3 - Suggested Prompts (Priority: P2)

As a user who wants quick access to common AI textbook questions, I want to see suggested prompts like "Explain SDD", "AI-Native Level 4", and "Agentic Loops" in the chatbot start screen so that I can easily explore key concepts from the textbook.

**Why this priority**: This enhances the user experience by providing guided access to common textbook topics and concepts.

**Independent Test**: Can be tested by opening the chatbot when no conversation is active and verifying that the suggested prompts appear as clickable chips in the start screen.

**Acceptance Scenarios**:

1. **Given** chatbot window is opened with no active conversation, **When** start screen appears, **Then** suggested prompts "Explain SDD", "AI-Native Level 4", and "Agentic Loops" appear as clickable chips

---

### Edge Cases

- How does the system handle text selection in non-textbook content areas?
- What happens when multiple text selections are made in quick succession?
- How does the system handle ChatKit initialization failures, network errors, or timeout scenarios?
- How does the system handle selected text that exceeds 200 character limit?
- How does the system ensure accessibility compliance across different assistive technologies?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST detect text selection events in the browser and show a floating "Ask AI" button with purple gradient styling
- **FR-002**: System MUST dispatch a custom 'aibook:open-with-context' event with the selected text when the tooltip button is clicked
- **FR-003**: System MUST render a ChatKit component with the correct purple gradient background: `bg-gradient-to-b from-violet-700 via-purple-600 to-indigo-900`
- **FR-004**: System MUST display a mascot image as an absolute-positioned element peeking over the top chat bubble
- **FR-005**: System MUST provide a rounded pill-shaped composer input field for user messages
- **FR-006**: System MUST accept and process the selected text as the initial user message when the chatbot opens
- **FR-007**: System MUST display suggested prompt chips: "Explain SDD", "AI-Native Level 4", "Agentic Loops" in the start screen
- **FR-008**: System MUST prevent SSR (Server-Side Rendering) crashes by wrapping components in `<BrowserOnly>` tags
- **FR-009**: System MUST mock the `getClientSecret` function to return a dummy string for UI rendering without a live backend
- **FR-010**: System MUST ensure zero 'window is not defined' errors during build process
- **FR-011**: System MUST implement WCAG 2.1 AA compliance for keyboard navigation, ARIA labels, and focus management
- **FR-012**: System MUST be responsive and adapt UI/UX for all device sizes according to window dimensions
- **FR-013**: System MUST implement comprehensive error handling with fallback UI, retry mechanisms, and user notifications for ChatKit failures
- **FR-014**: System MUST truncate selected text to 200 characters maximum with appropriate user feedback
- **FR-015**: System MUST implement standard frontend security practices with no secrets in client and proper input sanitization
- **FR-016**: System MUST use Tailwind as primary CSS framework with daisyUI and shadCN components as needed, ensuring no conflicts with existing Docusaurus styling
- **FR-017**: System MUST implement mascot as an SVG component with subtle animation positioned absolutely over chat bubbles
- **FR-018**: System MUST implement comprehensive mock system with simulated responses and state for UI development without backend dependency

### Key Entities *(include if feature involves data)*

- **Selected Text**: The text content that the user has highlighted/selected in the browser, used as context for the AI chat
- **Custom Event**: A 'aibook:open-with-context' event that carries the selected text payload to trigger the chatbot
- **Chatbot Window**: The UI component that contains the ChatKit interface with proper styling and mascot positioning

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can select any text in the textbook and see the "Ask AI" tooltip appear within 100ms of releasing the mouse
- **SC-002**: Clicking the "Ask AI" tooltip successfully opens the chatbot window and pre-fills the message with selected text 95% of the time
- **SC-003**: The chatbot window displays with correct purple gradient styling and mascot image visible on 100% of page loads
- **SC-004**: The application builds successfully without any 'window is not defined' errors during the SSR process
- **SC-005**: Suggested prompts appear as clickable chips in the chatbot start screen and are accessible to users 100% of the time
- **SC-006**: The UI meets WCAG 2.1 AA compliance standards for keyboard navigation and screen reader accessibility
- **SC-007**: The UI is responsive and adapts appropriately to different device sizes and window dimensions
- **SC-008**: The system handles ChatKit initialization failures gracefully with fallback UI and user notifications 95% of the time
- **SC-009**: Selected text is truncated to 200 characters maximum with appropriate user feedback when exceeded
- **SC-010**: The system implements proper security practices with no sensitive information exposed in client code
- **SC-011**: The UI components use Tailwind as primary CSS framework with daisyUI and shadCN components without conflicts with Docusaurus styling
- **SC-012**: The mascot SVG component appears with subtle animation and proper positioning over chat bubbles 100% of the time
- **SC-013**: The comprehensive mock system provides simulated responses and state management for UI development without backend dependency
