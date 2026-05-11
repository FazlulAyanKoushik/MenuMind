# MenuMind — Multi-Tenant Restaurant AI Chatbot Platform

AI-powered food recommendations platform where restaurant customers can chat with an AI assistant to get personalized menu recommendations.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local dev)
- Node.js 20+ (for local dev)

### Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys (OpenAI, Pinecone, etc.)
```

### Run with Docker
```bash
docker-compose up --build
```

### Run Database Migrations
```bash
make migrate
```

### Seed Sample Data
```bash
make seed
```

### Access the App
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Admin**: http://localhost:3000/admin

## Seed Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@menumind.com | admin123 |
| Owner 1 | owner@pizzeria.com | owner123 |
| Owner 2 | owner@sushi.com | owner123 |
| Consumer 1 | alice@example.com | consumer123 |
| Consumer 2 | bob@example.com | consumer123 |

## Tech Stack

- **Backend**: Python, FastAPI, PostgreSQL, Redis, Celery
- **AI**: OpenAI GPT-4o, Pinecone vector DB, LangChain
- **Frontend**: Next.js 14, Tailwind CSS
- **Infra**: Docker, Docker Compose

## Architecture

See `docs/architecture/` for detailed documentation.

### Multi-Tenancy

Every restaurant is a tenant with row-level isolation via `restaurant_id`:
- PostgreSQL: all relevant tables scoped by `restaurant_id`
- Pinecone: separate namespace per restaurant (`rest_{id}`)
- Redis: cache keys prefixed with `restaurant_id`
