# Palm Mind RAG Backend

RAG-powered FastAPI backend with document ingestion, semantic search, and chat.

## Prerequisites

- Docker & Docker Compose
- A [Google Gemini API key](https://aistudio.google.com/apikey)

## Setup

1. Clone the repository and enter the directory.

2. Create environment file:

```bash
cp .env.example .env
```

3. Edit `.env` and set your `GEMINI_API_KEY`.

## Run with Docker

```bash
docker compose up -d --build
```

The API is available at `http://localhost:8000`.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Chat with RAG context |
| `/ingest` | POST | Upload a document (.txt / .pdf) |
| `/booking` | POST | Create an interview booking |
| `/docs` | GET | Swagger UI documentation |

### Chat

```json
POST /chat
{
  "session_id": "user-123",
  "message": "What is this document about?"
}
```

### Ingest a document

Upload a `.txt` or `.pdf` file with an optional chunking strategy (`fixed` or `recursive`).

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@document.pdf" \
  -F "strategy=recursive"
```

### Create a booking

```json
POST /booking
{
  "name": "Prasun Bhattarai",
  "email": "prasun@example.com",
  "date": "2026-06-15",
  "time": "10:00"
}
```
```

Make sure PostgreSQL, Redis, and Qdrant are running and accessible via the hosts in `.env`.

## Project Structure

```
app/
  api/          # Route handlers
  core/         # Config
  db/           # Database clients (PostgreSQL, Redis, Qdrant)
  models/       # SQLAlchemy models
  services/     # Business logic (RAG, ingestion, booking, LLM)
  utils/        # Utilities (PDF reader, chunking, embeddings)
  main.py       # FastAPI entry point
```
