"use client";

import { useState, useEffect } from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { apiClient } from "@/lib/api";
import type { Restaurant } from "@/types";

export default function AdminRestaurants() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient("/admin/restaurants").then((data) => {
      if (data.success) setRestaurants(data.data || []);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Restaurants</h1>
      <div className="grid gap-4">
        {restaurants.map((r) => (
          <Card key={r.id} className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold">{r.name}</h3>
              <p className="text-sm text-gray-500">
                {r.slug} — {r.plan} — {r.status}
              </p>
            </div>
            <div className="flex gap-2">
              <Button variant="ghost">Edit</Button>
              <Button variant="danger">Suspend</Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
