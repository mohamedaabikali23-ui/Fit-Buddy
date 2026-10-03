# 💻 FitBuddy: Technical Stack & Architecture

This document provides a technical breakdown of the programming languages, frameworks, libraries, protocols, and architectural patterns powering **FitBuddy**.

---

## 1. Technology Matrix Overview

| Category | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Language** | Python | `3.10+` | Core server logic, mathematical calculations, and AI orchestration |
| **Backend Framework** | FastAPI | `>=0.110.0` | Asynchronous REST API, dependency injection, and Pydantic validation |
| **ASGI Server** | Uvicorn | `>=0.28.0` | Asynchronous Server Gateway Interface for high concurrency |
| **Database Engine** | SQLite | `3.x` | Embedded ACID relational database (`fitbuddy.db`) |
| **ORM** | SQLAlchemy | `>=2.0.0` | Object Relational Mapping and declarative schema management |
| **AI / LLM** | Google Gemini | `gemini-3.8-flash` | Generative reasoning for training routines, meal plans, and chat |
| **AI SDK** | `google-genai` | `>=1.0.0` | Official Google GenAI SDK (with fallback to `google.generativeai`) |
| **Template Engine** | Jinja2 | `>=3.1.0` | Server-Side Rendering (SSR) of dynamic HTML dashboards |
| **Form Parsing** | `python-multipart` | `>=0.0.9` | Form-data body extraction for user assessment submissions |
| **Markdown Parsers** | `markdown` & `marked.js`| `3.6.0` / CDN | Server-side and client-side conversion of Markdown to safe HTML |
| **Frontend UI** | HTML5 / CSS3 / ES6 JS | Native | Modern dark-mode glassmorphic interface, zero heavy frontend frameworks |
| **Typography** | Google Fonts | Web | *Outfit* (headings) & *Plus Jakarta Sans* (body text) |
| **Companion UI** | Streamlit | `>=1.35.0` | Standalone alternative dashboard interface |
| **Document Export** | `python-docx` | `>=1.1.0` | Programmatic Microsoft Word (.docx) generation with WordprocessingML |

---

## 2. Deep-Dive Tier Specifications

### A. Backend Architecture: FastAPI + Uvicorn
* **Asynchronous Execution**: Leverages Python's native `asyncio` loop for non-blocking I/O operations (HTTP requests, database reads/writes).
* **Dependency Injection**: Route handlers utilize FastAPI's `Depends(database.get_db)` to cleanly manage database session lifecycles (opening connections and guaranteeing teardown in `finally` blocks).
* **Data Validation**: Strict Pydantic models (`GenerateRequest`, `ChatRequest`) validate incoming JSON payloads and provide auto-generated OpenAPI documentation.
* **Auto-Generated Documentation**:
  * Swagger UI: `/docs`
  * ReDoc: `/redoc`

### B. Database & Persistence Layer: SQLite + SQLAlchemy
* **Engine Configuration**: Single-file storage at `fitbuddy.db` with thread-safety override (`check_same_thread=False`).
* **Declarative Mapping**:
  * `UserProfile`: Master record storing biometrics, goals, constraints, and metabolic calculations.
  * `WorkoutPlan`: Child record holding markdown workout splits with foreign key cascade deletion.
  * `MealPlan`: Child record holding 4-meal daily breakdowns and grocery lists with cascade deletion.
  * `ChatMessage`: Child record tracking user questions and coach responses for session memory.

### C. Generative AI Engine: Gemini 3.8 Flash
* **Model**: `gemini-3.8-flash` optimized for high-speed reasoning and structured markdown output.
* **SDK Hierarchy**:
  1. Primary: Official `google-genai` SDK (`genai.Client`) with `types.GenerateContentConfig`.
  2. Secondary Fallback: Legacy `google.generativeai` SDK (`legacy_genai.GenerativeModel`).
* **Resilience Pattern**: Exponential backoff retry handler catching HTTP 429 (quota) and 503 (high demand) errors with randomized jitter.
* **Offline Heuristics**: Local deterministic response generator fallback when API keys are absent or servers are unreachable.

### D. Frontend Design System: Vanilla CSS & JS
* **Design Philosophy**: High-end modern dark-mode glassmorphism.
* **CSS Custom Properties**:
  * Backgrounds: `--bg-primary: #0a0e17`, `--bg-card: rgba(17, 24, 39, 0.75)`
  * Accents: Emerald (`#10b981`), Cyan (`#06b6d4`), Amber (`#f59e0b`), Rose (`#f43f5e`)
  * Surface Effects: `backdrop-filter: blur(16px)`, radial gradient lighting
* **Client-Side Dynamics**:
  * Asynchronous AJAX via Fetch API.
  * Tab switching without page reloads.
  * Dynamic range slider badge updates.
  * Real-time toast alert dispatching system.
