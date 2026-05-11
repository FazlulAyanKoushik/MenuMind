"use client";

import { ReactNode, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getStoredUser, logout } from "@/lib/auth";

export default function OwnerLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const u = getStoredUser();
    if (!u || u.role !== "owner") {
      router.push("/login");
    } else {
      setUser(u);
    }
  }, [router]);

  if (!user) return null;

  const navLinks = [
    { href: "/owner/dashboard", label: "Dashboard" },
    { href: "/owner/menus", label: "Menu" },
    { href: "/owner/knowledge-base", label: "Knowledge Base" },
    { href: "/owner/qr-code", label: "QR Code" },
    { href: "/owner/analytics", label: "Analytics" },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/owner/dashboard" className="font-bold text-lg">
            MenuMind
          </Link>
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              {link.label}
            </Link>
          ))}
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
