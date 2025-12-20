<!--
SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0 (major consolidation)
List of modified principles: Consolidated original 7 principles into 6 focused principles + added new technical standards
Added sections: Working Software Priority, Technical Standards section, Error Prevention Rules, Educational Content Principles
Removed sections: None (incorporated all essential elements into new structure)
Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md (Constitution Check sections updated)
Follow-up TODOs: None
-->

# AIBOOK Constitution

## Core Principles

### 1. Security First
- No hardcoded credentials; all secrets must be managed via environment variables
- All user inputs must be validated to prevent injection attacks and other vulnerabilities
- Encrypt sensitive data at rest and in transit

### 2. Source of Truth
- Deployed Docusaurus content serves as the single source of truth for RAG knowledge
- AI responses must be strictly grounded in verified textbook content (no hallucinations)
- All textbook content must be accurate and technically correct

### 3. Working Software Priority
- Deliver functional features over comprehensive documentation
- Focus on working chatbot UI that responds to user queries about the textbook content
- Working software is the primary measure of progress

### 4. Modularity & Separation
- Separate Python files for FastAPI, Cohere, Qdrant, and Agent logic
- Clear boundaries between Docusaurus frontend, RAG backend, and authentication
- Components should be modular and independently testable

### 5. Test-Driven Development
- Minimum 80% test coverage for RAG and API modules
- All critical functions and components must have unit tests
- Integration tests verify interaction between frontend and RAG backend

### 6. Clear Naming & Conventions
- React components: PascalCase
- Python functions: snake_case with type hints
- Tailwind CSS: Use utility classes directly in JSX/TSX components
- Consistent, meaningful variable and function names required

## Technical Standards

### Stack Requirements
- Frontend: Docusaurus with Tailwind CSS
- Backend: FastAPI
- Vector Database: Qdrant Cloud
- Embeddings: Cohere
- Authentication: BetterAuth
- Database: Neon
- Deployment: GitHub Pages/Vercel (Frontend), Vercel/Railway (Backend)

### Code Quality
- All Python functions must include type hints
- Code must be clean, well-structured, and easy to understand
- Adhere to established style guides (Prettier, ESLint for JS; Black, Flake8 for Python)
- Clear API contracts for communication between services

## Development Workflow

### 1. Development Cycle
- Create feature branch from main
- Implement with tests and documentation
- Code review by another team member
- Merge only after all tests pass and review completed

### 2. Error Prevention Rules
- No commits directly to main branch
- All code changes must include tests
- Security vulnerabilities must be addressed before merging
- Code must pass linting and formatting checks
- Breaking changes require migration plans and justification

### 3. Conflict Resolution
- When principles conflict, prioritize user functionality (working chatbot UI)
- For technical disputes, default to the approach that's proven to work
- Regular team syncs to align on implementation approaches
- This constitution supersedes all other development practices

## Documentation & Knowledge Sharing

- Feature Specifications (`spec.md`): Define "what" is being built and "why"
- Implementation Plans (`plan.md`): Document "how" the feature will be built
- Task Lists (`tasks.md`): Break down implementation into actionable steps
- Prompt History Records (`history/prompts/`): Capture AI interactions for traceability
- User Documentation: The textbook itself serves as primary user documentation

## Educational Content Principles

### Content Creation
- Prioritize learning experience of the student
- Ensure information is clear, concise, and accessible to diverse audiences
- Maintain technical accuracy and reflect current best practices in AI and Robotics
- Include diagrams, screenshots, and visual aids to reinforce concepts

### Writing Standards
- Write with reader's comprehension as the primary goal
- Use proper formatting (lists, headings, emphasis) for readability
- Define all acronyms on first use
- Include detailed outlines before writing each section
- Conduct rigorous self-editing before publishing

## Governance

- All development practices must comply with this constitution
- Amendments require formal documentation and team approval
- All PRs and reviews must verify constitutional compliance
- Regular constitution reviews after each major release
- Use project documentation for runtime development guidance

**Version**: 2.0.0 | **Ratified**: 2025-12-19 | **Last Amended**: 2025-12-19