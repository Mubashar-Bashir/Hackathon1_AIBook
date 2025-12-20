# Implementation Plan: AIBOOK ChatKit UI Frontend (Layer-2)

**Branch**: `001-chatkit-ui-layer-2` | **Date**: 2025-12-19 | **Spec**: ../specs/001-chatkit-ui-layer-2/spec.md
**Input**: Feature specification from `/specs/[001-chatkit-ui-layer-2]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a pixel-perfect, interactive Chatbot UI using OpenAI ChatKit SDK that supports "Active Reading" via text selection, while strictly isolating changes to avoid regressing existing Docusaurus features. The implementation will follow a clean-slate approach, recreating all components to ensure quality and compliance with all requirements.

## Technical Context

**Language/Version**: TypeScript/JavaScript (Node.js 18+)
**Primary Dependencies**: React, @openai/chatkit-react, Tailwind CSS, daisyUI, shadcn/ui, Docusaurus 3.x
**Storage**: N/A (Client-side only, no persistent storage)
**Testing**: Jest, React Testing Library
**Target Platform**: Web browser (Chrome, Firefox, Safari, Edge)
**Project Type**: Web frontend component for Docusaurus
**Performance Goals**: <100ms response time for text selection tooltip, 60fps animations
**Constraints**: Fixed to bottom-right with z-index: 1001, no changes to existing CSS files, WCAG 2.1 AA compliance
**Scale/Scope**: Single page application component, responsive across all device sizes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Security First**: Components will implement proper input sanitization and avoid hardcoded credentials. Mock clientSecret will be properly isolated.
2. **Source of Truth**: Chatbot will use mock responses, with future integration planned to connect to textbook content.
3. **Working Software Priority**: Focus on functional UI components that demonstrate the text selection and chat functionality.
4. **Modularity & Separation**: Components will be isolated in src/components/Chatbot/ with clear boundaries from existing Docusaurus components.
5. **Test-Driven Development**: Unit tests will verify component functionality and accessibility compliance.
6. **Clear Naming & Conventions**: React components will use PascalCase, consistent with project standards.

## Project Structure

### Documentation (this feature)

```text
specs/001-chatkit-ui-layer-2/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── components/
│   └── Chatbot/         # New chatbot components directory
│       ├── ChatContainer.tsx    # Main container component
│       ├── ChatWidget.tsx       # The chat UI component
│       ├── SelectionTooltip.tsx # Text selection tooltip
│       ├── Mascot.tsx           # Mascot image component
│       └── types.ts             # TypeScript type definitions
├── hooks/               # Custom React hooks
│   └── useTextSelection.ts      # Text selection hook
└── client-modules/      # Docusaurus client modules
    └── Root.js          # Docusaurus root component injection point
