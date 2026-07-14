# Frontend Application

## Purpose
The frontend application provides the user interface for the Industrial Knowledge Intelligence (IKI) platform, allowing users to upload documents, perform natural language queries, visualize relationships in the knowledge graph, and manage alerts.

## Folder Structure
- `src/components/`: Reusable UI components, organized by domain (common, upload, graph, etc.).
- `src/pages/`: Top-level route components representing different views (Dashboard, Query, etc.).
- `src/layouts/`: Structural layout components (e.g., Sidebar, Navbar, Page Containers).
- `src/hooks/`: Custom React hooks for shared component logic.
- `src/services/`: Client-side business logic and state management wrappers.
- `src/api/`: API client configuration and endpoints for communicating with the backend.
- `src/types/`: TypeScript interfaces and type definitions.
- `src/utils/`: Helper functions and utility scripts.
- `src/styles/`: Global CSS/Tailwind styles.
- `src/assets/`: Static assets like images and icons.
- `public/`: Unprocessed static assets served directly.

## Responsibilities
- Present a responsive and intuitive user interface.
- Communicate with the FastAPI backend to fetch and mutate data.
- Render complex interactive visualizations (e.g., knowledge graph).
- Manage client-side state and caching (e.g., via React Query).

## Development Workflow
1. Install dependencies (once specified).
2. Run the development server (e.g., using Vite).
3. Follow standard React and TypeScript patterns to implement features.
