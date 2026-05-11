# MenuMind — Multi-Tenant Restaurant AI Chatbot Platform

## Project Overview

Build a production-ready, multi-tenant SaaS platform called **MenuMind**.
The core concept: a consumer visits a restaurant, scans a QR code, lands on that
restaurant's branded chat page, and gets AI-powered food recommendations
personalized to their dietary profile — using only that restaurant's menu data.

---

## Tech Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL (multi-tenant, row-level isolation by restaurant_id)
- **Cache / Queue**: Redis + Celery
- **Vector Store**: Pinecone (namespaced per restaurant) OR pgvector as fallback
- **AI / LLM**: OpenAI GPT-4o (chat + vision), text-embedding-3-small (embeddings)
- **AI Orchestration**: LangChain
- **File Storage**: AWS S3 (food images, menu uploads)
- **Auth**: JWT (access + refresh tokens), role-based (consumer, owner, admin)
- **Frontend**: Next.js 14 (App Router) + Tailwind CSS
- **Deployment**: Docker + Docker Compose (local), AWS ECS or Railway (prod)

---

## User Roles

Three distinct user roles with separate portals:

1. **Consumer** — end user who visits restaurants and chats with the AI
2. **Restaurant Owner** — manages their restaurant's data, menu, and AI knowledge base
3. **Admin** — platform superadmin who manages all tenants and billing

---

## Multi-Tenancy Model

Every restaurant is a **tenant**. All database queries and vector store lookups
MUST be scoped to a `restaurant_id`. No data from Restaurant A should ever
appear in Restaurant B's chat.

- PostgreSQL: every relevant table has a `restaurant_id` FK column
- Pinecone: use a separate namespace per `restaurant_id` (e.g. namespace = `rest_abc123`)
- Redis: cache keys prefixed with `restaurant_id`
- Middleware: a FastAPI middleware resolves `restaurant_id` from the request
  (QR URL param or JWT claim) on every request

---

## Feature Specification

### 1. Consumer Portal

#### QR Code Flow
- Each restaurant has a unique QR code URL: `/chat/{restaurant_slug}`
- Scanning the QR opens a branded chat page for that specific restaurant
- Consumer can use it as a guest (session-based) or log in / register for a profile
- The page shows the restaurant name, logo, and a chat interface

#### Consumer Profile
- Consumers can create an account and set:
  - Favorite food preferences (e.g. spicy, vegetarian, seafood lover)
  - Allergy information (e.g. peanuts, gluten, lactose) — stored as a list
  - Region / cuisine background (e.g. South Asian, Mediterranean)
- Profile data is injected into every AI prompt as a system-level context block

#### Chat Interface
- Full conversational chat UI (message history visible in the session)
- Consumer can type questions about food (e.g. "What do you recommend for lunch?", "Any spicy dishes?")
- Consumer can upload a photo of a food item
- The AI will:
  1. Analyze the uploaded image using GPT-4o Vision to identify the dish
  2. Search the restaurant's menu for similar or related items
  3. Cross-check with the consumer's allergy and preference profile
  4. Return a personalized recommendation with dish name, description, price, and why it matches
- Chat history is stored per session (and per user if logged in)

#### Allergy Safety
- If a recommended dish contains an ingredient matching the consumer's allergy list,
  the system MUST warn the consumer and suggest a safe alternative
- This check is a hard rule applied after RAG retrieval, before response generation

---

### 2. Restaurant Owner Portal

#### Authentication
- Owner registers with email, password, restaurant name
- Admin approves or auto-approves new restaurant accounts (configurable)

#### Dashboard
- Overview cards: total chat sessions today, most asked-about dishes, top recommendations given
- Recent chat logs (anonymized, no PII)
- Embedding status: shows whether menu is indexed and up to date

#### Menu Management
- CRUD interface for menu items with fields:
  - name, description, price, category, ingredients (list), allergens (list),
    cuisine_type, is_available (bool), image_url
- Bulk upload via CSV or PDF (parsed server-side, Celery job)
- When a menu item is created, updated, or deleted → trigger a Celery task to
  re-embed and update the Pinecone namespace for that restaurant

#### Knowledge Base Editor
- Rich text editor for owner to add extra context: restaurant story, chef specials,
  daily offers, FAQ (e.g. "Do you do takeaway?", "What are your opening hours?")
- This content is chunked, embedded, and stored in the same Pinecone namespace

#### QR Code Generator
- Auto-generate QR code for the restaurant's `/chat/{restaurant_slug}` URL
- Downloadable as PNG and SVG
- Owner can regenerate / rotate the slug if needed

