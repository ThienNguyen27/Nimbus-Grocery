'use client';

import React, { useRef, useCallback, useState } from 'react';
import Webcam from 'react-webcam';

export default function PaymentPage() {
  const webcamRef = useRef<Webcam>(null);
  const [error, setError] = useState<string | null>(null);

  const videoConstraints = {
    width: 640,
    height: 480,
    facingMode: 'user',
  };

  const captureAndPay = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      // TODO: send imageSrc to your face‐detection AI service,
      // then complete the payment flow on success.
      console.log('Face snapshot:', imageSrc);
    } else {
      setError('Could not capture image. Please try again.');
    }
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Show your face</h1>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <div className="mb-4">
        <Webcam
          audio={false}
          height={videoConstraints.height}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={videoConstraints.width}
          videoConstraints={videoConstraints}
          onUserMediaError={(e) => {
            console.error(e);
            setError('Camera access denied or unavailable.');
          }}
        />
      </div>
      <button
        onClick={captureAndPay}
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Capture & Pay
      </button>
    </div>
  );
}