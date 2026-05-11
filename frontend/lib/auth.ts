"use client";

import { setAccessToken } from "./api";

export function login(email: string, password: string, role?: string) {
  return fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/auth/login`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    }
  ).then(async (res) => {
    const data = await res.json();
    if (data.success && data.data) {
      setAccessToken(data.data.access_token);
      localStorage.setItem("refresh_token", data.data.refresh_token);
      localStorage.setItem("user", JSON.stringify(data.data.user));
      if (role) {
        localStorage.setItem("redirect_role", role);
      }
    }
    return data;
  });
}

export function register(
  email: string,
  password: string,
  role: string = "consumer",
  restaurantName?: string
) {
  return fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/auth/register`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        role,
        restaurant_name: restaurantName,
      }),
    }
  ).then(async (res) => {
    const data = await res.json();
    if (data.success && data.data) {
      setAccessToken(data.data.access_token);
      localStorage.setItem("refresh_token", data.data.refresh_token);
      localStorage.setItem("user", JSON.stringify(data.data.user));
    }
    return data;
  });
}

export function logout() {
  setAccessToken(null);
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
  localStorage.removeItem("redirect_role");
}

export function getStoredUser() {
  try {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  } catch {
    return null;
  }
}
