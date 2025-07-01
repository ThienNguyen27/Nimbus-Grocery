"use client";

import React, { useEffect, useRef, useState } from "react";
import { useRouter } from 'next/navigation';

export default function PredictPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [resultImg, setResultImg] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const startVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    };

    startVideo();

    const interval = setInterval(() => {
      captureAndSend();
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const captureAndSend = async () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      try {
        setLoading(true);
        const res = await fetch("http://localhost:8000/predict", {
          method: "POST",
          body: formData,
        });

        const blobRes = await res.blob();
        const imageUrl = URL.createObjectURL(blobRes);
        setResultImg(imageUrl);
      } catch (err) {
        console.error("Error sending frame to backend:", err);
      } finally {
        setLoading(false);
      }
    }, "image/jpeg");
  };

  const router = useRouter();

   const goToPay = () => {
    router.push('/payment');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">🍎 Live Grocery Detection</h1>

      <div className="rounded-xl overflow-hidden shadow-lg border-2 border-gray-200">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="w-[480px] h-[360px] object-cover"
        />
      </div>

      <canvas ref={canvasRef} style={{ display: "none" }} />

      {loading && <p className="text-gray-500 animate-pulse">Predicting...</p>}

      {resultImg && !loading && (
        <div className="flex flex-col items-center space-y-2">
          <h2 className="text-xl font-semibold text-green-700">Prediction Result</h2>
          <img
            src={resultImg}
            alt="Predicted Result"
            className="w-[480px] rounded-xl border-4 border-green-500 shadow-md transition-opacity duration-300"
          />
        </div>
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
