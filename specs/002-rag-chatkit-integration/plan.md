# Implementation Plan: RAG Integration with ChatKit UI using OpenAI Function Calling

**Branch**: `002-rag-chatkit-integration` | **Date**: 2025-12-13 | **Spec**: [specs/002-rag-chatkit-integration/spec.md](specs/002-rag-chatkit-integration/spec.md)
**Input**: Build and embed a Retrieval-Augmented Generation (RAG) chatbot within the published book using OpenAI Function Calling, ChatKit UI, FastAPI, Neon Serverless Postgres database, and Qdrant Cloud Free Tier. The chatbot must be able to answer user questions about the book's content, including answering questions based only on text selected by the user. This includes document fetching from Vercel/GitHub via sitemap/XML, chunking, embedding, and storage automation.

## Summary

Implement a comprehensive RAG system with ChatKit UI integration for the Physical AI & Humanoid Robotics textbook. The system will feature automated document fetching from Vercel/GitHub, content processing pipeline with chunking and embedding, storage in Qdrant Cloud with metadata in Neon Postgres, OpenAI Function Calling for advanced reasoning, and a responsive ChatKit UI. The solution will support both anonymous access and authenticated personalized features with proper error handling and performance optimization.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript (Node.js 18+), Markdown
**Primary Dependencies**:
- Backend: FastAPI 0.104+, Pydantic 2.x, asyncpg, SQLAlchemy, qdrant-client, cohere, openai, beautifulsoup4, requests
- Frontend: Docusaurus 3.x, React 18+, ChatKit components, axios
**Storage**: Neon Serverless Postgres (user data, metadata, content references), Qdrant Cloud (vector embeddings)
**Testing**: pytest for backend, Jest for frontend, Playwright for E2E tests
**Target Platform**: Web-based (GitHub Pages for frontend, cloud services for backend)
**Project Type**: Full-stack web application with microservices architecture
**Performance Goals**: <3s response time for 95% of queries, sub-2s page load, <5s content pipeline execution
**Constraints**: GitHub Pages static site limitations, Cohere/OpenAI/Qdrant API rate limits, Vercel/GitHub content access patterns
**Scale/Scope**: 1000 concurrent users, 10k+ textbook page views, 500+ daily chatbot queries

## Constitution Check

### Gate 1: User-Centric Design
✅ PASS: RAG chatbot with ChatKit UI prioritizes the learning experience of students with interactive Q&A capabilities.

### Gate 2: Clarity & Accessibility
✅ PASS: Content will be accessible with anonymous access for basic functionality and optional authentication for advanced features.

### Gate 3: Technical Accuracy
✅ PASS: Using established technologies (FastAPI, Qdrant, Cohere, OpenAI, Docusaurus) with proper documentation and testing.

### Gate 4: Efficiency & Performance
✅ PASS: Performance goals defined (<3s response times) with caching for offline functionality and optimized vector search.

### Gate 5: Security by Design
✅ PASS: Optional authentication for personalized features, with proper input sanitization and rate limiting.

### Gate 6: Maintainability & Scalability
✅ PASS: Separation of concerns between frontend (Docusaurus) and backend (FastAPI), with cloud-native architecture.

### Gate 7: Modularity & Reusability
✅ PASS: Component-based architecture with clear API contracts between services.

### Gate 8: Code Quality Standards
✅ PASS: Following established style guides and documentation practices as per constitution.

### Gate 9: Testing & Validation
✅ PASS: Unit, integration, and E2E testing planned with pytest, Jest, and Playwright.

### Gate 10: Architectural Principles
✅ PASS: Clear separation between Docusaurus frontend, RAG backend, database, vector store, and OpenAI integration services.

### Gate 11: Security & Privacy
✅ PASS: Optional authentication, with plans for data protection and input validation.

### Gate 12: Documentation & Knowledge Sharing
✅ PASS: Following the spec-plan-tasks documentation pattern with PHRs and potential ADRs.

## Project Structure

