# Palm Mind RAG Backend

RAG-powered FastAPI backend with document ingestion, semantic search, chat, and interview booking.

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

After making code changes, rebuild the FastAPI container:

```bash
docker compose build fastapi && docker compose up -d fastapi
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Chat with RAG context (auto-detects booking intents) |
| `/ingest` | POST | Upload a document (.txt / .pdf) |
| `/booking` | POST | Create an interview booking (direct API) |
| `/docs` | GET | Swagger UI documentation |

### Chat

Main conversational endpoint. **Booking is done through chat** — the system auto-detects booking intents from your message via Gemini. No need to call `/booking` separately.

```json
POST /chat
{
  "session_id": "user-123",
  "message": "What is this document about?"
}
```

**Booking via chat:**

```json
POST /chat
{
  "session_id": "user-123",
  "message": "Book an appointment for Prasun Bhattarai at prasunbhattarai2003@gmail.com on June 15 at 2pm"
}
```

Use natural language for the date and time (e.g. "June 15 at 2pm") — the LLM will extract and convert it to the required format automatically.

### Ingest a document

Upload a `.txt` or `.pdf` file with a chunking strategy.

**Strategies:**
- `fixed` — splits text into fixed-size chunks (100 chars, 20 overlap)
- `recursive` — uses `RecursiveCharacterTextSplitter` (200 chars, 40 overlap)

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@document.pdf" \
  -F "strategy=recursive"
```

In Postman: `POST http://localhost:8000/ingest?strategy=recursive`, body `form-data` with `file` (File) and optional `strategy` (Text).

### Create a booking (direct)

```json
POST /booking
{
  "name": "Prasun Bhattarai",
  "email": "prasun@example.com",
  "date": "2026-06-15",
  "time": "10:00"
}
```

## Services

| Service | Image | Port |
|---------|-------|------|
| FastAPI | palm-mind-rag-backend-fastapi | `8000:80` |
| PostgreSQL | postgres:17 | `5432` |
| Redis | redis:latest | `6379` |
| Qdrant | qdrant/qdrant:latest | `6333` |

## Project Structure

```
app/
  api/          # Route handlers (chat, ingest, booking)
  core/         # Config
  db/           # Database clients (PostgreSQL, Redis, Qdrant)
  models/       # SQLAlchemy models
  services/     # Business logic (RAG, ingestion, booking, LLM)
  utils/        # Utilities (PDF reader, chunking, embeddings)
  main.py       # FastAPI entry point with lifespan (creates DB tables and Qdrant collection at startup)
```
