# MenuMind — Multi-Tenant Restaurant AI Chatbot Platform

AI-powered food recommendations platform. Customers scan a QR code at a restaurant, land on a branded chat page, and get personalized dish recommendations based on their dietary profile — using only that restaurant's menu data.

## Architecture

![MenuMind System Architecture](docs/diagrams/menumind_system_architecture.svg)

## Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.12+ (for local dev without Docker)
- Node.js 20+ (for local frontend dev)
- [uv](https://docs.astral.sh/uv/) (Python package manager, used instead of pip)

### Setup

```bash
# 1. Clone and enter the project
git clone <repo-url> menumind
cd menumind

# 2. Configure environment variables
cp .env.example .env
# Edit .env — add your OpenAI API key, Pinecone credentials, etc.

# 3. Start all services
docker-compose up --build

# 4. Run database migrations (in another terminal)
make migrate

# 5. Seed sample data
make seed
```

### Access the App

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Admin Panel | http://localhost:3000/admin |

## Seed Accounts

| Role | Email | Password | Description |
|------|-------|----------|-------------|
| Admin | admin@menumind.com | admin123 | Platform superadmin |
| Owner 1 | owner@pizzeria.com | owner123 | Tony's Pizzeria |
| Owner 2 | owner@sushi.com | owner123 | Sakura Sushi |
| Consumer 1 | alice@example.com | consumer123 | Spicy vegetarian, peanut allergy |
| Consumer 2 | bob@example.com | consumer123 | Seafood lover, gluten/lactose |

## Project Structure

```
menumind/
├── backend/             # FastAPI + Celery + AI pipeline
│   ├── app/
│   │   ├── core/        # Config, DB, security, redis
│   │   ├── common/      # Middleware, exceptions, utils
│   │   ├── modules/     # Feature domains (auth, menus, chats, ai, ...)
│   │   ├── tasks/       # Celery background jobs
│   │   └── tests/       # Unit + integration tests
│   ├── Dockerfile
│   ├── pyproject.toml   # Dependencies (uv)
│   └── uv.lock          # Lockfile
├── frontend/            # Next.js 14 + Tailwind CSS
│   ├── app/             # App Router pages
│   │   ├── dashboard/   # Consumer dashboard
│   │   └── ...
│   ├── components/      # Shared UI components
│   ├── lib/             # API client, auth helpers
│   └── types/           # TypeScript type definitions
├── docs/                # Documentation
│   ├── architecture/    # System design docs
│   ├── api/             # API reference
│   ├── diagrams/        # Architecture diagrams
│   └── user-journeys.md # User journeys by role
├── infra/               # Nginx, Terraform, scripts
├── docker-compose.yml
├── Makefile
└── .env.example
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.0 (async) |
| **Database** | PostgreSQL 16 (asyncpg) |
| **Cache / Queue** | Redis + Celery |
| **Vector Store** | Pinecone (pgvector fallback ready) |
| **AI / LLM** | OpenAI GPT-4o, text-embedding-3-small |
| **AI Framework** | LangChain |
| **Auth** | JWT (access + refresh tokens), bcrypt |
| **Frontend** | Next.js 14 (App Router), Tailwind CSS, TypeScript |
| **Infra** | Docker, Docker Compose |

## Multi-Tenancy

Every restaurant is an isolated tenant:

- **PostgreSQL**: All tables scoped by `restaurant_id` FK
- **Pinecone**: Separate namespace per restaurant (`rest_{id}`)
- **Redis**: All cache keys prefixed with `restaurant_id`
- **Middleware**: `X-Restaurant-ID` header resolved on every request

See [docs/architecture/multi-tenancy.md](docs/architecture/multi-tenancy.md) for details.

## Key Features

- **Consumer**: Branded chat page (QR → chat), AI recommendations, image upload (vision), allergy safety warnings, dietary profile, personal dashboard
- **Owner**: Menu CRUD, CSV bulk upload, knowledge base editor, QR code generator (PNG download), analytics dashboard
- **Admin**: Tenant management, user management, platform analytics, billing plan assignment
- **AI**: RAG pipeline (embed → retrieve → rerank → generate), vision-based dish identification, streaming SSE responses

## API Overview

Base URL: `http://localhost:8000/api/v1`

| Endpoint | Description |
|----------|-------------|
| `POST /auth/register` | Create account |
| `POST /auth/login` | Authenticate |
| `POST /consumer/chat/{slug}/message` | Chat with AI (SSE stream) |
| `GET /owner/menu` | List menu items |
| `POST /owner/menu/bulk-upload` | CSV menu upload |
| `GET /admin/restaurants` | List tenants |
| `GET /health` | Health check |

Full API reference: [docs/api/endpoints.md](docs/api/endpoints.md)
User journeys: [docs/user-journeys.md](docs/user-journeys.md)

## Development

```bash
# Run tests
make test

# Run linter
make lint

# Create a new migration
make migrate-new name="description"

# View logs
make logs
```

## Docker Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `postgres` | postgres:16-alpine | 5432 | Primary database |
| `redis` | redis:7-alpine | 6379 | Cache, queue, rate limiting |
| `backend` | (custom) | 8000 | FastAPI application |
| `celery_worker` | (custom) | — | Async task processor |
| `celery_beat` | (custom) | — | Scheduled tasks |
| `frontend` | (custom) | 3000 | Next.js application |

## Environment Variables

Key variables (see `.env.example` for full list):

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `JWT_SECRET_KEY` | Secret for signing JWT tokens |
| `OPENAI_API_KEY` | OpenAI API key |
| `PINECONE_API_KEY` | Pinecone API key |
| `PINECONE_INDEX_NAME` | Pinecone index name |
| `CELERY_BROKER_URL` | Redis URL for Celery broker |

## License

See [LICENSE](LICENSE).
