"use client";

import { Card } from "@/components/ui/Card";

export default function OwnerAnalytics() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Analytics</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <h2 className="font-semibold mb-4">Chat Volume</h2>
          <p className="text-gray-500 text-sm">
            Chat volume chart will appear here.
          </p>
        </Card>
        <Card>
          <h2 className="font-semibold mb-4">Top Dishes</h2>
          <p className="text-gray-500 text-sm">
            Most mentioned dishes will appear here.
          </p>
        </Card>
      </div>
    </div>
  );
}
