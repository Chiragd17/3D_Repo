# Repo City Frontend

Repo City is an interactive 3D web application that visualizes GitHub repositories ("Google Earth for your codebase"). This directory contains the React frontend, built with Vite, TypeScript, and Three.js for high-performance 3D rendering.

## 🛠️ Project Structure

```text
repo-city/
├── public/              # Static assets and textures for the 3D world
├── src/
│   ├── components/      # React components (brand, analysis progress, etc.)
│   │   ├── three/       # 3D visualization core
│   │   │   ├── engine/  # Three.js engine (generators, camera, planets, shaders)
│   │   │   └── intelligence/ # Overlays for activity, dependencies, and hotspots
│   │   └── ui/          # Reusable UI components (Tailwind, Radix)
│   ├── data/            # Fallback mock data structures
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility functions
│   ├── pages/           # Application views (landing, analysis, world)
│   ├── services/        # API clients and data adapters bridging to the FastAPI backend
│   └── types/           # TypeScript interfaces and shared types
├── index.html           # HTML entry point
├── package.json         # Node.js dependencies and scripts
└── vite.config.ts       # Vite configuration
```

## 🚀 Implemented Features

This frontend handles the immersive visualization and navigation of codebases. Currently implemented features include:

### 1. 3D World Generation (Three.js)
- **Procedural City Generation**: Renders entire codebases as navigable 3D cities. Folders become districts, files become buildings.
- **Dynamic Overlays (Intelligence Mode)**:
  - **Activity Heatmap**: Highlights the most frequently modified files in the git history.
  - **Risk Hotspots**: Visualizes files with high complexity, large size, and missing tests in red.
  - **Test Coverage**: Indicates testing status across the repository.
  - **Dependencies**: Draws interconnected "roads" between files that import each other.
- **Atmospheric Rendering**: Real-time lighting, sun placement, and dynamic cloud layers over the "Planet" to create a premium aesthetic.

### 2. User Interface & Interactions
- **Repository Ingestion Flow**: A sleek landing page that handles GitHub OAuth authentication and visualizes the multi-step repository mapping progress.
- **File Inspector**: Clicking on any "building" opens a detailed dossier showing the file's language, size, risk score, and exact location within the project hierarchy.
- **City Intelligence (AI)**:
  - **Explain with AI**: Interfaces directly with the Groq-powered backend to provide deep, architectural summaries of any selected file.
  - **Ask the City**: A chat interface that can locate specific features (e.g. "Where is the authentication logic?") and pan the camera to the exact building.

### 3. State Management & API Integration
- **Session Caching**: Smooth transition from analysis to the 3D world using `sessionStorage`, persisting the loaded city across browser refreshes.
- **Data Adapters**: Seamlessly maps the flat JSON responses from the Python backend into the deeply nested hierarchical `PlanetData` structure required by the 3D engine.
- **OAuth Session Handling**: Securely manages GitHub authentication alongside the backend.

## 💻 Running the Frontend locally

### Prerequisites
Make sure you have Node.js 18+ and `pnpm` (or `npm`) installed.

### 1. Setup Environment
1. Ensure the Python FastAPI backend is running locally on port 8000.
2. Create a `.env` file in this directory and configure your backend URL:
   ```text
   VITE_API_BASE_URL=http://localhost:8000
   ```

### 2. Install Dependencies
```bash
pnpm install
```

### 3. Start the Development Server
```bash
pnpm run dev
```
The application will be available at `http://localhost:5173`.
