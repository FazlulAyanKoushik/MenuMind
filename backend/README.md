# MenuMind Backend

FastAPI-based backend for the MenuMind multi-tenant restaurant AI chatbot platform.

## Tech Stack

- **Framework**: Python 3.12, FastAPI
- **ORM**: SQLAlchemy 2.0 (async with asyncpg)
- **Database**: PostgreSQL 16
- **Cache / Queue**: Redis + Celery
- **Vector Store**: Pinecone
- **AI**: OpenAI GPT-4o, text-embedding-3-small, LangChain
- **Auth**: JWT (access + refresh tokens), bcrypt
- **File Storage**: AWS S3 (optional)

## Project Structure

```
backend/
├── app/
│   ├── core/                 # Config, database, security, redis, dependencies
│   │   ├── config.py         # Pydantic settings (env-based)
│   │   ├── database.py       # Async engine + session factory
│   │   ├── security.py       # JWT + bcrypt helpers
│   │   ├── redis.py          # Redis client
│   │   ├── dependencies.py   # FastAPI dependency injection
│   │   └── constants.py      # Enums, plan limits
│   │
│   ├── common/               # Shared cross-cutting concerns
│   │   ├── middleware/
│   │   │   ├── tenant.py     # Multi-tenant (X-Restaurant-ID resolver)
│   │   │   ├── rate_limit.py # Redis-based rate limiter
│   │   │   └── token_budget.py
│   │   ├── exceptions/
│   │   ├── pagination/
│   │   ├── responses/
│   │   ├── utils/
│   │   └── validators/
│   │
│   ├── modules/              # Feature/domain-driven modules
│   │   ├── auth/             # User registration, login, JWT
│   │   ├── users/            # Consumer profiles
│   │   ├── tenants/          # Restaurant management
│   │   ├── menus/            # Menu CRUD + bulk upload
│   │   ├── knowledge_base/   # Restaurant knowledge entries
│   │   ├── chats/            # Chat sessions + messages
│   │   ├── qr/               # QR code generation
│   │   ├── ai/               # AI pipeline
│   │   │   ├── embeddings/   # OpenAI embedding + Pinecone client
│   │   │   ├── rag/          # RAG pipeline (retrieve → generate)
│   │   │   ├── vision/       # GPT-4o image analysis
│   │   │   └── prompts/      # System prompt templates
│   │   ├── owner/            # Owner dashboard + analytics
│   │   └── admin/            # Admin panel
│   │
│   ├── tasks/                # Celery background jobs
│   │   ├── celery_app.py     # Celery app configuration
│   │   ├── ai_tasks.py       # Embedding generation
│   │   └── reports.py        # Daily stats aggregation
│   │
│   ├── db/
│   │   ├── base.py           # SQLAlchemy Base with all models
│   │   ├── session.py
│   │   ├── migrations/       # Alembic migration files
│   │   └── seed.py           # Sample data seeder
│   │
│   ├── tests/                # Test suite
│   │   ├── unit/             # Unit tests (auth, rag, utils)
│   │   ├── integration/      # Integration tests
│   │   └── e2e/              # End-to-end tests
│   │
│   └── main.py               # FastAPI app entry point
│
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── alembic.ini
```

## Module Architecture

Each domain module follows a consistent internal pattern:

```
modules/{domain}/
├── router.py       # FastAPI route definitions
├── service.py      # Business logic
├── model.py        # SQLAlchemy model
├── schema.py       # Pydantic request/response schemas
├── repository.py   # Database queries
└── dependencies.py # Module-specific FastAPI dependencies
```

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 16
- Redis 7
- OpenAI API key
- Pinecone API key (optional, falls back gracefully)

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your database URL, API keys, etc.

# Run migrations
alembic upgrade head

# Seed data
python -m app.db.seed

# Start server
uvicorn app.main:app --reload
```

### Docker

```bash
# Build and run with Docker Compose from project root
docker-compose up backend celery_worker celery_beat
```

## API

Full API documentation is available at `/docs` (Swagger UI) or `/redoc` when the server is running.

Base URL: `http://localhost:8000/api/v1`

Key endpoints:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | Login |
| POST | `/auth/refresh` | Refresh token |
| GET | `/consumer/profile` | Get consumer profile |
| PUT | `/consumer/profile` | Update consumer profile |
| POST | `/consumer/chat/{slug}/message` | Chat with AI (SSE) |
| GET | `/owner/menu` | List menu items |
| POST | `/owner/menu` | Create menu item |
| POST | `/owner/menu/bulk-upload` | Bulk CSV upload |
| GET | `/owner/knowledge-base` | List KB entries |
| GET | `/owner/qr-code` | Get QR code |
| GET | `/owner/dashboard` | Dashboard stats |
| GET | `/admin/restaurants` | List restaurants |
| PUT | `/admin/restaurants/{id}/status` | Update status |
| GET | `/admin/analytics/platform` | Platform analytics |
| GET | `/health` | Health check |

## AI Pipeline

The RAG pipeline processes each consumer message through these steps:

1. **Receive** message + optional image
2. **Vision** (if image): GPT-4o identifies the dish
3. **Query construction**: message + vision output + consumer profile
4. **Embedding**: text-embedding-3-small
5. **Vector retrieval**: Pinecone namespace scoped by `restaurant_id`
6. **Reranking**: cosine similarity
7. **Prompt construction**: system prompt + context + history + user message
8. **Generation**: GPT-4o streaming response
9. **Allergy safety**: post-process warning if allergen detected
10. **Logging**: save exchange with token counts

## Celery Tasks

| Task | Trigger | Description |
|------|---------|-------------|
| `embed_menu_item` | Menu create/update/delete | Re-embed menu item in Pinecone |
| `embed_knowledge_chunk` | KB create/update | Re-embed knowledge entry |
| `process_menu_bulk_upload` | CSV upload | Parse + batch embed menu items |
| `aggregate_daily_stats` | Cron (midnight) | Aggregate daily chat/token stats |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/unit/test_auth.py
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL async connection string |
| `REDIS_URL` | Yes | — | Redis connection string |
| `JWT_SECRET_KEY` | Yes | — | JWT signing secret |
| `OPENAI_API_KEY` | Yes | — | OpenAI API key |
| `PINECONE_API_KEY` | No | — | Pinecone API key |
| `PINECONE_INDEX_NAME` | No | menumind | Pinecone index name |
| `CELERY_BROKER_URL` | Yes | — | Redis URL for Celery |
| `LOG_LEVEL` | No | INFO | Logging level |
