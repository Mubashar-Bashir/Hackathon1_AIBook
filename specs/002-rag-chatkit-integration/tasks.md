# Implementation Tasks: RAG Integration with ChatKit UI using OpenAI Function Calling

**Feature**: RAG Integration with ChatKit UI using OpenAI Function Calling
**Spec**: [specs/002-rag-chatkit-integration/spec.md](specs/002-rag-chatkit-integration/spec.md)
**Branch**: `002-rag-chatkit-integration`
**Input**: Build and embed a Retrieval-Augmented Generation (RAG) chatbot within the published book using OpenAI Function Calling, ChatKit UI, FastAPI, Neon Serverless Postgres database, and Qdrant Cloud Free Tier.

## Dependencies

- Neon Serverless Postgres must be configured and accessible
- Qdrant Cloud must be configured and accessible
- OpenAI API key must be available
- Cohere API key must be available for embeddings

## Implementation Strategy

This feature will be implemented incrementally following the user story priorities:
- **Phase 1**: MVP with basic RAG functionality (User Story 1)
- **Phase 2**: Content pipeline automation (User Story 2)
- **Phase 3**: OpenAI Function Calling enhancement (User Story 3)

## Phase 1: Setup and Project Structure

- [ ] T001 Create backend/src/rag_chatkit directory structure
- [ ] T002 Add OpenAI, Cohere, qdrant-client to backend/requirements.txt
- [ ] T003 Create backend/src/config/rag_config.py for RAG-specific settings
- [ ] T004 Set up environment variables documentation for new services

## Phase 2: Foundational Components

- [ ] T005 Create backend/src/models/chat.py with ChatMessage and ChatSession models
- [ ] T006 Create backend/src/models/content.py with BookContent and TextChunk models
- [ ] T007 Create backend/src/models/user.py with User and AnonymousSession models
- [ ] T008 Implement database service in backend/src/services/database_service.py
- [ ] T009 Implement vector store service in backend/src/services/vector_store_service.py
- [ ] T010 Create embedding service in backend/src/services/embedding_service.py

## Phase 3: [US1] Interactive Book Learning with RAG Chatbot

### Models and Services
- [ ] T011 [US1] Implement RAG service in backend/src/services/rag_service.py
- [ ] T012 [US1] Create content retrieval service in backend/src/services/content_service.py
- [ ] T013 [US1] Add context handling to RAG service for selected text vs full book

### API Endpoints
- [ ] T014 [US1] Create chatbot API router in backend/src/api/chatbot.py
- [ ] T015 [US1] Implement query endpoint with full book context in backend/src/api/chatbot.py
- [ ] T016 [US1] Implement query endpoint with selected text context in backend/src/api/chatbot.py

### Frontend Integration
- [ ] T017 [P] [US1] Set up ChatKit dependencies in book/package.json
- [ ] T018 [P] [US1] Create ChatKitWrapper component in book/src/components/ChatKitWrapper.jsx
- [ ] T019 [US1] Connect ChatKitWrapper to backend API endpoints
- [ ] T020 [US1] Implement text selection handling in ChatKitWrapper

## Phase 4: [US2] Automated Content Pipeline

### Document Fetching
- [x] T021 [P] [US2] Create document fetcher service in backend/src/utils/document_fetcher.py
- [x] T022 [P] [US2] Implement sitemap/XML parsing in backend/src/utils/document_fetcher.py
- [x] T023 [US2] Create URL crawler for Vercel/GitHub content in backend/src/utils/document_fetcher.py

### Content Processing
- [x] T024 [P] [US2] Implement content chunking service in backend/src/services/content_service.py
- [x] T025 [P] [US2] Create text cleaning and preprocessing in backend/src/services/content_service.py
- [x] T026 [US2] Configure optimal chunk size parameters (~512-1024 tokens)

### Storage Pipeline
- [x] T027 [P] [US2] Create embedding pipeline service in backend/src/services/content_service.py
- [x] T028 [P] [US2] Implement parallel embedding generation in backend/src/services/content_service.py
- [x] T029 [US2] Create storage coordination service in backend/src/services/content_service.py

### Automation
- [x] T030 [US2] Create scheduled pipeline runner in backend/src/services/content_service.py
- [x] T031 [US2] Implement on-demand pipeline trigger endpoint in backend/src/api/content_pipeline.py

## Phase 5: [US3] OpenAI Function Calling Integration

### Function Definitions
- [x] T032 [US3] Create RAG retrieval function in backend/src/services/rag_service.py
- [x] T033 [US3] Implement content search function in backend/src/services/rag_service.py
- [x] T034 [US3] Create context synthesis function in backend/src/services/rag_service.py

