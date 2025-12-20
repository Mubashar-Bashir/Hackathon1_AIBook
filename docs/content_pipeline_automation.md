# Content Pipeline Automation

## Overview
This document describes the automated content pipeline for the Physical AI & Humanoid Robotics Textbook RAG system. The pipeline automatically fetches, processes, and stores textbook content to keep the knowledge base current.

## Pipeline Components

### 1. Document Fetcher
- **Purpose**: Fetch content from Vercel/GitHub via sitemap or XML
- **Location**: `backend/src/utils/document_fetcher.py`
- **Functionality**:
  - Parse sitemap.xml to discover content URLs
  - Extract text content from HTML pages
  - Handle different content types and structures

### 2. Content Processor
- **Purpose**: Process raw content into chunks for RAG
- **Location**: `backend/src/services/content_service.py`
- **Functionality**:
  - Text cleaning and preprocessing
  - Content chunking with optimal size parameters
  - Metadata extraction and preservation

### 3. Embedding Generator
- **Purpose**: Create vector embeddings for content chunks
- **Location**: `backend/src/services/embedding_service.py`
  - Generate embeddings using Cohere (with OpenAI fallback)
  - Store embeddings in vector database
  - Handle batch processing for efficiency

### 4. Storage Coordinator
- **Purpose**: Store processed content in appropriate databases
- **Location**: `backend/src/services/content_service.py`
- **Functionality**:
  - Store embeddings in Qdrant Cloud
  - Store metadata in Neon Postgres
  - Maintain content references and relationships

## Pipeline Workflow

### 1. Content Discovery
The pipeline starts by discovering content to process:
- Fetch sitemap.xml from the textbook URL
- Parse URLs for individual textbook pages/chapters
- Filter URLs to include only relevant content

### 2. Content Fetching
For each discovered URL:
- Fetch the HTML content
- Parse the content to extract text
- Clean and preprocess the text
- Extract relevant metadata (title, URL, etc.)

### 3. Content Chunking
The extracted content is chunked into smaller pieces:
- Target chunk size: 512-1024 tokens (configurable)
- Overlap between chunks: 20% to maintain context
- Preserve semantic boundaries where possible
- Generate chunk-level metadata

### 4. Embedding Generation
Each content chunk is processed to create embeddings:
- Use Cohere embedding model (embed-english-v3.0)
- Fallback to OpenAI if Cohere is unavailable
- Generate embeddings in batches for efficiency
- Store embedding vectors with content references

### 5. Storage and Indexing
Processed content is stored in the appropriate systems:
- Embedding vectors stored in Qdrant Cloud
- Content metadata stored in Neon Postgres
- Maintain relationships between content chunks
- Update search indexes for fast retrieval

## Automation Methods

### 1. Scheduled Automation
The pipeline can run on a schedule:
- Use cron jobs for regular updates
- Configure frequency based on content update patterns
- Run during off-peak hours to minimize impact

Example cron job:
```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/backend && source venv/bin/activate && python -c "..."
```

### 2. Event-Driven Automation
The pipeline can be triggered by events:
- Content updates detected
- Manual trigger via API
- Integration with CI/CD for content changes

### 3. On-Demand Automation
The pipeline can be triggered manually:
- API endpoint: `POST /api/content/fetch`
- Command-line interface
- Admin dashboard interface

## Configuration Parameters

### Chunking Parameters
- `CHUNK_SIZE`: Target size for content chunks (default: 512 tokens)
- `CHUNK_OVERLAP`: Overlap percentage between chunks (default: 20%)
- `MIN_CHUNK_SIZE`: Minimum chunk size (default: 100 tokens)
- `MAX_CHUNK_SIZE`: Maximum chunk size (default: 2000 tokens)

### Processing Parameters
- `BATCH_SIZE`: Number of chunks to process simultaneously (default: 10)
- `REQUEST_TIMEOUT`: Timeout for content fetching (default: 30 seconds)
- `RETRY_ATTEMPTS`: Number of retry attempts for failed operations (default: 3)

### Quality Parameters
- `MIN_CONTENT_LENGTH`: Minimum content length to process (default: 50 characters)
- `CONTENT_SIMILARITY_THRESHOLD`: Threshold for duplicate content detection (default: 0.9)

## API Endpoints

### Trigger Pipeline
```
POST /api/content/fetch
```

**Request Body:**
```json
{
  "base_url": "https://your-book-url.com",
  "sitemap_url": "https://your-book-url.com/sitemap.xml",
  "force_update": false,
  "content_filter": ["docs/*", "tutorials/*"]
}
```

