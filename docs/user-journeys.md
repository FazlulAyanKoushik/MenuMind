# User Journeys

## 1. Consumer Journey

### Onboarding & First Visit

1. **Scan QR Code** — Consumer scans a restaurant's QR code (on table tent card, receipt, or entrance)
2. **Land on Chat Page** — Opens `http://localhost:3000/chat/{slug}` — branded with restaurant name, logo
3. **Guest or Login** — Can chat immediately as guest (session-based) or login/register for personalized experience
4. **Enter Preferences** — If registered: fills profile (preferences, allergies, cuisine background)

### Chat with AI

1. **Ask a Question** — Types "What's good for lunch?" or "Any spicy dishes?"
2. **Receive Recommendations** — AI responds with dish names, descriptions, prices from that restaurant's menu
3. **Follow-up Questions** — Continues conversation naturally ("Anything dairy-free?", "How much is the Margherita?")
4. **Upload a Photo** — Takes a picture of a dish; AI identifies it via vision and recommends similar items
5. **Allergy Warning** — If a recommended dish contains an allergen the consumer has listed, AI warns and suggests alternatives
6. **End Session** — Closes the page; chat history persists for 30 days (guest) or indefinitely (logged-in)

### Key Pages
- `/chat/{slug}` — Branded chat interface (public, no auth required)
- `/profile` — Preferences, allergies, region settings (auth required)
- `/login`, `/register` — Auth pages

---

## 2. Restaurant Owner Journey

### Account Setup

1. **Register** — Signs up with email, password, restaurant name at `/register`
2. **Account Created** — Status set to `pending`; admin approves or auto-approves
3. **First Login** — Lands on `/owner/dashboard` with empty state prompts

### Manage Menu

1. **View Menu** — Opens `/owner/menu` — sees list of current items (empty initially)
2. **Add Item** — Clicks "Add Item" → fills form: name, description, price, category, ingredients, allergens, cuisine type, availability
3. **Bulk Upload** — Uploads a CSV with all menu items at once
4. **Edit/Delete** — Updates prices, marks items unavailable, removes discontinued dishes
5. **Auto-Indexing** — Each menu change triggers background embedding to Pinecone (menu is searchable by AI within ~60s)

### Knowledge Base

1. **Add Context** — Opens `/owner/knowledge-base` → adds restaurant story, chef specials, daily offers, FAQs
2. **Rich Editor** — Writes free-form content that the AI will use alongside menu data
3. **Publish** — Content is chunked and embedded into the restaurant's Pinecone namespace

### QR Code

1. **Generate QR** — Opens `/owner/qr-code` → sees auto-generated QR pointing to `http://localhost:3000/chat/{slug}`
2. **Download** — Downloads PNG for printing on tables, receipts, or signage
3. **Regenerate** — Rotates the slug if needed (old QR becomes invalid)

### Analytics

1. **Dashboard** — `/owner/dashboard` — sees today's chat count, top recommended dishes, embedding status
2. **Analytics Page** — `/owner/analytics` — weekly chat volume chart, top 10 mentioned dishes, satisfaction signals (thumbs up/down)
3. **Usage Alerts** — Warned via dashboard if monthly token usage exceeds 80% of plan limit

### Key Pages
- `/owner/dashboard` — Overview
- `/owner/menu`, `/owner/menu/new`, `/owner/menu/[id]/edit` — Menu CRUD
- `/owner/knowledge-base` — Knowledge base editor
- `/owner/qr-code` — QR code generator
- `/owner/analytics` — Analytics dashboard
- `/owner/settings` — Account settings

---

## 3. Admin Journey

### Tenant Management

1. **Login** — Signs in with admin credentials at `/login` → redirected to `/admin/restaurants`
2. **View All Tenants** — Sees table of all registered restaurants with status, plan, owner, created date
3. **Approve New Restaurants** — Reviews pending restaurants → approves or rejects
4. **Suspend/Activate** — Suspends a violating restaurant or re-activates a suspended one
5. **Assign Plans** — Upgrades/downgrades restaurant plans (Free → Pro → Enterprise)

### User Management

1. **View Users** — Opens `/admin/users` → sees all platform users with roles
2. **Change Roles** — Promotes a consumer to owner, or assigns admin privileges
3. **Impersonate** — Can view an owner's dashboard for support (logged for audit)

### Platform Analytics

1. **Overview** — `/admin/analytics` — sees total restaurants, total users, total chats, token usage across all tenants
2. **Top Tenants** — Sorted list of restaurants by engagement (chat volume, token consumption)
3. **Cost Tracking** — Token usage and estimated OpenAI cost per restaurant

### Key Pages
- `/admin/restaurants` — Tenant list, approve/suspend
- `/admin/users` — User list, role management
- `/admin/analytics` — Platform-wide stats
- `/admin/settings` — Platform settings

---

## Cross-Cutting Concerns

| Step | Consumer | Owner | Admin |
|------|----------|-------|-------|
| Auth | Optional (guest OK) | Required | Required |
| Restaurant Context | From QR slug | From JWT + header | Selects any |
| Data Scope | Single restaurant | Own restaurant | All restaurants |
| Chat | Unlimited | — | — |
| Menu Management | — | Own menu | — |
| Platform Controls | — | — | Full |
