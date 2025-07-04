"use client";

import React, { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

export default function PredictPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [loadingModel, setLoadingModel] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function setupCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
        return new Promise<void>((resolve) => {
          videoRef.current!.onloadedmetadata = () => resolve();
        });
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    }

    async function loadModelAndPredict() {
      await setupCamera();
      const video = videoRef.current!;
      const canvas = canvasRef.current!;
      const ctx = canvas.getContext("2d")!;

      // Load YOLO model (TS-safe)
      const model = await (window as any).yolo.load();
      setLoadingModel(false);

      const predictFrame = async () => {
        if (video.readyState === 4) {
          // Resize canvas to match video
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Run detection
          const predictions = await model.detect(video);

          // Draw boxes & labels inline
          ctx.lineWidth = 2;
          ctx.font = "16px sans-serif";
          ctx.textBaseline = "top";
          predictions.forEach((pred: any) => {
            const [x, y, w, h] = pred.bbox as [number, number, number, number];
            const label = (pred.className || pred.label || pred.class).toString();
            const score = ((pred.confidence ?? pred.probability ?? 0) * 100).toFixed(1);

            // Box
            ctx.strokeStyle = "green";
            ctx.strokeRect(x, y, w, h);
            // Label background
            const text = `${label} ${score}%`;
            const textW = ctx.measureText(text).width;
            const textH = parseInt(ctx.font, 10);
            ctx.fillStyle = "green";
            ctx.fillRect(x, y - textH - 4, textW + 4, textH + 4);
            // Text
            ctx.fillStyle = "black";
            ctx.fillText(text, x + 2, y - textH - 2);
          });

          // Tally counts
          const newCounts: Record<string, number> = {};
          predictions.forEach((pred: any) => {
            const label = (pred.className || pred.label || pred.class).toString();
            newCounts[label] = (newCounts[label] || 0) + 1;
          });
          setCounts(newCounts);
        }
        requestAnimationFrame(predictFrame);
      };

      predictFrame();
    }

    loadModelAndPredict();
  }, []);

  const goToPay = () => {
    router.push("/payment");
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">🍎 Live Grocery Detection</h1>

      {loadingModel ? (
        <p className="text-gray-500">Loading model and camera...</p>
      ) : (
        <>
          <div className="mb-4 w-full max-w-md text-left">
            <p className="font-medium text-lg mb-2">Detected fruits:</p>
            {Object.keys(counts).length === 0 ? (
              <p className="text-gray-600">None</p>
            ) : (
              <ul className="list-disc list-inside">
                {Object.entries(counts).map(([label, qty]) => (
                  <li key={label} className="text-gray-800">
                    {label}: <span className="font-bold">{qty}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="relative rounded-xl overflow-hidden shadow-lg border-2 border-gray-200">
            <video
              ref={videoRef}
              autoPlay
              muted
              playsInline
              className="w-[480px] h-[360px] object-cover"
            />
            <canvas ref={canvasRef} className="absolute top-0 left-0" />
          </div>
        </>
      )}

      <button
        onClick={goToPay}
        className="mt-4 px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
      >
        Pay
      </button>
    </div>
  );
}
