"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { apiClient } from "@/lib/api";
import type { MenuItem } from "@/types";

export default function OwnerMenus() {
  const [items, setItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient("/owner/menu", {
      headers: { "X-Restaurant-ID": "placeholder" },
    }).then((data) => {
      if (data.success) setItems(data.data || []);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Menu Items</h1>
        <Button>Add Item</Button>
      </div>
      <div className="grid gap-4">
        {items.length === 0 && (
          <Card>
            <p className="text-gray-500">
              No menu items yet. Add your first item to get started.
            </p>
          </Card>
        )}
        {items.map((item) => (
          <Card key={item.id} className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold">{item.name}</h3>
              <p className="text-sm text-gray-500">
                {item.category} — ${item.price.toFixed(2)}
              </p>
              <p className="text-xs text-gray-400">
                {item.ingredients.join(", ")}
              </p>
            </div>
            <div className="flex gap-2">
              <Button variant="ghost" size="small">
                Edit
              </Button>
              <Button variant="danger" size="small">
                Delete
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
