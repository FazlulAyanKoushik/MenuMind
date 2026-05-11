"use client";

import { useState, useEffect, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
import { apiClient, getAccessToken } from "@/lib/api";

export default function ProfilePage() {
  const router = useRouter();
  const [preferences, setPreferences] = useState("");
  const [allergies, setAllergies] = useState("");
  const [region, setRegion] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getAccessToken()) {
      router.push("/login");
      return;
    }
    apiClient("/consumer/profile").then((data) => {
      if (data.success && data.data) {
        setPreferences((data.data.preferences || []).join(", "));
        setAllergies((data.data.allergies || []).join(", "));
        setRegion(data.data.region || "");
      }
      setLoading(false);
    });
  }, [router]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    await apiClient("/consumer/profile", {
      method: "PUT",
      body: JSON.stringify({
        preferences: preferences.split(",").map((s) => s.trim()).filter(Boolean),
        allergies: allergies.split(",").map((s) => s.trim()).filter(Boolean),
        region: region || null,
      }),
    });
    alert("Profile updated!");
  }

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-md mx-auto">
        <Card>
          <h1 className="text-2xl font-bold mb-6">My Profile</h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Food Preferences (comma-separated)"
              value={preferences}
              onChange={(e) => setPreferences(e.target.value)}
              placeholder="spicy, vegetarian, seafood lover"
            />
            <Input
              label="Allergies (comma-separated)"
              value={allergies}
              onChange={(e) => setAllergies(e.target.value)}
              placeholder="peanuts, gluten, lactose"
            />
            <Input
              label="Cuisine Background"
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              placeholder="South Asian, Mediterranean"
            />
            <Button type="submit" className="w-full">
              Save Profile
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
}
