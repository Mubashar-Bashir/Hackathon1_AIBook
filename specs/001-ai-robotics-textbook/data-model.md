# Data Model: Physical AI & Humanoid Robotics Textbook

## Entities

### User
**Description**: Represents a registered user of the textbook system

**Fields**:
- `id` (string): Unique identifier for the user
- `email` (string): User's email address (primary login)
- `name` (string): User's full name
- `background` (string): User's experience level (beginner, intermediate, expert)
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last update timestamp
- `preferences` (json): User preferences including language settings

**Validation**:
- Email must be valid format
- Background must be one of: "beginner", "intermediate", "expert"
- Name cannot be empty

**Relationships**:
- One-to-many with UserSession (user can have multiple sessions)
- One-to-many with ChatbotInteraction (user can have multiple interactions)

### UserSession
**Description**: Represents an authenticated user session

**Fields**:
- `id` (string): Unique identifier for the session
- `user_id` (string): Reference to the user
- `token` (string): Session token
- `created_at` (datetime): Session creation timestamp
- `expires_at` (datetime): Session expiration timestamp

**Validation**:
- Token must be unique
- Expiration must be in the future

**Relationships**:
- Many-to-one with User (belongs to user)

### ChatbotQuery
**Description**: Represents a query sent to the RAG chatbot

**Fields**:
- `id` (string): Unique identifier for the query
- `user_id` (string): Reference to the user who made the query (optional for anonymous)
- `query_text` (string): The original query text
- `context` (string): Context provided to the chatbot (full book or selected text)
- `created_at` (datetime): Query creation timestamp
- `source_page` (string): URL or identifier of the page where query was made

**Validation**:
- Query text must not be empty
- Context must be provided

**Relationships**:
- Many-to-one with User (optional - can be anonymous)
- One-to-one with ChatbotResponse (query generates one response)

### ChatbotResponse
**Description**: Represents a response from the RAG chatbot

**Fields**:
- `id` (string): Unique identifier for the response
- `query_id` (string): Reference to the original query
- `response_text` (string): The chatbot's response text
- `sources` (array): List of source documents/chunks used to generate response
- `created_at` (datetime): Response creation timestamp
- `confidence_score` (float): Confidence level of the response (0.0-1.0)

**Validation**:
- Response text must not be empty
- Confidence score must be between 0.0 and 1.0

**Relationships**:
- Many-to-one with ChatbotQuery (belongs to query)

### TextbookChapter
**Description**: Represents a chapter in the textbook

**Fields**:
- `id` (string): Unique identifier for the chapter
- `title` (string): Chapter title
- `content` (string): Chapter content in Markdown format
- `content_urdu` (string): Chapter content translated to Urdu (optional)
- `module` (string): Module this chapter belongs to
- `order` (integer): Chapter's position in the textbook
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Validation**:
- Title must not be empty
- Content must not be empty
- Order must be a positive integer

**Relationships**:
- One-to-many with ChapterPersonalization (chapter can have multiple personalizations)

### ChapterPersonalization
**Description**: Represents personalized content for a chapter based on user background

**Fields**:
- `id` (string): Unique identifier
- `chapter_id` (string): Reference to the chapter
- `background_level` (string): User background level (beginner, intermediate, expert)
- `personalized_content` (string): Personalized content for this background level
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Validation**:
- Background level must be one of: "beginner", "intermediate", "expert"
- Personalized content must not be empty

**Relationships**:
- Many-to-one with TextbookChapter (belongs to chapter)

### VectorEmbedding
**Description**: Represents a vector embedding of text content for RAG search

**Fields**:
- `id` (string): Unique identifier for the embedding
- `content_id` (string): Reference to the original content (chapter ID or text block ID)
- `content_text` (string): Original text that was embedded
- `embedding_vector` (array): The actual embedding vector (will be stored in Qdrant)
- `created_at` (datetime): Creation timestamp
- `model_used` (string): Model used to generate the embedding

**Validation**:
- Content text must not be empty
- Embedding vector must have proper dimensions

**Relationships**:
- Many-to-one with TextbookChapter (content belongs to chapter)

### CachedResponse
**Description**: Represents cached responses to maintain functionality during service outages

**Fields**:
- `id` (string): Unique identifier
- `query_hash` (string): Hash of the original query for quick lookup
- `query_text` (string): Original query text
- `cached_response` (string): Cached response text
- `created_at` (datetime): Cache creation timestamp
- `expires_at` (datetime): Cache expiration timestamp
- `valid_until` (datetime): When this cache should be invalidated

**Validation**:
- Query hash must be unique
- Expiration must be in the future

**Relationships**:
- No direct relationships, standalone cache entries