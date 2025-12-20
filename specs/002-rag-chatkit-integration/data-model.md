# Data Model: RAG Integration with ChatKit UI

## Entity Definitions

### ChatMessage
- **id**: UUID (Primary Key)
- **session_id**: UUID (Foreign Key to ChatSession)
- **sender_type**: Enum (user | bot)
- **content**: Text
- **timestamp**: DateTime
- **metadata**: JSON (additional context, source references)

### ChatSession
- **id**: UUID (Primary Key)
- **user_id**: UUID (Foreign Key to User, nullable for anonymous sessions)
- **created_at**: DateTime
- **updated_at**: DateTime
- **context_type**: Enum (full_book | selected_text | custom)
- **selected_text**: Text (nullable, for selected text context)

### User
- **id**: UUID (Primary Key)
- **email**: String (nullable)
- **name**: String (nullable)
- **created_at**: DateTime
- **preferences**: JSON (personalization settings)

### BookContent
- **id**: UUID (Primary Key)
- **url**: String (source URL)
- **title**: String
- **content_text**: Text (raw content)
- **created_at**: DateTime
- **updated_at**: DateTime
- **metadata**: JSON (source info, processing status)

### TextChunk
- **id**: UUID (Primary Key)
- **content_id**: UUID (Foreign Key to BookContent)
- **chunk_text**: Text
- **chunk_index**: Integer
- **token_count**: Integer
- **embedding_id**: String (reference to Qdrant vector ID)
- **created_at**: DateTime

### EmbeddingReference
- **id**: String (Qdrant vector ID)
- **chunk_id**: UUID (Foreign Key to TextChunk)
- **embedding_model**: String
- **created_at**: DateTime

### ContentReference
- **id**: UUID (Primary Key)
- **url**: String
- **title**: String
- **section_path**: String (path within the book structure)
- **last_fetched**: DateTime
- **status**: Enum (pending | processing | completed | failed)

### AgentTask
- **id**: UUID (Primary Key)
- **session_id**: UUID (Foreign Key to ChatSession)
- **task_type**: String (function_call type)
- **parameters**: JSON (function parameters)
- **status**: Enum (pending | executing | completed | failed)
- **result**: JSON (nullable, function result)
- **created_at**: DateTime

## Relationships

### ChatSession → ChatMessage
- One-to-Many relationship
- ChatSession can have multiple ChatMessage records

### User → ChatSession
- One-to-Many relationship (optional)
- User can have multiple ChatSession records, but ChatSession can be anonymous

### BookContent → TextChunk
- One-to-Many relationship
- One BookContent can be split into multiple TextChunk records

### TextChunk → EmbeddingReference
- One-to-One relationship
- Each TextChunk has one corresponding EmbeddingReference

### ContentReference → BookContent
- One-to-One relationship
- Each ContentReference points to one BookContent record

### ChatSession → AgentTask
- One-to-Many relationship
- ChatSession can trigger multiple AgentTask records

## Indexes

### ChatMessage
- Index on `session_id` for efficient session-based queries
- Index on `timestamp` for chronological ordering

### ChatSession
- Index on `user_id` for user-specific queries
- Index on `updated_at` for recent session queries

### BookContent
- Index on `url` for unique content identification
- Index on `updated_at` for freshness checks

### TextChunk
- Index on `content_id` for content-based queries
- Index on `chunk_index` for ordered retrieval

### ContentReference
- Index on `url` for duplicate prevention
- Index on `last_fetched` for update scheduling

## Constraints

### ChatMessage
- `sender_type` must be either 'user' or 'bot'
- `content` length must be between 1 and 10,000 characters

### ChatSession
- If `context_type` is 'selected_text', then `selected_text` must not be null

### TextChunk
- `token_count` must be between 100 and 2000 (enforcing chunk size limits)
- `chunk_index` must be non-negative

### ContentReference
- `status` must be one of the defined enum values
- `url` must be a valid URL format

## Validation Rules

### Content Integrity
- TextChunk content must be derived from its parent BookContent
- EmbeddingReference must exist when TextChunk is marked as processed

### Session Management
- Anonymous sessions should expire after 24 hours of inactivity
- Authenticated sessions can have extended lifetime based on user preferences

### Rate Limiting
- Users should be limited to 100 messages per hour
- Content fetching should be limited to prevent overloading source sites