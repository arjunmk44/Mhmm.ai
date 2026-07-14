# AI/ML Module

## Purpose
The AI/ML module is the intelligence engine of the Industrial Knowledge Intelligence (IKI) platform. It manages document processing pipelines, orchestrates LangGraph agents, extracts entities and relationships for the knowledge graph, and powers hybrid retrieval strategies (Vector + Graph).

## Folder Structure
- `agents/`: LangGraph agent definitions and state management.
- `ingestion/`: Document loading, parsing, and chunking logic.
- `extraction/`: Entity and relationship extraction utilizing LLMs.
- `graph/`: Neo4j interaction, graph building, and entity resolution.
- `retrieval/`: Hybrid, vector, graph, and keyword search implementations.
- `embeddings/`: Embedding models and vector database interactions.
- `llm/`: API clients (Gemini, Groq) and model routing logic.
- `prompts/`: Centralized prompt templates for various tasks.
- `interfaces/`: Boundaries defined for integration with the main Backend API.
- `config/`: AI-specific environment settings and constants.
- `utils/`: Reusable helpers, validators, and logging tailored for AI components.
- `tests/`: Automated unit and integration tests.

## Responsibilities
- Process unstructured industrial documents into structured knowledge.
- Build and query the Neo4j Knowledge Graph.
- Provide advanced RAG (Retrieval-Augmented Generation) capabilities.
- Expose clean interfaces (`interfaces/`) for the FastAPI backend to invoke.

## Development Workflow
1. Install dependencies from `requirements.txt`.
2. Implement logic within the designated domains.
3. Validate outputs using unit tests.
4. Expose functionality through the `interfaces/` modules.

## Integration with Backend
The FastAPI backend will import from the `interfaces/` directory to trigger AI jobs (like ingestion or querying) rather than calling internal AI components directly. This ensures loose coupling.