#### Analytics
- Daily/weekly chart of chat volume
- Top 10 dishes mentioned in chats
- Consumer satisfaction signal (thumbs up/down on AI responses)

---

### 3. Admin Portal

#### Tenant Management
- List all registered restaurants with status (active, pending, suspended)
- Approve / suspend / delete a restaurant account
- View per-restaurant usage stats (chat count, token usage, embedding size)

#### User Management
- View all consumers and owners
- Manually assign or revoke roles
- Impersonate an owner (for support purposes, logged)

#### Platform Analytics
- Total platform chat volume over time
- Token usage and cost estimate by restaurant
- Top restaurants by engagement

#### Billing / Subscription (stub or full, mark clearly)
- Simple plan tiers: Free (50 chats/month), Pro (1000 chats/month), Enterprise (unlimited)
- Admin can manually assign a plan to a restaurant
- (Stub Stripe integration for future payment processing)

---

## AI System — RAG Architecture

### Pipeline (per consumer message)

1. **Receive** the consumer's message + optional image
2. **Vision step** (if image present): send image to GPT-4o Vision with prompt:
   "Identify this food dish. Return: dish name, key ingredients, cuisine type."
3. **Query construction**: combine the user message + vision output (if any) +
   consumer profile (allergies, preferences, region) into a structured query string
4. **Embedding**: embed the query using text-embedding-3-small
5. **Vector retrieval**: query Pinecone namespace for `restaurant_id`, top-k=8 results
6. **Reranking**: use a simple cosine similarity rerank or LangChain contextual compression
7. **Prompt construction**: build the final prompt with:
   - System prompt: role definition + restaurant context + consumer profile injection
   - Retrieved context: relevant menu items and knowledge base chunks
   - Allergy safety instruction: hard rule block
   - Conversation history: last N messages
   - User message
8. **Generate**: send to GPT-4o, stream the response back to the frontend
9. **Safety check**: post-process to detect if any recommended dish contains an allergen
   from the consumer's profile. If yes, prepend a warning block to the response.
10. **Log**: save the exchange to chat_sessions table with token counts

### System Prompt Template (inject at runtime)
```text
You are MenuMind, a friendly AI food assistant for {restaurant_name}.
You ONLY recommend dishes available at this restaurant.
Do NOT mention any dishes, ingredients, or restaurants outside this context.
Consumer profile:

Dietary preferences: {preferences}
Allergies: {allergies}
Cuisine background: {region}

CRITICAL RULE: If a dish contains any ingredient from the consumer's allergy list,
you MUST clearly warn them before suggesting it and offer a safe alternative.
Use the menu context below to answer. If the answer is not in the context, say
"I don't have that information — please ask a staff member.
```

---

## Database Schema (key tables)

```sql
-- Core tenant
restaurants (id, slug, name, logo_url, plan, status, owner_id, created_at)

-- Users
users (id, email, password_hash, role ENUM('consumer','owner','admin'), created_at)

-- Consumer profiles
consumer_profiles (id, user_id, preferences[], allergies[], region, updated_at)

-- Menu
menu_items (id, restaurant_id, name, description, price, category,
            ingredients[], allergens[], cuisine_type, is_available,
            image_url, embedding_status, created_at, updated_at)

-- Knowledge base
knowledge_chunks (id, restaurant_id, content, source_type, created_at)

-- Chat
chat_sessions (id, restaurant_id, user_id, started_at)
chat_messages (id, session_id, role ENUM('user','assistant'), content,
               image_url, tokens_used, created_at)

-- QR codes
qr_codes (id, restaurant_id, slug, image_url, created_at)

-- Analytics
daily_stats (id, restaurant_id, date, chat_count, token_count)
```

---

## API Structure
```doctest
/api/v1/
auth/
POST /register
POST /login
POST /refresh
POST /logout
consumer/
GET  /profile
PUT  /profile
GET  /chat/{restaurant_slug}/history
POST /chat/{restaurant_slug}/message   ← main chat endpoint (streaming)
owner/
GET  /dashboard
GET  /menu
POST /menu
PUT  /menu/{item_id}
DELETE /menu/{item_id}
POST /menu/bulk-upload
GET  /knowledge-base
POST /knowledge-base
PUT  /knowledge-base/{chunk_id}
DELETE /knowledge-base/{chunk_id}
GET  /qr-code
POST /qr-code/regenerate
GET  /analytics
admin/
GET  /restaurants
PUT  /restaurants/{id}/status
GET  /users
PUT  /users/{id}/role
GET  /analytics/platform
PUT  /restaurants/{id}/plan
```

