# MenuMind Frontend

Next.js 14 frontend for the MenuMind multi-tenant restaurant AI chatbot platform.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **State**: React hooks + localStorage (no external state library)
- **API Client**: Custom fetch-based client with JWT refresh

## Project Structure

```
frontend/
├── app/                              # Next.js App Router pages
│   ├── (public)/                     # Public routes (no auth required)
│   │   └── chat/[slug]/              # Consumer chat page (branded per restaurant)
│   ├── (auth)/                       # Authentication routes
│   │   ├── login/                    # Login page
│   │   └── register/                 # Registration page
│   ├── profile/                      # Consumer profile settings (auth required)
│   ├── owner/                        # Owner portal (auth required, role: owner)
│   │   ├── layout.tsx                # Owner nav + auth guard
│   │   ├── dashboard/                # Overview stats
│   │   ├── menus/                    # Menu item list
│   │   ├── knowledge-base/           # Knowledge base entries
│   │   ├── qr-code/                  # QR code generator + download
│   │   ├── analytics/                # Chat volume + top dishes
│   │   └── settings/                 # Restaurant settings
│   ├── admin/                        # Admin portal (auth required, role: admin)
│   │   ├── layout.tsx                # Admin nav + auth guard
│   │   ├── page.tsx                  # Restaurant management
│   │   ├── users/                    # User management
│   │   └── analytics/                # Platform-wide analytics
│   ├── api/                          # API route handlers
│   ├── layout.tsx                    # Root layout
│   ├── page.tsx                      # Landing page
│   └── globals.css                   # Tailwind imports + global styles
│
├── components/                       # Reusable React components
│   ├── ui/                           # Design system primitives
│   │   ├── Button.tsx                # Styled button (primary/secondary/danger/ghost)
│   │   ├── Card.tsx                  # Content container
│   │   └── Input.tsx                 # Form input with label + error state
│   ├── chat/                         # Chat-specific components
│   ├── forms/                        # Form components
│   ├── dashboard/                    # Dashboard widgets
│   └── shared/                       # Shared layout components
│
├── lib/                              # Utility libraries
│   ├── api.ts                        # API client with JWT refresh logic
│   └── auth.ts                       # Auth helpers (login, register, logout)
│
├── types/                            # TypeScript type definitions
│   └── index.ts                      # User, MenuItem, ChatSession, etc.
│
├── hooks/                            # Custom React hooks
├── stores/                           # State management (if needed)
├── services/                         # Service layer
├── styles/                           # Additional styles
│
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── Dockerfile
```

## Pages

### Consumer Routes

| Route | Auth | Description |
|-------|------|-------------|
| `/chat/[slug]` | Optional | Branded chat page — SSE streaming, typing indicator |
| `/profile` | Required | Dietary preferences, allergies, cuisine region |
| `/login` | — | Login form |
| `/register` | — | Registration form (consumer or owner) |

### Owner Routes

| Route | Description |
|-------|-------------|
| `/owner/dashboard` | Overview cards (today's chats, menu count, top dish) |
| `/owner/menus` | Menu item list with edit/delete |
| `/owner/knowledge-base` | Restaurant info, FAQs, specials editor |
| `/owner/qr-code` | Generate + download QR code (PNG) |
| `/owner/analytics` | Chat volume chart, top dishes |
| `/owner/settings` | Restaurant profile settings |

### Admin Routes

| Route | Description |
|-------|-------------|
| `/admin` | Restaurant list with approve/suspend |
| `/admin/users` | Platform user management |
| `/admin/analytics` | Total chats, tokens, restaurants |

## Setup

### Prerequisites

- Node.js 20+
- npm 10+

### Local Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Start development server
npm run dev
```

### Docker

```bash
# Build and run with Docker Compose from project root
docker-compose up frontend
```

## API Client

The custom API client in `lib/api.ts` handles:

- Automatic JWT token attachment via `Authorization` header
- Token refresh on 401 responses (uses `/auth/refresh` endpoint)
- Base URL resolution from `NEXT_PUBLIC_API_URL` environment variable

```typescript
import { apiClient } from "@/lib/api";

// GET request
const data = await apiClient("/consumer/profile");

// POST request
const data = await apiClient("/owner/menu", {
  method: "POST",
  body: JSON.stringify({ name: "Margherita", price: 12.99 }),
});
```

## Streaming Chat

The chat page at `/chat/[slug]` uses Server-Sent Events (SSE) to stream AI responses:

```
POST /api/v1/consumer/chat/{slug}/message
X-Restaurant-ID: {restaurant_id}

SSE response:
data: {"delta": "I", "done": false}
data: {"delta": " recommend", "done": false}
data: {"delta": " the Margherita...", "done": false}
data: {"done": true}
```

## Authentication Flow

1. User logs in → receives `access_token` + `refresh_token`
2. Tokens stored in `localStorage`
3. API client attaches `Authorization: Bearer <access_token>` to all requests
4. On 401, client attempts token refresh via `/auth/refresh`
5. Owner/Admin layouts check role on mount, redirect to `/login` if unauthorized

## Design System

The `components/ui/` directory contains the design system primitives:

- **Button**: `primary` | `secondary` | `danger` | `ghost` variants
- **Card**: Consistent white container with shadow
- **Input**: Labeled input with error state

All components accept standard HTML attributes and a `className` prop for customization.
