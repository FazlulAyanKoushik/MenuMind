"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";

export default function HomePage() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-primary-50 to-white">
      <div className="text-center max-w-lg">
        <h1 className="text-4xl font-bold mb-4">MenuMind</h1>
        <p className="text-lg text-gray-600 mb-8">
          AI-powered food recommendations personalized to your taste and dietary
          needs.
        </p>
        <div className="flex gap-4 justify-center">
          <Button onClick={() => router.push("/login")}>Login</Button>
          <Button
            variant="secondary"
            onClick={() => router.push("/register")}
          >
            Register
          </Button>
        </div>
      </div>
    </div>
  );
}