---

## Celery Background Jobs

- `embed_menu_item(item_id)` — called on menu item create/update/delete
- `embed_knowledge_chunk(chunk_id)` — called on knowledge base change
- `process_menu_bulk_upload(file_path, restaurant_id)` — CSV/PDF parsing + batch embed
- `aggregate_daily_stats()` — cron, runs at midnight per restaurant

---

## Frontend Pages

### Consumer
- `/chat/[restaurant_slug]` — main chat page, restaurant-branded, public
- `/profile` — consumer profile settings (authenticated)
- `/login`, `/register`

### Owner
- `/owner/dashboard`
- `/owner/menu`
- `/owner/menu/new`, `/owner/menu/[id]/edit`
- `/owner/knowledge-base`
- `/owner/qr-code`
- `/owner/analytics`
- `/owner/settings`

### Admin
- `/admin/restaurants`
- `/admin/users`
- `/admin/analytics`
- `/admin/settings`

---

## Non-Functional Requirements

- All API responses include `X-Request-ID` header for tracing
- Rate limiting: 30 chat messages per consumer per minute (Redis)
- Token budgeting: warn owner via dashboard if monthly token usage > 80% of plan limit
- Input validation: all user inputs sanitized (Pydantic models server-side)
- File upload: max 5MB, only jpeg/png/webp accepted for food images
- Embeddings regenerated automatically within 60 seconds of menu change (Celery)
- Chat streaming via Server-Sent Events (SSE) or WebSocket
- Logging: structured JSON logs, log level configurable via env
- Environment config: all secrets via `.env` / AWS Secrets Manager, never hardcoded

---

## Folder Structure
```doctest
menumind/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── core/                 # global app setup
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   ├── redis.py
│   │   │   ├── dependencies.py
│   │   │   └── constants.py
│   │   │
│   │   ├── common/               # reusable shared logic
│   │   │   ├── exceptions/
│   │   │   ├── middleware/
│   │   │   ├── pagination/
│   │   │   ├── responses/
│   │   │   ├── utils/
│   │   │   └── validators/
│   │   │
│   │   ├── modules/              # feature/domain driven
│   │   │
│   │   │   ├── auth/
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   ├── model.py
│   │   │   │   ├── schema.py
│   │   │   │   ├── repository.py
│   │   │   │   └── dependencies.py
│   │   │   │
│   │   │   ├── users/
│   │   │   ├── tenants/
│   │   │   ├── menus/
│   │   │   ├── qr/
│   │   │   ├── chats/
│   │   │   ├── knowledge_base/
│   │   │   ├── ai/
│   │   │   │   ├── agents/
│   │   │   │   ├── rag/
│   │   │   │   ├── embeddings/
│   │   │   │   ├── vision/
│   │   │   │   └── prompts/
│   │   │   │
│   │   │   └── admin/
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── migrations/
│   │   │
│   │   ├── tasks/
│   │   │   ├── celery_app.py
│   │   │   ├── emails.py
│   │   │   ├── ai_tasks.py
│   │   │   └── reports.py
│   │   │
│   │   └── tests/
│   │       ├── unit/
│   │       ├── integration/
│   │       └── e2e/
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── (public)/
│   │   │   └── chat/[slug]/
│   │   │
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   │
│   │   ├── owner/
│   │   │   ├── dashboard/
│   │   │   ├── menus/
│   │   │   ├── analytics/
│   │   │   └── knowledge-base/
│   │   │
│   │   ├── admin/
│   │   │
│   │   └── api/
│   │
│   ├── components/
│   │   ├── ui/                   # design system
│   │   ├── chat/
│   │   ├── forms/
│   │   ├── dashboard/
│   │   └── shared/
│   │
│   ├── features/                 # frontend domain modules
│   │   ├── auth/
│   │   ├── chat/
│   │   ├── menu/
│   │   ├── ai/
│   │   └── analytics/
│   │
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── socket.ts
│   │   └── utils.ts
│   │
│   ├── hooks/
│   ├── stores/                   # Zustand/Jotai/Redux
│   ├── types/
│   ├── services/
│   ├── styles/
│   └── Dockerfile
│
├── infra/
│   ├── nginx/
│   ├── docker/
│   ├── scripts/
│   └── terraform/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   └── diagrams/
│
├── .env.example
├── docker-compose.yml
├── Makefile
├── README.md
└── .gitignore
```
---

