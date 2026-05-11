# Multi-Tenancy Model

Every restaurant registered on the platform is an isolated **tenant**. Tenant isolation is enforced at every layer of the stack.

## Database Layer (PostgreSQL)

Every tenant-scoped table includes a `restaurant_id` foreign key column:

| Table | Isolation Column |
|-------|-----------------|
| `menu_items` | `restaurant_id` |
| `knowledge_chunks` | `restaurant_id` |
| `chat_sessions` | `restaurant_id` |
| `chat_messages` | (via `chat_sessions.restaurant_id`) |
| `daily_stats` | `restaurant_id` |
| `qr_codes` | `restaurant_id` |

All queries filter by `restaurant_id`. The `X-Restaurant-ID` header is resolved by middleware and injected into request state.

## Vector Store (Pinecone)

Each restaurant gets a dedicated Pinecone namespace:

```
namespace = f"rest_{restaurant_id}"
```

Menu embeddings and knowledge base chunks are upserted into this namespace only. Queries against Restaurant A will never return results from Restaurant B.

## Cache Layer (Redis)

All cache keys are prefixed with the restaurant ID:

```
key = f"{restaurant_id}:rate_limit:chat:{client_ip}"
key = f"{restaurant_id}:session:{session_id}"
```

## Application Layer (Middleware)

The `TenantMiddleware` extracts `X-Restaurant-ID` from every request header and attaches it to `request.state.restaurant_id`. Route handlers and dependencies access this value to scope all operations.

For QR-code-driven consumer flows, the `restaurant_slug` URL parameter is resolved to a `restaurant_id` via the `restaurants` table.

## Auth Layer

- Consumers authenticate via JWT (optional for chat — guest sessions allowed)
- Owners authenticate via JWT, and their restaurant scope is derived from the `restaurants` table (`owner_id` relationship)
- Admin users operate across all tenants (no restaurant scope)
