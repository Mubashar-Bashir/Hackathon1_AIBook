# AIBook Backend Architecture Overview

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   External      │
│   (React)       │◄──►│   (FastAPI)      │◄──►│   Services      │
│                 │    │                  │    │                 │
│ • Chat Interface│    │ • Chatbot API    │    │ • Google Gemini │
│ • Auth UI       │    │ • Auth API       │    │ • Cohere API    │
│ • Content UI    │    │ • Content API    │    │ • Qdrant Cloud  │
│ • Settings      │    │ • RAG Monitor    │    │ • Neon DB       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Component Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Application                      │
├─────────────────────────────────────────────────────────────────┤
│ • main.py (Application Entry Point)                            │
│ • Middleware (CORS, Auth, Rate Limiting)                       │
│ • API Routes (/api/chatbot, /api/auth, /api/content)           │
└─────────────────────────────────────────────────────────────────┤
                              │
┌─────────────────────────────────────────────────────────────────┤
│                        Service Layer                            │
├─────────────────────────────────────────────────────────────────┤
│ • RAGService (Query processing, context handling)              │
│ • EmbeddingService (Vector search, similarity)                 │
│ • AuthService (User management, session handling)              │
│ • ContentService (Document processing, storage)                │
│ • CacheService (Response caching, optimization)                │
└─────────────────────────────────────────────────────────────────┤
                              │
┌─────────────────────────────────────────────────────────────────┤
│                        Data Layer                               │
├─────────────────────────────────────────────────────────────────┤
│ • Vector Store (Qdrant - textbook content)                     │
│ • Embedding API (Cohere - text vectorization)                  │
│ • Generation API (Gemini - response generation)                │
│ • User DB (Neon - user data, sessions)                         │
└─────────────────────────────────────────────────────────────────┘
```

## API Layer Architecture

### Chatbot API (`/api/chatbot`)
```
POST /api/chatbot/query          - Standard RAG query
POST /api/chatbot/stream-query   - Streaming RAG query (NEW)
GET  /api/chatbot/health         - Health check
GET  /api/chatbot/history/{id}   - Query history
```

### Authentication API (`/api/auth`)
```
POST /api/auth/register          - User registration
POST /api/auth/login             - User login
POST /api/auth/logout            - User logout
GET  /api/auth/profile           - User profile
PUT  /api/auth/profile           - Update profile
```

### Content Pipeline API (`/api/content`)
```
POST /api/content/fetch          - Fetch and process content
POST /api/content/chunk          - Process text chunks
GET  /api/content/stats          - Content statistics
```

### RAG Monitor API (`/api/monitor`)
```
WS   /api/monitor/rag-progress   - Real-time progress (WebSocket)
GET  /api/monitor/rag-status     - Current status
GET  /api/monitor/vector-stats   - Vector store stats
```

## Service Layer Architecture

### RAGService
```
┌─────────────────────────────────────────────────────────────────┐
│                        RAGService                               │
├─────────────────────────────────────────────────────────────────┤
│ Methods:                                                        │
│ • query_knowledge_base()        - Basic RAG query              │
│ • query_with_function_calling() - Enhanced reasoning           │
│ • process_query_with_enhanced_reasoning() - Smart routing      │
│ • stream_query_response()      - Streaming response (NEW)      │
│ • _generate_response()         - LLM response generation       │
│ • _calculate_confidence()      - Response confidence scoring   │
│ • _get_fallback_response()     - Error fallback handling       │
└─────────────────────────────────────────────────────────────────┘
```

### Key Dependencies
- **EmbeddingService**: For vector search and similarity
- **CacheService**: For response caching
- **ContentService**: For content retrieval functions
- **Google Gemini API**: For response generation
- **Qdrant Vector Store**: For content storage and retrieval

## Data Flow Architecture

### Standard Query Flow
```
User Query → Validation → Context Processing → Vector Search →
LLM Generation → Response Formatting → Cache Storage → Client Response
```

### Streaming Query Flow
```
User Query → Validation → Context Processing → Vector Search →
LLM Streaming Generation → SSE Formatting → Chunked Response →
Real-time Client Rendering
```

### Authentication Flow
```
User Credentials → Validation → Token Generation → Session Storage →
Response with Token → Subsequent Requests with Token →
Token Validation → Access Control
```

## Integration Points

### External Services
1. **Google Gemini API**: Response generation
2. **Cohere API**: Text embedding
3. **Qdrant Cloud**: Vector storage
4. **Neon Serverless Postgres**: User data storage

### Internal Services
1. **RAGService** ↔ **EmbeddingService**: Vector search
2. **AuthService** ↔ **UserService**: User management
3. **ContentService** ↔ **EmbeddingService**: Content processing
4. **CacheService** ↔ All services: Response optimization

## Security Architecture

### Authentication
- JWT tokens for session management
- Role-based access control
- Password hashing with bcrypt
- Session timeout handling

### Authorization
- Endpoint-level access control
- User-specific data isolation
- Rate limiting implementation
- Input validation and sanitization

### Data Protection
- Environment variable management
- Secure API key handling
- Database connection encryption
- Response sanitization

## Performance Architecture

### Caching Strategy
- Response caching for frequent queries
- Embedding caching for repeated searches
- Session caching for authentication
- CDN integration for static content

### Scaling Considerations
- Asynchronous request handling
- Connection pooling
- Load balancing readiness
- Database optimization

## Error Handling Architecture

### Error Types
- **Client Errors (4xx)**: Validation, authentication
- **Server Errors (5xx)**: API failures, internal errors
- **Service Errors**: External service unavailability
- **Streaming Errors**: Connection interruptions

### Error Recovery
- Graceful degradation
- Fallback responses
- Retry mechanisms
- User-friendly error messages

## Testing Architecture

### Test Layers
- **Unit Tests**: Individual function testing
- **Integration Tests**: Service interaction testing
- **E2E Tests**: Complete workflow testing
- **Performance Tests**: Load and stress testing

### Test Coverage
- API contract validation
- Service method testing
- Error scenario testing
- Performance benchmarking

---
*Architecture Document Version: 1.1*
*Last Updated: December 15, 2025*
*Next Review: On major architecture changes*