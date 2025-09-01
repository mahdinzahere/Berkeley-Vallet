# Documentation for RAG Pipeline

This directory contains the documentation files used by the LangChain RAG (Retrieval-Augmented Generation) pipeline to provide intelligent, context-aware support responses to users.

## Purpose

The RAG pipeline enables the rideshare app to:
- Answer user questions with accurate, up-to-date information
- Provide consistent responses based on official policies
- Reduce support ticket volume through self-service
- Ensure all users receive the same information regardless of when they ask

## File Structure

### `faq.md`
- **Content**: Frequently asked questions for riders and drivers
- **Use Case**: General support queries, how-to questions
- **Examples**: "How do I request a ride?", "How are fares calculated?"

### `policies.md`
- **Content**: Official policies, rules, and procedures
- **Use Case**: Policy questions, refund requests, account issues
- **Examples**: "What's the cancellation policy?", "How do I get a refund?"

### `campus_playbook.md`
- **Content**: Campus-specific guidance, hotspots, safety tips
- **Use Case**: Location-specific questions, safety concerns, campus navigation
- **Examples**: "Where are the best pickup spots?", "What are peak hours?"

## RAG Pipeline Integration

### 1. Document Embedding
- Documents are chunked into smaller segments (512 tokens)
- OpenAI embeddings are generated for each chunk
- Chunks are stored in pgvector database with metadata

### 2. Query Processing
- User questions are converted to embeddings
- Similar chunks are retrieved from the database
- Context is provided to the LLM for response generation

### 3. Response Generation
- GPT-4o-mini generates responses using retrieved context
- Responses are grounded in official documentation
- Citations reference specific document sections

## Technical Implementation

### Dependencies
- `langchain`: Core RAG framework
- `openai`: Embedding and LLM services
- `pgvector`: Vector similarity search
- `markdown`: Document parsing

### Key Functions
- `embed_docs()`: Process and store document chunks
- `build_support_qa()`: Create retrieval QA chain
- `/ai/support` endpoint: Handle user queries

### Database Schema
```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(1536)
);
```

## Usage Examples

### User Query: "How much does a ride cost?"
**Retrieved Context**: `faq.md` - Fare calculation section
**Response**: "Rides cost $2.50 base fare plus $1.75 per mile. For example, a 3-mile ride would cost $7.75 total."

### User Query: "Can I cancel my ride?"
**Retrieved Context**: `policies.md` - Cancellation rules section
**Response**: "Yes, you can cancel rides. Cancellations before driver acceptance are free. Within 2 minutes of acceptance is also free. After that, fees range from $2 to $10 depending on timing."

### User Query: "Where should I get picked up on campus?"
**Retrieved Context**: `campus_playbook.md` - Pickup hotspots section
**Response**: "Popular pickup spots include Sather Gate (main entrance), Sproul Plaza (student center), and Memorial Stadium. These areas have high traffic and are well-lit for safety."

## Maintenance

### Document Updates
- Update markdown files as policies change
- Re-run `embed_docs()` script after changes
- Monitor response quality and accuracy
- Regular review of common user questions

### Performance Monitoring
- Track query response times
- Monitor embedding quality
- Analyze user satisfaction scores
- Identify gaps in documentation coverage

## Security Considerations

- All responses are generated from official documentation
- No sensitive information is stored in embeddings
- User queries are logged for quality improvement
- Responses are filtered for inappropriate content

## Future Enhancements

- Multi-language support
- Voice query processing
- Real-time policy updates
- Integration with campus systems
- Advanced analytics and insights
