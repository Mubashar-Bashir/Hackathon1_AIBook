# RAG Query Skill

## 1. 🎯 Purpose and Philosophy

This skill enables semantic search and retrieval-augmented generation (RAG) functionality for the Physical AI & Humanoid Robotics textbook. It allows users to ask questions about the textbook content and receive accurate, contextually relevant answers based on vector embeddings of the knowledge base.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for RAG query execution | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Python scripts for RAG operations | On Demand |
| `assets/` | Optional | Configuration files and reference data | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Input Validation**: Verify that the user query is provided and is not empty.
2.  **Embedding Generation**: Generate vector embeddings for the user query using the configured embedding model (e.g., OpenAI, Cohere, or custom model).
3.  **Vector Search**: Perform a similarity search in the vector database (Qdrant Cloud) against the textbook content embeddings.
4.  **Context Retrieval**: Retrieve the top-k most relevant text chunks from the textbook based on similarity scores.
5.  **Context Formatting**: Format the retrieved context into a structured prompt for the LLM.
6.  **Response Generation**: Generate a comprehensive answer using the LLM, incorporating the retrieved context.
7.  **Response Validation**: Ensure the generated response is relevant to the query and properly cites the source content.
8.  **Output Delivery**: Return the final response with source citations and confidence scores.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/rag_query.py`
* **Invocation Command**: `python scripts/rag_query.py --query "your question here" --top_k 5`
* **Configuration**: The script reads configuration from `assets/rag_config.json` which contains API keys, model settings, and vector database connection parameters.

### D. Inputs and Outputs

* **Inputs:**
    * `query`: The user's question or search query (string)
    * `top_k`: Number of relevant chunks to retrieve (integer, default: 5)
    * `min_score`: Minimum similarity score threshold (float, default: 0.3)
* **Outputs:**
    * `response`: The generated answer based on retrieved context
    * `sources`: List of source documents/chunks used in generation
    * `confidence`: Confidence score for the response (0.0-1.0)
    * `query_embedding`: The vector representation of the original query

---

## 4. 🛠️ Error Handling

* **Vector Database Unavailable**: If the vector database connection fails, return an error message and suggest trying again later.
* **No Relevant Results**: If no content meets the minimum similarity threshold, return a response indicating that no relevant information was found in the textbook.
* **API Limit Exceeded**: If embedding or LLM API limits are reached, return a graceful error message and suggest retrying after a delay.