## Build Order (recommended sequence for AI agent)

1. Docker Compose setup (postgres, redis, backend, frontend)
2. Database models + migrations (Alembic)
3. Auth system (register, login, JWT, role guard)
4. Multi-tenant middleware
5. Owner: menu CRUD + Celery embedding pipeline + Pinecone integration
6. Owner: knowledge base + bulk upload
7. Consumer: profile CRUD
8. Consumer: chat endpoint — RAG pipeline (text only first)
9. Consumer: vision agent integration (image upload → food ID → RAG)
10. Consumer: allergy safety post-processor
11. Owner: QR code generator
12. Owner: analytics dashboard
13. Admin: tenant + user management
14. Admin: platform analytics
15. Frontend: consumer chat page (streaming UI)
16. Frontend: owner portal pages
17. Frontend: admin portal pages
18. Rate limiting + token budgeting
19. Tests (pytest: unit + integration for RAG pipeline and auth)
20. README + .env.example

---

## Deliverables

- Fully working Docker Compose local environment (`docker-compose up` starts everything)
- Seed script that creates: 1 admin, 2 sample restaurants with owners, sample menus,
  and 2 consumer accounts
- Postman collection OR auto-generated OpenAPI docs at `/docs`
- README with setup instructions, environment variables, and architecture notes



---
## Parallel Agent Workstreams
This project is designed to be built by multiple AI agents working simultaneously.
Split the work across the following independent lanes. Each lane has no hard dependency
on the others during initial build — they integrate at the end.

---

### Lane 1 — Backend Core (Agent 1)
- Docker Compose setup (postgres, redis, backend service)
- Database models + Alembic migrations
- Auth system: register, login, JWT, role guard, refresh token
- Multi-tenant middleware: restaurant_id resolver
- Admin API: tenant management, user management, platform analytics
- Owner API: settings, QR code generator, analytics endpoints
- Seed script: 1 admin, 2 restaurants, 2 consumers, sample menus

### Lane 2 — AI Pipeline (Agent 2)
- Pinecone client setup with per-restaurant namespace logic
- Embedding service: text-embedding-3-small, chunk + upsert menu items
- RAG pipeline: query embed → retrieve → rerank → prompt build → stream
- Vision agent: GPT-4o image input → dish identification → RAG handoff
- Allergy safety post-processor
- Consumer profile injector (preferences + allergies into system prompt)
- Celery tasks: embed_menu_item, embed_knowledge_chunk, process_bulk_upload
- Unit tests for RAG pipeline (mock Pinecone + mock OpenAI)

### Lane 3 — Owner + Consumer APIs (Agent 3)
- Owner API: menu CRUD, bulk upload (CSV/PDF parse), knowledge base CRUD
- Consumer API: profile CRUD, chat endpoint (calls Lane 2 AI service internally)
- Chat session + message persistence (chat_sessions, chat_messages tables)
- Rate limiting middleware (Redis, 30 msgs/min per consumer)
- Token usage logging per message
- Integration tests for chat endpoint

### Lane 4 — Frontend (Agent 4)
- Next.js 14 project setup with Tailwind CSS
- Consumer: `/chat/[slug]` page — streaming chat UI, image upload, typing indicator
- Consumer: `/profile` page — allergy, preferences, region form
- Owner portal: dashboard, menu management, knowledge base, QR code, analytics
- Admin portal: restaurant list, user management, platform analytics
- Shared: auth pages (login, register), API client with JWT refresh logic,
  role-based route guards

---

### Integration Checkpoint

After all lanes complete, one agent (or you manually) runs the integration step:
- Wire Lane 3 chat endpoint to call Lane 2 AI service
- Confirm Lane 1 middleware is applied to all Lane 3 routes
- Connect Lane 4 frontend API client to Lane 1/3 backend base URL
- Run `docker-compose up` and verify end-to-end: QR URL → chat → AI response
- Run full test suite

---

### Shared Contract (all agents must follow)

- Base URL for all API calls: `http://localhost:8000/api/v1`
- Auth header: `Authorization: Bearer <access_token>`
- All requests include `X-Restaurant-ID` header (set by middleware, not client)
- Streaming chat uses Server-Sent Events (SSE) at `POST /consumer/chat/{slug}/message`
- SSE format: `data: {"delta": "...", "done": false}` → final: `data: {"done": true}`
- Shared `.env.example` is the single source of truth for all environment variables
- All agents write to the same repo folder structure defined above