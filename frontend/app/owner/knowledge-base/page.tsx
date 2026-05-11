"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { apiClient } from "@/lib/api";
import type { KnowledgeChunk } from "@/types";

export default function OwnerKnowledgeBase() {
  const [chunks, setChunks] = useState<KnowledgeChunk[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient("/owner/knowledge-base", {
      headers: { "X-Restaurant-ID": "placeholder" },
    }).then((data) => {
      if (data.success) setChunks(data.data || []);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Knowledge Base</h1>
        <Button>Add Entry</Button>
      </div>
      <div className="grid gap-4">
        {chunks.length === 0 && (
          <Card>
            <p className="text-gray-500">
              No knowledge base entries yet. Add restaurant info, FAQs, and
              specials here.
            </p>
          </Card>
        )}
        {chunks.map((chunk) => (
          <Card key={chunk.id}>
            <p>{chunk.content}</p>
            <p className="text-xs text-gray-400 mt-2">{chunk.source_type}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
