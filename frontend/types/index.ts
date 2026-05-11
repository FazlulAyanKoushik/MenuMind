export interface User {
  id: string;
  email: string;
  role: "consumer" | "owner" | "admin";
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface MenuItem {
  id: string;
  restaurant_id: string;
  name: string;
  description?: string;
  price: number;
  category?: string;
  ingredients: string[];
  allergens: string[];
  cuisine_type?: string;
  is_available: boolean;
  image_url?: string;
}

export interface ChatSession {
  id: string;
  restaurant_id: string;
  user_id?: string;
  started_at: string;
  messages: ChatMessage[];
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: "user" | "assistant";
  content?: string;
  image_url?: string;
  created_at: string;
}

export interface KnowledgeChunk {
  id: string;
  restaurant_id: string;
  content: string;
  source_type: string;
  created_at: string;
}

export interface Restaurant {
  id: string;
  slug: string;
  name: string;
  logo_url?: string;
  plan: string;
  status: string;
  owner_id: string;
}