**Parameters:**
- `base_url`: Base URL for the textbook
- `sitemap_url`: URL to sitemap.xml (optional, defaults to base_url/sitemap.xml)
- `force_update`: Whether to update existing content (default: false)
- `content_filter`: Patterns to include/exclude content (optional)

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "started",
  "total_documents": 42,
  "estimated_completion": "2023-12-13T11:30:00Z"
}
```

### Check Pipeline Status
```
GET /api/content/status/{job_id}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "completed",
  "progress": {
    "fetched": 42,
    "processed": 42,
    "embedded": 42,
    "stored": 42,
    "errors": 0
  },
  "completion_time": "2023-12-13T11:25:00Z",
  "results": {
    "documents_processed": 42,
    "chunks_created": 156,
    "embeddings_generated": 156
  }
}
```

### List Recent Jobs
```
GET /api/content/jobs
```

## Monitoring and Logging

### Pipeline Metrics
The system tracks various metrics:
- Documents processed per run
- Chunks created per document
- Embedding generation success rate
- Processing time per document
- Error rates and types

### Logging Configuration
- Detailed logs for each processing step
- Error logs with context for debugging
- Performance metrics logging
- Audit logs for content changes

### Health Checks
- Pipeline status monitoring
- External service availability
- Database connectivity checks
- Vector database connectivity

## Error Handling and Resilience

### Fetching Errors
- Retry failed requests with exponential backoff
- Skip inaccessible URLs with logging
- Handle rate limiting from source sites
- Graceful degradation when sources are unavailable

### Processing Errors
- Continue processing other documents if one fails
- Detailed error logging for failed documents
- Option to retry failed documents separately
- Preserve partial results from successful operations

### Storage Errors
- Rollback failed storage operations
- Retry storage operations with backoff
- Maintain data consistency across systems
- Alert on storage failures

## Performance Optimization

### Batch Processing
- Process multiple documents in parallel
- Batch embedding generation for efficiency
- Optimize database operations with bulk operations
- Use connection pooling for database access

### Caching Strategies
- Cache frequently accessed embeddings
- Cache processed content to avoid reprocessing
- Cache external API responses where appropriate
- Implement smart cache invalidation

### Resource Management
- Limit concurrent operations to prevent overload
- Monitor memory usage during processing
- Implement proper cleanup of temporary resources
- Use async operations where possible

## Security Considerations

### Content Validation
- Validate content before processing
- Sanitize fetched content to prevent injection
- Verify content type and size limits
- Filter out non-textual content appropriately

### API Security
- Rate limiting for pipeline triggers
- Authentication for administrative operations
- Input validation for all parameters
- Secure handling of credentials

### Data Privacy
- Ensure content complies with privacy requirements
- Handle personal information appropriately
- Maintain audit logs for content processing
- Secure storage of processed content

## Testing the Pipeline

### Unit Tests
- Test individual components in isolation
- Verify chunking algorithms
- Test error handling scenarios
- Validate content processing logic

### Integration Tests
- Test end-to-end pipeline functionality
- Verify database storage operations
- Test external API integrations
- Validate search functionality

### Performance Tests
- Test pipeline performance with large content sets
- Measure processing time and resource usage
- Test concurrent pipeline operations
- Verify system stability under load

## Troubleshooting

### Common Issues

#### Content Not Being Fetched
- **Check**: Verify sitemap.xml is accessible
- **Check**: Ensure base URL is correct
- **Check**: Verify network connectivity to source

#### Slow Processing Times
- **Check**: Database connection performance
- **Check**: External API response times
- **Check**: System resource utilization
- **Adjust**: Batch sizes and concurrency settings

#### Embedding Generation Failures
- **Check**: API key validity and rate limits
- **Check**: Network connectivity to embedding services
- **Check**: Content size and format
- **Verify**: Fallback service configuration

#### Search Quality Issues
- **Check**: Embedding quality and relevance
- **Check**: Chunk size and overlap settings
- **Check**: Content preprocessing quality
- **Adjust**: Similarity thresholds

### Debugging Tools
- Pipeline status monitoring
- Detailed logging with timestamps
- Performance profiling tools
- Database query analysis

## Maintenance Tasks

### Regular Maintenance
- Monitor pipeline execution logs
- Check for failed processing jobs
- Verify content freshness
- Review and update configuration parameters

### Periodic Optimization
- Analyze processing performance
- Optimize chunking parameters
- Update embedding models if needed
- Review and adjust batch sizes

### Content Updates
- Schedule regular content updates
- Monitor for new content additions
- Handle content structure changes
- Update content filtering rules as needed