"use client";

import { useState, useEffect } from "react";
import { Card } from "@/components/ui/Card";
import { apiClient } from "@/lib/api";

export default function AdminAnalytics() {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient("/admin/analytics/platform").then((data) => {
      if (data.success) setAnalytics(data.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Platform Analytics</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <p className="text-sm text-gray-500">Total Restaurants</p>
          <p className="text-3xl font-bold">{analytics?.total_restaurants || 0}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-500">Total Chats</p>
          <p className="text-3xl font-bold">{analytics?.total_chats || 0}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-500">Tokens Used</p>
          <p className="text-3xl font-bold">{analytics?.total_tokens_used || 0}</p>
        </Card>
      </div>
    </div>
  );
}
