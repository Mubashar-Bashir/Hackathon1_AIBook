# Implementation Tasks: AIBOOK ChatKit UI Frontend (Layer-2)

**Feature**: OpenAI ChatKit UI Layer (Layer-2) for AIBOOK
**Branch**: `001-chatkit-ui-layer-2`
**Spec**: ../specs/001-chatkit-ui-layer-2/spec.md
**Plan**: ../specs/001-chatkit-ui-layer-2/plan.md

## Dependencies

User stories can be implemented in parallel after foundational tasks are complete:
- US1 (Text Selection Tooltip) and US2 (Chatbot Window) can be developed independently
- US3 (Suggested Prompts) depends on US2 (Chatbot Window) implementation
- All stories require foundational components to be complete first

## Parallel Execution Examples

- **Setup Phase**: T001-T008 can be done in parallel with research tasks T009-T012
- **US1 & US2**: Text selection tooltip and chatbot window can be developed in parallel after foundational tasks
- **US3**: Can be developed after US2 is complete

## Implementation Strategy

MVP scope includes US1 (Text Selection Tooltip) and US2 (Chatbot Window Integration) to deliver core functionality. US3 (Suggested Prompts) is an enhancement that builds on the core functionality.

---

## Phase 1: Setup

- [X] T001 Install required dependencies: @openai/chatkit-react, daisyUI, shadcn/ui
- [X] T002 Create directory structure: src/components/Chatbot/ and src/hooks/
- [X] T003 [P] Create TypeScript type definitions in src/components/Chatbot/types.ts
- [X] T004 [P] Set up Docusaurus Root.js integration in src/client-modules/Root.js
- [X] T005 [P] Create foundational CSS utility classes with Tailwind
- [X] T006 [P] Prepare mascot image assets for chatbot UI
- [X] T007 [P] Create mock ChatKit initialization function for UI development
- [X] T008 [P] Set up testing framework with Jest and React Testing Library

## Phase 2: Foundational Components

- [X] T009 [P] Create useTextSelection hook in src/hooks/useTextSelection.ts
- [X] T010 [P] Create ChatContainer component with BrowserOnly wrapper in src/components/Chatbot/ChatContainer.tsx
- [X] T011 [P] Create ChatContext for state management in src/components/Chatbot/context.ts
- [X] T012 [P] Create TooltipContext for tooltip state management in src/components/Chatbot/context.ts
- [X] T013 [P] Implement text selection detection logic with proper cleanup
- [X] T014 [P] Create custom event dispatcher for 'aibook:open-with-context' events
- [X] T015 [P] Implement 200 character limit validation for selected text
- [X] T016 [P] Set up responsive design breakpoints for mobile compatibility
- [X] T017 [P] Implement WCAG 2.1 AA accessibility patterns for components
- [X] T018 [P] Create error handling utilities for ChatKit failures

## Phase 3: User Story 1 - Text Selection Tooltip (Priority: P1)

**Goal**: Enable users to select text on any page and see a floating "Ask AI" button for immediate clarification

**Independent Test**: Can be fully tested by selecting text on a book page and verifying that a floating purple "Ask AI" button appears. The button should be positioned near the selected text and be easily clickable.

- [X] T019 [US1] Create SelectionTooltip component in src/components/Chatbot/SelectionTooltip.tsx
- [X] T020 [US1] Implement text selection detection with mouseup event listener
- [X] T021 [US1] Calculate tooltip position relative to selected text
- [X] T022 [US1] Style tooltip with purple gradient matching mockup (bg-gradient-to-b from-violet-700 via-purple-600 to-indigo-900)
- [X] T023 [US1] Implement 200 character limit with truncation for selected text
- [X] T024 [US1] Add accessibility attributes (ARIA labels, keyboard navigation) to tooltip
- [X] T025 [US1] Ensure tooltip is responsive across different device sizes
- [X] T026 [US1] Dispatch custom 'aibook:open-with-context' event with selected text when clicked
- [X] T027 [US1] Add tooltip animation and smooth transitions
- [X] T028 [US1] Handle edge case: multiple text selections made in quick succession
- [X] T029 [US1] Handle edge case: very large text selections (entire chapters)
- [X] T030 [US1] Test tooltip positioning on mobile devices and small screens
- [X] T031 [US1] Verify tooltip appears within 100ms of releasing the mouse
- [X] T032 [US1] Test accessibility compliance with screen readers

