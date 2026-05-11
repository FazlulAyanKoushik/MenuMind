"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { apiClient, getAccessToken } from "@/lib/api";

export default function ConsumerDashboard() {
  const router = useRouter();
  const [profile, setProfile] = useState<{
    preferences: string[];
    allergies: string[];
    region: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getAccessToken()) {
      router.push("/login");
      return;
    }
    apiClient("/consumer/profile")
      .then((data) => {
        if (data.success && data.data) {
          setProfile(data.data);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [router]);

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold">My Dashboard</h1>

        <Card>
          <h2 className="font-semibold mb-2">My Profile</h2>
          {profile ? (
            <div className="space-y-1 text-sm text-gray-600">
              <p>
                <span className="font-medium">Preferences:</span>{" "}
                {profile.preferences?.join(", ") || "None set"}
              </p>
              <p>
                <span className="font-medium">Allergies:</span>{" "}
                {profile.allergies?.join(", ") || "None set"}
              </p>
              <p>
                <span className="font-medium">Cuisine Background:</span>{" "}
                {profile.region || "Not set"}
              </p>
            </div>
          ) : (
            <p className="text-sm text-gray-500">
              Complete your profile to get personalized recommendations.
            </p>
          )}
          <Button
            className="mt-4"
            onClick={() => router.push("/profile")}
          >
            {profile ? "Edit Profile" : "Set Up Profile"}
          </Button>
        </Card>

        <Card>
          <h2 className="font-semibold mb-2">Chat with a Restaurant</h2>
          <p className="text-sm text-gray-500 mb-4">
            Scan a restaurant&apos;s QR code or visit their chat page to get
            AI-powered food recommendations.
          </p>
          <p className="text-sm text-gray-400">
            Ask a staff member for the restaurant&apos;s QR code or use the
            chat URL provided at the restaurant.
          </p>
        </Card>
      </div>
    </div>
  );
}
