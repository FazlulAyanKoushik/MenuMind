"use client";

import { useState, useEffect } from "react";
import { Card } from "@/components/ui/Card";
import { apiClient } from "@/lib/api";

export default function AdminUsers() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient("/admin/users").then((data) => {
      if (data.success) setUsers(data.data || []);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Users</h1>
      <div className="grid gap-4">
        {users.map((u) => (
          <Card key={u.id} className="flex items-center justify-between">
            <div>
              <p className="font-semibold">{u.email}</p>
              <p className="text-sm text-gray-500">Role: {u.role}</p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