### Documentation (this feature)
```text
specs/002-rag-chatkit-integration/
├── plan.md              # This file
├── research.md          # Research and technology decisions
├── data-model.md        # Entity relationships and schemas
├── quickstart.md        # Setup and deployment instructions
├── contracts/           # API contracts
└── tasks.md             # Implementation tasks
```

### Source Code
```text
# Full-stack application
book/
├── src/
│   ├── components/
│   │   ├── ChatKitWrapper.jsx      # ChatKit UI integration
│   │   ├── RAGChatbot.jsx          # RAG chatbot component
│   │   └── TextSelectionHandler.jsx # Text selection context handler
│   └── pages/
├── docusaurus.config.js
├── package.json
└── sidebars.js

backend/
├── src/
│   ├── models/                    # Data models
│   │   ├── chat.py               # ChatMessage, ChatSession
│   │   ├── content.py            # BookContent, TextChunk
│   │   └── user.py               # User, Session models
│   ├── services/                  # Business logic
│   │   ├── rag_service.py        # RAG processing
│   │   ├── embedding_service.py  # Embedding generation
│   │   ├── content_service.py    # Content fetching and processing
│   │   ├── vector_store_service.py # Qdrant operations
│   │   └── database_service.py   # Neon Postgres operations
│   ├── tools/                     # OpenAI Function Calling tools
│   │   ├── rag_tool.py           # RAG retrieval function
│   │   └── content_tool.py       # Content processing functions
│   ├── api/                       # FastAPI endpoints
│   │   ├── chatbot.py            # Chatbot endpoints
│   │   ├── content_pipeline.py   # Content pipeline endpoints
│   │   └── auth.py               # Authentication endpoints
│   └── utils/                     # Utility functions
│       ├── document_fetcher.py   # Web scraping utilities
│       ├── chunker.py            # Text chunking utilities
│       └── logger.py             # Logging utilities
├── main.py                       # FastAPI application
├── requirements.txt              # Dependencies
└── tests/                        # Test suite

.history/                         # Prompt History Records
└── prompts/
    └── 002-rag-chatkit-integration/
        └── *.prompt.md
```

## Phase 0: Research & Technology Decisions

### Research Findings

**Decision**: Use OpenAI Function Calling instead of Assistants API
**Rationale**: Function Calling provides more direct control over the RAG process and better integration with existing backend services
**Alternatives considered**: OpenAI Assistants API (more managed but less flexible), LangChain agents (more complex setup)

**Decision**: Implement dual storage approach (Qdrant for embeddings, Neon for metadata)
**Rationale**: Qdrant optimized for vector similarity search, Neon for structured metadata and relationships
**Alternatives considered**: Single database approach (less optimal for vector operations)

**Decision**: Use BeautifulSoup and requests for content fetching
**Rationale**: Reliable for static site content extraction from Vercel/GitHub
**Alternatives considered**: Puppeteer (more complex, for dynamic content), Scrapy (overkill for this use case)

## Phase 1: Data Models and API Contracts

### Data Model Summary

- **ChatMessage**: User and bot messages with timestamps and metadata
- **ChatSession**: Session tracking with anonymous or authenticated users
- **BookContent**: Raw content from source with URL and metadata
- **TextChunk**: Processed content chunks with embedding references
- **Embedding**: Vector representation linked to content chunks
- **User**: Optional authenticated user with preferences
- **ContentReference**: Links between content chunks and source locations

### API Contract Summary

- **Chatbot API**: `/api/chatbot/query` - Process queries with RAG
- **Content Pipeline API**: `/api/content/fetch` - Trigger content ingestion
- **Authentication API**: `/api/auth` - User authentication endpoints

## Generated Artifacts

- **Research**: [research.md](./research.md) - Technology research and decision rationale
- **Data Model**: [data-model.md](./data-model.md) - Detailed entity relationships and schemas
- **API Contracts**: [contracts/](./contracts/) - OpenAPI specifications
- **Quickstart Guide**: [quickstart.md](./quickstart.md) - Development setup and deployment instructions