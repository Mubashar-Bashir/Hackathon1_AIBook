# Research: AIBOOK ChatKit UI Frontend (Layer-2)

## Decision: Clean-slate Implementation Approach
**Rationale**: Previous components may have rendering issues or architectural problems. Clean implementation ensures all requirements are properly met without inheriting legacy issues.
**Alternatives considered**:
- Fix existing components (rejected due to unknown state and potential technical debt)
- Hybrid approach (rejected due to complexity and risk of inheriting issues)

## Decision: OpenAI ChatKit React SDK Integration
**Rationale**: Required by spec to use OpenAI ChatKit SDK. The @openai/chatkit-react package provides the necessary UI components. Proper setup requires following the official documentation: https://platform.openai.com/docs/guides/chatkit
**Alternatives considered**:
- Custom chat UI implementation (rejected due to time constraints and spec requirement)
- Alternative chat SDKs (rejected due to spec requirement for OpenAI ChatKit)

## Decision: ChatKit Account Setup
**Rationale**: Before implementing the UI, a proper ChatKit account and project setup is required following the official guide. This includes API keys, authentication, and rate limits configuration.
**Alternatives considered**:
- Skip account setup (rejected as it's required for production)
- Use alternative authentication methods (rejected as it must follow official guide)

## Decision: SSR-Safe Component Architecture
**Rationale**: Docusaurus requires SSR compatibility. BrowserOnly wrapper ensures no "window is not defined" errors during build.
**Alternatives considered**:
- Client-side only rendering (rejected due to Docusaurus SSR requirements)
- Dynamic imports without BrowserOnly (rejected due to potential build errors)

## Decision: Text Selection API Implementation
**Rationale**: Browser native Selection API provides reliable text selection detection across all modern browsers.
**Alternatives considered**:
- Custom text selection logic (rejected due to complexity and browser compatibility issues)
- Third-party text selection libraries (rejected due to added dependencies and potential conflicts)

## Decision: WCAG 2.1 AA Compliance
**Rationale**: Accessibility is critical for educational content. WCAG 2.1 AA ensures usability for users with disabilities.
**Alternatives considered**:
- Basic accessibility only (rejected due to compliance requirements)
- WCAG 2.0 (rejected due to WCAG 2.1 being the current standard)

## Decision: Responsive Design Approach
**Rationale**: Mobile-first approach ensures proper functionality across all device sizes, critical for educational content access.
**Alternatives considered**:
- Desktop-first approach (rejected due to mobile usage trends)
- Separate mobile app (rejected due to single-platform requirement)

## Decision: Event-Driven Communication
**Rationale**: Custom events via window.dispatchEvent provide decoupled communication between text selection and chatbot without affecting Docusaurus architecture.
**Alternatives considered**:
- Context API (rejected due to global state complexity)
- Redux/Zustand (rejected due to over-engineering for simple communication)

## Decision: 200 Character Limit for Selection
**Rationale**: Prevents performance issues and ensures reasonable context for AI responses while providing clear user feedback.
**Alternatives considered**:
- No limit (rejected due to performance and UX concerns)
- Different character limits (100, 500) - rejected due to balance of usability and performance

## Decision: Tailwind CSS Only for Styling
**Rationale**: Consistent with project constraints. No changes to existing CSS files, using Tailwind utility classes exclusively.
**Alternatives considered**:
- Custom CSS files (rejected due to constraint violation)
- CSS modules (rejected due to constraint violation)

## Decision: Mock ClientSecret for SDK
**Rationale**: Required for UI rendering without live backend. Properly isolated to prevent security issues in mock implementation.
**Alternatives considered**:
- No client secret (rejected due to SDK requirements)
- Environment variable (rejected due to no backend requirement)