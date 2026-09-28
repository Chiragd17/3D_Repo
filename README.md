# 🏙️ Repo City

Repo City is an interactive 3D web application that visualizes GitHub repositories ("Google Earth for your codebase"). It transforms flat, complex repositories into sprawling, navigable 3D cities where folders become distinct districts and files become buildings. Powered by an intelligent backend, it maps deep code structures, activity hotspots, test coverage, and leverages AI to provide architectural explanations of your codebase.

---

## 🏗️ Master Project Structure

The project is split into two primary applications: a high-performance **React/Three.js Frontend** and an intelligent **FastAPI Backend**.

```text
CREATIVE_WEBSITE/
├── backend/                   # Python FastAPI Backend
│   ├── app/
│   │   ├── ai/                # AI integrations (Groq)
│   │   ├── analyzer/          # Repository intelligence (dependencies, hotspots)
│   │   ├── api/               # FastAPI routers (analyze, ask, auth, explain)
│   │   ├── github/            # GitHub client (HTTP requests, tree parsing)
│   │   └── store.py           # Auto-caching datastore for parsed repos
│   └── tests/                 # Pytest unit tests
│
└── frontend/                  # React + Three.js Frontend
    └── Repo-City-Frontend-Foundation/artifacts/repo-city/
        ├── public/            # Static assets and 3D textures
        └── src/
            ├── components/    # UI and 3D core
            │   └── three/     # Three.js engine and visualizer overlays
            ├── pages/         # Application views (Landing, Analysis, World)
            ├── services/      # API clients bridging to the FastAPI backend
            └── types/         # TypeScript shared types
```

---

## ✨ Features & Architecture

### 1. 3D World Generation (Frontend)
- **Procedural City Generation**: Renders entire codebases procedurally.
- **Dynamic Overlays**:
  - **Activity Heatmap**: Highlights the most frequently modified files in the git history.
  - **Risk Hotspots**: Visualizes files with high complexity, large size, and missing tests in red.
  - **Test Coverage**: Indicates testing status across the repository.
  - **Dependencies**: Draws interconnected "roads" between files that import each other.
- **Atmospheric Rendering**: Real-time lighting, sun placement, and dynamic cloud layers over the "Planet".

### 2. GitHub Repository Ingestion (Backend)
- **OAuth Authentication**: Supports full GitHub OAuth flow, allowing users to ingest **Private Repositories**.
- **REST Integration**: Recursively fetches a repository's metadata and file tree securely.
- **Intelligent Filtering & Prioritization**: 
  - Drops generated folders (`node_modules`, `dist`, `.git`) and binary assets.
  - Limits analysis to the top 150 files to optimize memory and performance.
- **Code Analysis Heuristics**: Detects test files, calculates line counts, and tracks git history.

### 3. City Intelligence (AI Integration)
- **Explain with AI**: Interfaces directly with Groq-powered AI models to generate deep, architectural summaries of any selected building/file.
- **Ask the City**: A chat interface to locate specific features (e.g. "Where is the authentication logic?") and automatically pan the 3D camera to the target.

### 4. Data Persistence & State
- **Auto-caching Datastore**: The backend immediately stores analyzed repos in memory and persists them to disk (`repo_cache.json`) so your cities survive server reloads.
- **Session Caching**: The frontend seamlessly caches the 3D hierarchy in `sessionStorage` to allow lightning-fast navigation without re-fetching.

---

## 💻 Getting Started (Local Development)

### 1. Setup the Backend
The backend requires Python 3.11+.
```bash
cd backend
.venv\Scripts\activate
cp .env.example .env
```
Update your `.env` with a `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, and a `GROQ_API_KEY`.
```bash
uvicorn app.main:app --reload
```
The backend API and Swagger docs will be available at `http://localhost:8000/docs`.

### 2. Setup the Frontend
The frontend requires Node.js 18+ and `pnpm`.
```bash
cd frontend/Repo-City-Frontend-Foundation/artifacts/repo-city
cp .env.example .env
```
Ensure your `.env` contains: `VITE_API_BASE_URL=http://localhost:8000`
```bash
pnpm install
pnpm run dev
```
The application will be available at `http://localhost:5173`.

---

## 🧪 Testing
To run the test suite for the backend parsing and filtering utilities:
```bash
cd backend
python -m pytest tests/
```
