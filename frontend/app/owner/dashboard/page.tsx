"use client";

import { Card } from "@/components/ui/Card";

export default function OwnerDashboard() {
  const stats = [
    { label: "Today's Chats", value: "—" },
    { label: "Menu Items", value: "—" },
    { label: "Top Dish", value: "—" },
    { label: "AI Status", value: "Active" },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Owner Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        {stats.map((stat) => (
          <Card key={stat.label}>
            <p className="text-sm text-gray-500">{stat.label}</p>
            <p className="text-2xl font-bold mt-1">{stat.value}</p>
          </Card>
        ))}
      </div>
      <Card>
        <h2 className="font-semibold mb-2">Recent Activity</h2>
        <p className="text-gray-500 text-sm">
          Chat logs and activity will appear here once the system is connected.
        </p>
      </Card>
    </div>
  );
}