```

**Structure Decision**: Web application frontend component with isolated structure in src/components/Chatbot/ to maintain clear boundaries from existing Docusaurus components. Components will be integrated via Docusaurus Root.js using a safe wrapper approach.

## Phase 0: Research & Analysis

### Existing Components Analysis
- **Task**: Investigate any existing chatbot components in the codebase that may not be rendering properly
- **Task**: Analyze current Docusaurus structure and component integration patterns
- **Task**: Research OpenAI ChatKit React SDK integration patterns and best practices
- **Task**: Investigate SSR-safe component patterns for Docusaurus applications

### Technology Research
- **Task**: Research accessibility best practices for chatbot UI components (WCAG 2.1 AA)
- **Task**: Investigate responsive design patterns for chatbot widgets across device sizes
- **Task**: Explore error handling strategies for external SDK failures
- **Task**: Examine text selection API implementation patterns for tooltip positioning
- **Task**: Study official ChatKit setup documentation: https://platform.openai.com/docs/guides/chatkit

### Pre-Implementation Setup
- **Task**: Set up OpenAI ChatKit account following official documentation
- **Task**: Configure API keys and authentication methods
- **Task**: Set up rate limits and usage settings for the project
- **Task**: Document production configuration requirements

## Phase 1: Design & Architecture

### Component Architecture
- **Main Container**: ChatContainer.tsx - Entry point that handles state management and coordinates child components
- **Chat Widget**: ChatWidget.tsx - The main chat interface with proper styling and mascot positioning
- **Selection ToolTip**: SelectionTooltip.tsx - Floating button that appears when text is selected
- **Mascot Component**: Mascot.tsx - Positioned mascot image that peeks over chat bubbles
- **Hooks**: Custom hooks for text selection detection and state management

### Data Flow Design
- **Text Selection**: Browser text selection API → Custom event dispatch → Chatbot initialization
- **State Management**: React Context API for managing chat state, visibility, and selected text
- **Event Communication**: Custom 'aibook:open-with-context' events for communication between text and chatbot

### Styling Architecture
- **CSS Framework**: Tailwind CSS utility classes exclusively (no custom CSS files)
- **Responsive Design**: Mobile-first approach with responsive breakpoints
- **Accessibility**: ARIA labels, keyboard navigation, focus management
- **Theme Integration**: Purple/indigo gradient matching mockup design

## Phase 2: Implementation Strategy

### Integration Approach
- **Global Injection**: Safe wrapper approach in Docusaurus Root.js to inject chatbot component
- **SSR Safety**: All components wrapped in <BrowserOnly> to prevent SSR issues
- **Event Bus**: window.dispatchEvent for communication between book text and chatbot
- **Code Isolation**: All new code in src/components/Chatbot/ to prevent regressions

### Error Handling Design
- **SDK Failures**: Fallback UI with user notifications when ChatKit fails to initialize
- **Network Errors**: Retry mechanisms with appropriate user feedback
- **Text Truncation**: 200 character limit with clear user feedback when exceeded
- **Graceful Degradation**: Chatbot remains functional even when external services fail

### Mobile Responsiveness
- **Responsive Layout**: Flexible chat window that adapts to different screen sizes
- **Touch Optimization**: Larger touch targets for mobile users
- **Viewport Handling**: Proper positioning and sizing on mobile screens
- **Orientation Changes**: Handling of screen rotation and layout adjustments

## Phase 3: Implementation & Testing

### Component Development
- **ChatContainer**: SSR-safe wrapper using BrowserOnly to prevent build errors
- **ChatWidget**: Main chat interface with proper styling and mascot positioning
- **SelectionTooltip**: Text selection detection with proper positioning and 200 char limit
- **Mascot Component**: Animated mascot that peeks over chat bubbles
- **Custom Hooks**: Encapsulated logic for text selection, state management, and responsiveness

### Integration Testing
- **Docusaurus Integration**: Verify safe injection in Root.js without affecting existing functionality
- **SSR Safety**: Confirm no "window is not defined" errors during build process
- **Cross-browser Compatibility**: Test in Chrome, Firefox, Safari, and Edge
- **Mobile Responsiveness**: Verify proper behavior across all device sizes

### Quality Assurance
- **Accessibility Testing**: Automated and manual verification of WCAG 2.1 AA compliance
- **Performance Testing**: Verify <100ms response time for text selection
- **Error Handling**: Test fallback UI and error recovery scenarios
- **Text Truncation**: Verify 200-character limit with proper user feedback

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| External SDK Dependency (@openai/chatkit-react) | Required to meet core requirement of using OpenAI ChatKit SDK | Building custom chat UI would require significantly more effort and not meet spec requirement |
| Global DOM Injection (Root.js) | Required for global text selection functionality across all pages | Component-by-component integration would miss text selection on pages without explicit imports |
| Clean-slate Implementation | Required to avoid issues with existing non-functional components | Relying on existing broken components would compromise quality and requirements compliance |

## Constitution Compliance Verification

### ✅ Security First
- [x] No hardcoded credentials in implementation
- [x] Input sanitization for selected text
- [x] Proper isolation of mock clientSecret

### ✅ Source of Truth
- [x] Mock responses properly isolated for UI development
- [x] Future integration path defined for textbook content

### ✅ Working Software Priority
- [x] Focus on functional UI components
- [x] Text selection and chat functionality prioritized

### ✅ Modularity & Separation
- [x] Components isolated in src/components/Chatbot/
- [x] Clear boundaries from existing Docusaurus components
- [x] Modular component architecture

### ✅ Test-Driven Development
- [x] Unit tests planned for component functionality
- [x] Accessibility tests included
- [x] Integration tests for Docusaurus compatibility

### ✅ Clear Naming & Conventions
- [x] React components use PascalCase
- [x] Consistent with project standards
- [x] Meaningful variable and function names