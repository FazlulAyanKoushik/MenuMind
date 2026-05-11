"use client";

import { ReactNode, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getStoredUser, logout } from "@/lib/auth";

export default function AdminLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const u = getStoredUser();
    if (!u || u.role !== "admin") {
      router.push("/login");
    } else {
      setUser(u);
    }
  }, [router]);

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/admin" className="font-bold text-lg">
            MenuMind Admin
          </Link>
          <Link href="/admin" className="text-sm text-gray-600">
            Restaurants
          </Link>
          <Link href="/admin/users" className="text-sm text-gray-600">
            Users
          </Link>
          <Link href="/admin/analytics" className="text-sm text-gray-600">
            Analytics
          </Link>
        </div>
        <button
          onClick={() => {
            logout();
            router.push("/login");
          }}
          className="text-sm text-red-600 hover:underline"
        >
          Logout
        </button>
      </nav>
      <main className="p-6 max-w-6xl mx-auto">{children}</main>
    </div>
  );
}
