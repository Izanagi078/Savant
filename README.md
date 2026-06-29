# 🚀 SmartTutor: Course Builder & Personal Tutor

A lightweight, synchronous agentic course compiler that automatically constructs structured learning syllabi, retrieves targeted reference videos and papers, filters them using a Verifier Agent, and hosts an interactive expert tutoring chat dashboard.

---

## 📐 System Architecture

SmartTutor uses a simplified, high-performance synchronous agentic pipeline that eliminates container overhead (no Docker, Kafka, Redis, or local vector DB indexing required):

```mermaid
graph TD
    Client[Next.js Frontend] -->|1. POST /content/generate| API[FastAPI Gateway]
    API -->|2. Generate Syllabus & Queries| Gemini[Gemini 1.5 Flash]
    
    API -->|3a. Search query| YT[YouTube XML Feed]
    API -->|3b. Search query| arXiv[arXiv API]
    API -->|3c. Search query| Wiki[Wikipedia OpenSearch]
    
    YT -.->|Raw Results| API
    arXiv -.->|Raw Results| API
    Wiki -.->|Raw Results| API
    
    API -->|4. Audit & Filter Resources| Verifier[Verifier Agent - Groq Llama 3.1]
    Verifier -->|5. Return Verified Course JSON| API
    API -->|6. Cache Session Course| Store[In-Memory Store]
    API -->|7. Return Complete Verified Syllabus| Client
    
    Client -->|8. Chat Tutor Prompt| API
    API -->|9. Lookup Syllabus Context| Store
    API -->|10. In-Context RAG Response| Groq[Groq Llama 3.1 / Gemini]
```

---

## ⚡ Core Technology Stack

* **Frontend:** Next.js, React, TypeScript, Chart.js, TailwindCSS.
* **API Gateway:** FastAPI (Python), Pydantic.
* **LLM Engine:** Gemini 1.5 Flash (syllabus query compilation) & Groq Llama 3.1 8B (verifier agent and chat tutor).
* **RAG Strategy:** Memory-safe in-context context stuffing (no heavy FAISS vector files on disk).
* **Scraping & Ingestion:** BeautifulSoup4, aiohttp, requests.

---

## 📂 Repository Structure

```text
smart-tutor-workspace/
├── smart-tutor/               # Next.js React Frontend App
│   ├── public/                # Static assets & media
│   ├── src/
│   │   ├── app/               # Next.js Router pages (content, quiz, performance)
│   │   ├── components/        # Sidebar, ContentCard, QuizForm, PerformanceChart
│   │   └── styles/            # Global stylesheets
│   ├── package.json
│   └── tsconfig.json
│
└── smart-tutor-backend/       # FastAPI Python Backend App
    ├── docs/                  # Architecture schemas & notes
    ├── src/
    │   ├── api/               # API Controllers & routes
    │   ├── config/            # System configuration settings
    │   ├── models/            # Pydantic validation schemas
    │   ├── services/          # LLM orchestration, Verifier Agent, search services
    │   └── utils/             # Helper utilities
    ├── tests/                 # Backend testing harness
    └── requirements.txt       # Python backend dependencies
```

---

## 🛠️ Installation & Setup

### 1. Configure API Keys
Create a `.env` file inside `smart-tutor-backend` containing your credentials:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Configure the Python Backend
Activate your local virtual environment and install dependencies:
```bash
cd smart-tutor-backend
# Activate your environment
source Scripts/activate  # Windows PowerShell/Cmd
pip install -r requirements.txt
```

Launch the FastAPI web server:
```bash
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
```

### 3. Run the Frontend App
Install Node modules and start the Next.js development server:
```bash
cd smart-tutor
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to access the learning client.