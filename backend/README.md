# Repo City Backend

Repo City is an interactive 3D web application that visualizes GitHub repositories ("Google Earth for your codebase"). This directory contains the Python FastAPI backend, which handles repository parsing, GitHub REST API integration, and AI-powered natural language code exploration.

## 🛠️ Project Structure

```text
backend/
├── app/
│   ├── ai/              # AI integrations
│   ├── analyzer/        # Repository intelligence (dependencies, hotspots, aggregator)
│   ├── api/             # FastAPI routers (analyze, ask, auth, explain, repository)
│   ├── github/          # GitHub client (HTTP requests, tree parsing, filtering)
│   ├── models/          # Pydantic JSON schemas
│   ├── main.py          # FastAPI application entry point
│   └── store.py         # Store for parsed repositories with disk caching
├── tests/               # Pytest unit tests
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## 🚀 Implemented Features

This backend is actively developed to support the full 3D visualization platform. The following functionality is currently implemented:

### 1. Foundation & API Contracts
- **FastAPI Setup**: Core web framework, structured logically with routers and environment variables.
- **CORS**: Configured out-of-the-box to communicate with a frontend running on `http://localhost:5173`.
- **Pydantic Data Models**: Stable schemas to strictly type responses (e.g., `RepoFile`, `District`, `RepositoryResponse`), guaranteeing a predictable data contract for the 3D frontend.
- **AI Endpoints**: Supports Groq-powered AI for code explanation (`/api/explain`) and chat capabilities (`/api/ask`).

### 2. GitHub Repository Ingestion
- **GitHub URL Parsing**: Safely extracts the `owner` and `repo` from URLs (e.g., ignores trailing `.git` or `/tree/main`).
- **OAuth Authentication**: Supports a full GitHub OAuth flow, exchanging authorization codes for access tokens to allow users to ingest their own **Private Repositories**.
- **REST Integration**: Seamlessly cascades credentials (from user session, to global `.env` token, to unauthenticated access) to recursively fetch a repository's metadata and complete file tree via `httpx`.
- **Intelligent Filtering & Prioritization**: 
  - Drops generated folders (`node_modules`, `dist`, `.git`) and binary assets.
  - Prioritizes Source Code > Config Files > Documentation.
  - Deterministically limits analysis to the top **150 files** to respect memory and rate-limit constraints.
- **Code Analysis Heuristics**: 
  - Detects if a file is a test file based on naming conventions (`test_*.py`, `*.spec.ts`, etc.).

### 3. Repository Intelligence & Persistence
- **Deep Content Analysis**: Securely fetches raw file blobs using SHA hashes to analyze actual code.
- **Static Dependency Extraction**: Uses optimized Regex heuristics to parse internal imports for Python and JS/TS (`import`, `from`, `require`) and build an interconnected internal dependency graph (roads).
- **Hotspot Heuristics**: Calculates a normalized `hotspot_score` (low, medium, high) based on a weighted formula: *File Size + Git Activity + Missing Test Penalty*. 
  > **Note:** The hotspot score is a heuristic visual indicator designed to drive 3D heatmap rendering. It is **not** a formal code-quality or security assessment.
- **Rollup Aggregation**: Flattens file-level intelligence into District (folder) averages and overall Repository Statistics (total LOC, languages, etc.).
  - Generates perfectly stable, URL-safe **File IDs** (`src-auth-login-ts`) to act as 3D building IDs for the frontend.
- **Auto-caching Datastore**: Analyzed repos are immediately stored in server memory and automatically persisted to disk (`repo_cache.json`) to survive server reloads seamlessly.
- **Testing**: A full suite of `pytest` unit tests covering the parsing, filtering, ID generation, and language detection logic.

## 💻 Running the Backend locally

### Prerequisites
Make sure you have Python 3.11+ installed.
The project uses `fastapi`, `uvicorn`, `httpx`, `groq`, and `pytest`.

### 1. GitHub OAuth App Setup
To enable authentication and private repository access, create a new GitHub Developer Application:
1. Go to GitHub > Settings > Developer settings > OAuth Apps > **New OAuth App**.
2. **Homepage URL**: `http://localhost:5173`
3. **Authorization callback URL**: `http://localhost:8000/api/auth/github/callback`

### 2. Setup Environment
1. Activate your virtual environment:
   ```bash
   .venv\Scripts\activate
   ```
2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Add your newly generated `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, and a `GROQ_API_KEY` with your selected model. DO NOT commit this file to version control.

### 3. Start the Server
Start the development server using Uvicorn:
```bash
uvicorn app.main:app --reload
```

### 4. Explore the Docs
FastAPI automatically generates interactive Swagger documentation.
Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the endpoints instantly!

## 🧪 Running Tests
To verify all GitHub parsing and filtering utilities:
```bash
python -m pytest tests/
```
