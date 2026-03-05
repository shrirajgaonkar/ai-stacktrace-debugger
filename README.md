# AI Debugging Assistant

AI Debugging Assistant is an intelligent developer tool that analyzes stack traces and error logs, identifies possible root causes, and suggests fixes using AI.

The system automatically parses error logs, detects runtime environments, matches known error patterns, and uses LLMs to explain problems and recommend solutions.

This project demonstrates a production-style architecture using FastAPI, PostgreSQL, Celery, Redis, and React.

---

# Features

• Upload stack traces or error logs  
• Automatic runtime detection (Python, Node.js, Java)  
• Structured stack trace parsing  
• Pattern-based error detection  
• AI-powered root cause analysis  
• Suggested fix steps with code snippets  
• Debugging session tracking  
• GitHub OAuth login  
• Background processing with Celery  
• Real-time session status updates  

---

# Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Celery
- Redis
- Pydantic
- JWT Authentication
- GitHub OAuth

### Frontend
- React
- TypeScript
- Vite

### AI
- OpenAI
- Anthropic Claude

---

# Architecture

```
User Uploads Error Log
        │
        ▼
FastAPI API
        │
        ▼
Session Created (Queued)
        │
        ▼
Celery Worker
        │
        ├── Stack Trace Parser
        ├── Pattern Matcher
        └── LLM Analysis
                │
                ▼
Session Updated with Root Causes + Fix Suggestions
```

---

# Project Structure

```
stacktrace-ai/
│
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── parsing/
│   │   ├── patterns/
│   │   ├── llm/
│   │   ├── services/
│   │   ├── workers/
│   │   └── utils/
│   │
│   ├── migrations/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│
└── sample_logs/
```

---

# Local Setup

## 1 Install PostgreSQL

Create database:

```
stacktrace_ai
```

---

## 2 Install Redis

Mac / Linux

```
brew install redis
```

Windows

Use Redis Windows port or WSL.

Start Redis:

```
redis-server
```

---

## 3 Backend Setup

Navigate to backend folder:

```
cd backend
```

Create virtual environment:

```
python -m venv .venv
```

Activate:

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## 4 Configure Environment

Create `.env` using `.env.example`.

Example:

```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/stacktrace_ai
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your_secret_key
OPENAI_API_KEY=your_key
```

---

## 5 Run Database Migrations

```
alembic upgrade head
```

---

## 6 Start Backend

```
uvicorn app.main:app --reload
```

Open:

```
http://localhost:8000/docs
```

---

## 7 Start Celery Worker

Open new terminal:

```
celery -A app.workers.celery_app worker --loglevel=info
```

---

## 8 Start Frontend

```
cd frontend
npm install
npm run dev
```

Open:

```
http://localhost:5173
```

---

# API Endpoints

### Authentication

```
GET /api/auth/github/login
GET /api/auth/github/callback
```

### Sessions

```
POST /api/sessions
GET /api/sessions
GET /api/sessions/{session_id}
POST /api/sessions/{session_id}/comment
POST /api/sessions/{session_id}/resolve
```

### Status

```
GET /api/sessions/{session_id}/status
```

---

# Example Use Case

Developer uploads a stack trace:

```
ZeroDivisionError: division by zero
```

System will:

1. Parse the stack trace
2. Identify exception type
3. Match known error patterns
4. Ask LLM for explanation
5. Suggest fixes

Example output:

```
Root Cause:
Division by zero caused by empty list input.

Suggested Fix:
Add validation before dividing.

Example Code:

if len(values) == 0:
    return 0
```

---

# Testing

Run tests:

```
pytest
```

---

# Future Improvements

• VSCode extension integration  
• GitHub PR debugging  
• CI failure analysis  
• Error pattern auto-learning  
• Log clustering  

---

# License

MIT License
