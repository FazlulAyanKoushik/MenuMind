"use client";

import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export default function OwnerSettings() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      <Card>
        <div className="space-y-4">
          <Input label="Restaurant Name" placeholder="Your restaurant name" />
          <Input label="Email" type="email" placeholder="owner@example.com" />
          <Button>Save Settings</Button>
        </div>
      </Card>
    </div>
  );
}
