# Industrial Knowledge Intelligence Platform

An AI-powered platform for extracting, processing, and querying industrial knowledge using Retrieval-Augmented Generation (RAG) and graph databases.

---

## 🏗️ Architecture Overview

The system consists of three main pillars:
- **Frontend**: A modern web interface for users to query the knowledge graph and visualize relationships.
- **Backend**: A robust API for handling queries, data ingestion, and orchestration.
- **AI/ML**: Agentic workflows and embeddings generation to power the intelligence of the platform.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS
- **Data Fetching**: React Query
- **Visualization**: react-force-graph

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Task Scheduling**: APScheduler

### AI & Machine Learning
- **LLM**: Gemini 2.5 Flash
- **Agent Framework**: LangGraph
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Graph Integration**: Neo4j Python Driver

### Databases
- **Vector/Relational DB**: PostgreSQL (Supabase with pgvector)
- **Graph DB**: Neo4j AuraDB

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Backend Deployment**: Railway
- **Frontend Deployment**: Vercel

---

## 📁 Folder Structure

```text
.
├── ai_ml/       # AI pipelines, embeddings, and LangGraph agents
├── backend/     # FastAPI application code
├── docker/      # Docker configurations
├── docs/        # Project documentation
├── frontend/    # React application code
├── scripts/     # Helper scripts for development
└── .github/     # GitHub Actions workflows
```

---

## 🚀 Setup Instructions

*(Placeholder: Instructions for setting up the local environment, including environment variables and Docker)*

---

## 👥 Team Structure

*(Placeholder: Add team members and their roles here)*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
