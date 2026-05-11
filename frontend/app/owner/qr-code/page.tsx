"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { apiClient } from "@/lib/api";

export default function OwnerQRCode() {
  const [qrData, setQrData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function fetchQR() {
    setLoading(true);
    const data = await apiClient("/owner/qr-code", {
      headers: { "X-Restaurant-ID": "placeholder" },
    });
    if (data.success) setQrData(data.data);
    setLoading(false);
  }

  async function regenerate() {
    setLoading(true);
    const data = await apiClient("/owner/qr-code/regenerate", {
      method: "POST",
      headers: { "X-Restaurant-ID": "placeholder" },
    });
    if (data.success) setQrData(data.data);
    setLoading(false);
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">QR Code</h1>
      <Card>
        {!qrData ? (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">
              Generate a QR code for your restaurant chat page.
            </p>
            <Button onClick={fetchQR} disabled={loading}>
              Generate QR Code
            </Button>
          </div>
        ) : (
          <div className="text-center py-4">
            <p className="text-sm text-gray-500 mb-2">
              Scan to start chatting:
            </p>
            <p className="font-mono text-sm mb-4">{qrData.chat_url}</p>
            <img
              src={`data:image/png;base64,${qrData.qr_png_base64}`}
              alt="QR Code"
              className="mx-auto w-48 h-48 mb-4"
            />
            <div className="flex gap-2 justify-center">
              <Button
                onClick={() => {
                  const a = document.createElement("a");
                  a.href = `data:image/png;base64,${qrData.qr_png_base64}`;
                  a.download = `qr-${qrData.slug}.png`;
                  a.click();
                }}
              >
                Download PNG
              </Button>
              <Button variant="secondary" onClick={regenerate} disabled={loading}>
                Regenerate
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