## Phase 4: User Story 2 - Chatbot Window Integration (Priority: P1)

**Goal**: Show an AI chatbot window that appears pre-filled with selected text when user clicks "Ask AI" button

**Independent Test**: Can be fully tested by opening the chatbot window and verifying it renders properly with the correct styling, mascot image, and input field. The chatbot should accept and process user messages.

- [X] T033 [US2] Create ChatWidget component in src/components/Chatbot/ChatWidget.tsx
- [X] T034 [US2] Implement purple gradient background styling (bg-gradient-to-b from-violet-700 via-purple-600 to-indigo-900)
- [X] T035 [US2] Create mascot component in src/components/Chatbot/Mascot.tsx
- [X] T036 [US2] Position mascot as absolute element peeking over top chat bubble
- [X] T037 [US2] Create pill-shaped composer input field for user messages
- [X] T038 [US2] Implement ChatKit integration with mocked getClientSecret
- [X] T039 [US2] Accept and process selected text as initial user message when chatbot opens
- [X] T040 [US2] Implement message display area with proper styling
- [X] T041 [US2] Add accessibility attributes to chat interface (keyboard navigation, ARIA)
- [X] T042 [US2] Ensure chat window is responsive across all device sizes
- [X] T043 [US2] Implement fixed positioning to bottom-right with z-index: 1001
- [X] T044 [US2] Create fallback UI for ChatKit initialization failures
- [X] T045 [US2] Implement error handling with user notifications
- [X] T046 [US2] Add retry mechanisms for network errors
- [X] T047 [US2] Implement graceful degradation when external services fail
- [X] T048 [US2] Test chat window rendering without 'window is not defined' errors
- [X] T049 [US2] Verify mascot image appears as absolute-positioned element on 100% of page loads
- [X] T050 [US2] Test pill-shaped composer input field functionality
- [X] T051 [US2] Verify chatbot opens with selected text pre-filled 95% of the time

## Phase 5: User Story 3 - Suggested Prompts (Priority: P2)

**Goal**: Show suggested prompts like "Explain SDD", "AI-Native Level 4", and "Agentic Loops" in chatbot start screen for quick access to common textbook questions

**Independent Test**: Can be tested by opening the chatbot when no conversation is active and verifying that the suggested prompts appear as clickable chips in the start screen.

- [X] T052 [US3] Create suggested prompts UI component in chat start screen
- [X] T053 [US3] Implement "Explain SDD" prompt chip as clickable element
- [X] T054 [US3] Implement "AI-Native Level 4" prompt chip as clickable element
- [X] T055 [US3] Implement "Agentic Loops" prompt chip as clickable element
- [X] T056 [US3] Style prompt chips as clickable elements with proper accessibility
- [X] T057 [US3] Add keyboard navigation support for suggested prompts
- [X] T058 [US3] Ensure suggested prompts are responsive across device sizes
- [X] T059 [US3] Test suggested prompts appear as clickable chips 100% of the time
- [X] T060 [US3] Verify suggested prompts are accessible to users

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T061 Implement comprehensive error handling with fallback UI for all components
- [X] T062 Add performance optimizations (React.memo, lazy loading) to components
- [X] T063 Conduct accessibility audit and ensure WCAG 2.1 AA compliance
- [X] T064 Implement responsive design testing across multiple device sizes
- [ ] T065 Add unit tests for all components and hooks (80%+ coverage)
- [ ] T066 Add integration tests for Docusaurus compatibility
- [ ] T067 Implement cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] T068 Conduct end-to-end testing of complete user journey (select text → tooltip → chat)
- [ ] T069 Document component APIs and integration patterns
- [X] T070 Verify no changes to existing CSS files (only Tailwind utilities used)
- [X] T071 Ensure zero 'window is not defined' errors during SSR process
- [X] T072 Verify all components are properly isolated in src/components/Chatbot/
- [X] T073 Test security practices: no secrets exposed in client code
- [X] T074 Final integration testing with Docusaurus application
- [X] T075 Performance testing: verify <100ms response time for text selection