# Backend Service

## Purpose
The backend service powers the Industrial Knowledge Intelligence (IKI) platform, handling API requests, data ingestion, knowledge graph queries, vector similarity searches, and background task orchestration.

## Folder Structure
- `app/api/`: API route definitions and endpoint handlers.
- `app/core/`: Core configuration, logging, and security utilities.
- `app/db/`: Database configuration, SQLAlchemy models, and session management.
- `app/services/`: Core business logic, integrating different components like AI, DBs, and third-party APIs.
- `app/schemas/`: Pydantic models for request and response validation.
- `app/crud/`: Reusable database interaction operations (Create, Read, Update, Delete).
- `app/tests/`: Automated test suite.

## Responsibilities
- Serve RESTful APIs via FastAPI.
- Interface with PostgreSQL (pgvector) and Neo4j AuraDB.
- Execute AI workflows and generate embeddings.
- Manage scheduled background tasks.
