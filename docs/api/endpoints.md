# API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

### POST /auth/register
Create a new user account.

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "role": "consumer",
  "restaurant_name": "My Restaurant"  // required when role = "owner"
}
```

### POST /auth/login
Authenticate and receive JWT tokens.

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### POST /auth/refresh
Refresh an expired access token.

```json
{
  "refresh_token": "..."
}
```

### POST /auth/logout
Invalidate the current session.

---

## Consumer

### GET /consumer/profile
Get the authenticated consumer's dietary profile.
- **Auth**: Bearer token required

### PUT /consumer/profile
Update consumer profile.

```json
{
  "preferences": ["spicy", "vegetarian"],
  "allergies": ["peanuts"],
  "region": "South Asian"
}
```

### GET /consumer/chat/{slug}/history
Get chat history for a restaurant.

### POST /consumer/chat/{slug}/message
Send a chat message and receive an SSE stream of the AI response.
- **Headers**: `X-Restaurant-ID: <restaurant_id>`
- **Auth**: Optional (guest sessions allowed)

```json
{
  "message": "What do you recommend?",
  "session_id": "optional-existing-session-id"
}
```

**SSE Response Format:**
```
data: {"delta": "I", "done": false}
data: {"delta": " recommend", "done": false}
data: {"delta": " the Margherita...", "done": false}
data: {"done": true}
```

---

## Owner

All owner endpoints require `X-Restaurant-ID` header and JWT auth.

### GET /owner/dashboard
Overview stats: today's chats, menu count, embedding status.

### GET /owner/menu
List all menu items.

### POST /owner/menu
Create a new menu item.

### PUT /owner/menu/{item_id}
Update a menu item.

### DELETE /owner/menu/{item_id}
Delete a menu item.

### POST /owner/menu/bulk-upload
Upload a CSV file of menu items (multipart form).

### GET /owner/knowledge-base
List knowledge base entries.

### POST /owner/knowledge-base
Create a knowledge base entry.

### PUT /owner/knowledge-base/{chunk_id}
Update a knowledge base entry.

### DELETE /owner/knowledge-base/{chunk_id}
Delete a knowledge base entry.

### GET /owner/qr-code
Get the restaurant's QR code (PNG as base64).

### POST /owner/qr-code/regenerate
Generate a new slug and QR code.

### GET /owner/analytics
Daily chat/token stats for the last 7 days.

---

## Admin

All admin endpoints require a JWT with `admin` role.

### GET /admin/restaurants
List all restaurants.

### PUT /admin/restaurants/{id}/status
Update restaurant status (active/pending/suspended).

### PUT /admin/restaurants/{id}/plan
Update restaurant plan (free/pro/enterprise).

### GET /admin/users
List all platform users.

### PUT /admin/users/{id}/role
Change a user's role.

### GET /admin/analytics/platform
Platform-wide stats: total restaurants, chats, token usage.

---

## Health

### GET /health
```json
{"status": "healthy", "service": "MenuMind"}
```