### Integration
- [x] T035 [US3] Integrate OpenAI Function Calling with RAG service in backend/src/services/rag_service.py
- [x] T036 [US3] Implement fallback to basic RAG when functions unavailable
- [x] T037 [US3] Add function calling orchestration to chatbot API
- [x] T069 Add function calling error handling and fallback logic documentation
- [x] T070 Implement function calling rate limiting and monitoring
- [ ] T071 Add function calling test coverage for edge cases

## Phase 6: Polish & Cross-Cutting Concerns

### Error Handling and Monitoring
- [x] T038 Implement comprehensive error handling across all services
- [x] T039 Create logging configuration for RAG pipeline in backend/src/utils/logging.py
- [x] T040 Implement graceful degradation when external services unavailable
- [x] T066 Add comprehensive error logging for content pipeline in backend/src/services/content_service.py
- [x] T067 Implement monitoring metrics for content pipeline performance in backend/src/services/content_service.py
- [x] T068 Add detailed error responses for content pipeline API endpoints in backend/src/api/content_pipeline.py

### Performance and Optimization
- [x] T041 Add caching layer for RAG responses in backend/src/services/cache_service.py
- [x] T042 Implement response time monitoring and metrics
- [x] T043 Optimize embedding generation performance

### Security
- [x] T044 [P] Implement input sanitization to prevent prompt injection
- [x] T045 [P] Add rate limiting for API endpoints
- [x] T046 Validate and sanitize user-selected text context
- [x] T053 [P] Implement API rate limiting for chatbot endpoints in backend/src/middleware/rate_limit.py
- [x] T054 [P] Add request validation and sanitization middleware in backend/src/middleware/validation.py
- [x] T055 Implement secure session handling with proper expiration in backend/src/services/session_service.py
- [x] T056 Add security headers to FastAPI application in backend/main.py
- [x] T057 Implement proper error masking to prevent information disclosure in backend/src/middleware/error_handler.py
- [x] T058 Add input validation for all API endpoints with Pydantic models in backend/src/api/chatbot.py
- [x] T059 Implement secure API key handling and rotation mechanism in backend/src/config/rag_config.py
- [x] T060 Add audit logging for security-relevant events in backend/src/utils/logging.py

### Authentication
- [ ] T047 [US3] Implement optional authentication middleware in backend/src/middleware/auth.py
- [ ] T048 [US3] Create authentication endpoints in backend/src/api/auth.py for optional login
- [ ] T049 [US3] Implement session management for both anonymous and authenticated users in backend/src/services/session_service.py
- [ ] T050 [US3] Add user preference storage and retrieval in backend/src/services/user_service.py
- [ ] T051 [US3] Modify ChatSession model to support authenticated sessions in backend/src/models/chat.py
- [ ] T052 [US3] Update frontend to support optional authentication flow in book/src/components/ChatKitWrapper.jsx

### Testing and Quality
- [ ] T061 Create unit tests for RAG service in backend/tests/test_rag_service.py
- [ ] T062 Create integration tests for chatbot API in backend/tests/test_chatbot_api.py
- [ ] T063 Implement accuracy testing for responses
- [ ] T064 Create performance benchmarks for response times

### Documentation
- [ ] T065 Update API documentation for new endpoints
- [ ] T066 Create deployment guide for RAG components
- [ ] T067 Document content pipeline automation process

## Parallel Execution Examples

**Parallelizable Tasks (can run simultaneously):**
- T005, T006, T007: Model creation tasks
- T017, T018: Frontend component setup
- T021, T022: Document fetching components
- T024, T025: Content processing components
- T032, T033: Function tool creation

**Sequential Dependencies:**
- T001-T004 must complete before T005-T009
- T005-T009 must complete before T011-T020
- T011-T020 should complete before T021-T031
- T021-T031 should complete before T032-T037
- T032-T037 should complete before T047-T060 (security/auth dependencies)

## Independent Test Criteria

**User Story 1 Complete When:**
- Students can interact with ChatKit UI chatbot
- Chatbot answers questions based on book content
- Chatbot answers questions based only on selected text
- UI provides smooth, responsive experience

**User Story 2 Complete When:**
- Automated pipeline fetches content from Vercel/GitHub
- Content is properly chunked and embedded
- Vectors are stored in Qdrant Cloud with metadata in Neon Postgres

**User Story 3 Complete When:**
- OpenAI Function Calling processes complex, multi-step queries
- Functions coordinate with RAG system appropriately
- System falls back to basic RAG when functions unavailable