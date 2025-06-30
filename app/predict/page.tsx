"use client";

import React, { useEffect, useRef, useState } from "react";

export default function PredictPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [resultImg, setResultImg] = useState<string | null>(null);

  useEffect(() => {
    // Start webcam
    const startVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    };

    startVideo();

    // Capture and send every 2 seconds
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
        const res = await fetch("http://localhost:8000/predict", {
          method: "POST",
          body: formData,
        });

        const blobRes = await res.blob();
        const imageUrl = URL.createObjectURL(blobRes);
        setResultImg(imageUrl);
      } catch (err) {
        console.error("Error sending frame to backend:", err);
      }
    }, "image/jpeg");
  };

  return (
    <div style={{ textAlign: "center", padding: "1rem" }}>
      <h1>Live Grocery Detection</h1>

      <video ref={videoRef} autoPlay muted playsInline style={{ width: "480px", height: "360px", borderRadius: "8px" }} />

      <canvas ref={canvasRef} style={{ display: "none" }} />

      {resultImg && (
        <>
          <h2>Prediction</h2>
          <img src={resultImg} alt="Detected frame" style={{ width: "480px", border: "2px solid green" }} />
        </>
      )}
    </div>
  );
}
