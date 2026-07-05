# 🚀 Savant: AI-Powered Course Builder & Interactive Tutor Suite

Savant is a production-grade, highly concurrent generative learning platform that compiles customized, structured course syllabi, retrieves targeted video and paper references, filters them through a verification agent, and hosts an interactive tutoring dashboard featuring dynamically graded quizzes and chat support.

### 🌐 Live Deployment
- **Frontend App:** [https://savant.vercel.app](https://savant.vercel.app)
- **Backend API Gateway:** [https://savant-oqtv.onrender.com](https://savant-oqtv.onrender.com) (API Docs: [https://savant-oqtv.onrender.com/docs](https://savant-oqtv.onrender.com/docs))

---

## 📐 System Architecture

Savant is built as a fully decoupled client-server architecture. It features server-side edge routing and asynchronous database processing:

```mermaid
graph TD
    Client[Next.js Frontend] -->|HTTP Requests with Credentials| Middleware[Edge Middleware]
    Middleware -->|Verified Cookie Check| Gateway[FastAPI Backend Gateway]

    subgraph User & Session State
        Gateway -->|Async engine| PostgreSQL[(Supabase Cloud PostgreSQL)]
    end

    subgraph Stage 1 - Syllabus Generation
        Gateway -->|Generate| Gemini[Gemini 2.5 Flash]
    end

    subgraph Stage 2 - Resource Concurrency
        Gateway -->|Fetch| YT[YouTube API]
        Gateway -->|Fetch| Arxiv[arXiv API]
        Gateway -->|Fetch| Wiki[Wikipedia Web Scraper]
    end

    subgraph Stage 3 - Verification Agent
        Gateway -->|Raw Results| Verifier[Verifier Agent]
        Verifier -->|Syllabus & Map| Gateway
    end

    Gateway -->|Save Syllabus & Chat Logs| PostgreSQL
    Gateway -->|Return Payload| Client
    Client -->|Local Cache| Zustand[(Zustand State Store)]

    subgraph Interactive Chat Tutor
        Client -->|Chat Query| Gateway
        Gateway -->|Retrieve History| PostgreSQL
        Gateway -->|LLM Context response| Groq[Groq LLaMA 3]
    end
```

---

## ⚡ Core Technology Stack

* **Frontend App:** Next.js (App Router, Turbopack), React 19, TypeScript, TailwindCSS v4, Chart.js, Zustand.
* **API Gateway:** FastAPI (Python), Uvicorn.
* **Database & Transactions:** Cloud PostgreSQL (Supabase) via SQLAlchemy + `asyncpg` (Asynchronous driver with `aiosqlite` local fallback).
* **Router Protection:** Next.js Server-Side Middleware for HttpOnly cookie checks.
* **LLM Engine:** Gemini 2.5 Flash (syllabus query compilation & quiz generation) & Groq LLaMA 3 (verifier agent and chat tutor).
* **Scraping & Integration:** BeautifulSoup4, aiohttp, httpx.

---

## 🛠️ Installation & Local Setup

### 1. Configure Environment Variables
Create a `.env` file inside `smart-tutor-backend` containing your credentials:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://username:password@your-supabase-host:5432/postgres
JWT_SECRET_KEY=your_secure_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. Run the Python Backend
Install dependencies inside the virtual environment:
```bash
cd smart-tutor-backend
# Activate virtual environment
.\Scripts\activate
pip install -r requirements.txt
```

Launch the FastAPI web server with auto-reload:
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Run the Frontend Client
Install the React dependencies and run the Next.js client development server:
```bash
cd smart-tutor
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to access the learning application.

---

## 🌐 Cloud Deployment & Configuration

The application is deployed and configured for production use:

### 1. Frontend (Vercel)
The Next.js frontend is deployed on Vercel.
* **Live Deployment:** [https://savant.vercel.app](https://savant.vercel.app)
* **Environment Variables:**
  * `NEXT_PUBLIC_API_URL`: The live backend API gateway URL (`https://savant-oqtv.onrender.com`). If not set, the frontend fallback logic automatically uses this production URL.

### 2. Backend (Render)
The FastAPI backend is deployed on Render.
* **Live API Endpoint:** [https://savant-oqtv.onrender.com](https://savant-oqtv.onrender.com)
* **Interactive API Documentation:** [https://savant-oqtv.onrender.com/docs](https://savant-oqtv.onrender.com/docs)
* **Deployment Details:**
  * **Build Command:** `pip install -r requirements.txt`
  * **Start Command:** `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
  * **Environment Variables Required:**
    * `GEMINI_API_KEY`: Google Gemini API Key for syllabus compilation and quiz generation.
    * `GROQ_API_KEY`: Groq API Key for agentic content verification and tutoring chat.
    * `DATABASE_URL`: Supabase Cloud PostgreSQL connection string (handles table creation dynamically on lifespan startup).
    * `JWT_SECRET_KEY`: Private signing key for authorization tokens.
    * `ALLOWED_ORIGINS`: Production frontend origin (`https://savant.vercel.app`) to handle cross-origin request credentials.