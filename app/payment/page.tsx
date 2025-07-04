'use client';

import React, { useRef, useCallback, useState, useEffect } from 'react';
import Webcam from 'react-webcam';

type CartItem = { itemId: number; name: string; quantity: number; price: number; };

export default function PaymentPage() {
  const webcamRef = useRef<Webcam>(null);
  const [error, setError]       = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);

  useEffect(() => {
    setCartItems([
      { itemId: 1, name: 'Apple',  quantity: 3, price: 0.5 },
      { itemId: 2, name: 'Banana', quantity: 2, price: 0.75 },
      { itemId: 7, name: 'Milk',   quantity: 1, price: 2.50 },
    ]);
  }, []);

  const total = cartItems.reduce((sum, i) => sum + i.quantity * i.price, 0);

  // just do face recognition and set username
  const captureOnly = useCallback(async () => {
    setError(null);
    setUsername(null);

    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) {
      setError('Could not capture your face.');
      return;
    }

    // dataURL → Blob
    const res  = await fetch(imageSrc);
    const blob = await res.blob();

    const form = new FormData();
    form.append('file', blob, 'face.jpg');

    try {
      const detect = await fetch('/predict-person', {
        method: 'POST',
        body: form,
      });
      if (!detect.ok) throw new Error(await detect.text());
      const { name } = await detect.json();

      if (!name || name === 'Unknown') {
        setError('Face not recognized');
      } else {
        setUsername(name);
      }
    } catch(err: any) {
      console.error(err);
      setError('Server error. Please try again.');
    }
  }, []);

  // optional: chain captureOnly then /pay
  const captureAndPay = useCallback(async () => {
    await captureOnly();
    if (!username) return;
    // call /pay with user_id, cartItems, total…
  }, [captureOnly, username]);

  return (
    <div className="flex p-4 gap-6">

      {/* left: live webcam + capture button + immediate greeting */}
      <div className="flex-1 flex flex-col items-center">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={{ width: 640, height: 480, facingMode: 'user' }}
          className="rounded shadow mb-2"
          onUserMediaError={() => setError('Camera access denied')}
        />

        <button
          onClick={captureOnly}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mb-2"
        >
          Capture
        </button>

        {/* show the recognized name right under the camera */}
        {username && (
          <p className="mt-2 text-xl font-semibold text-center">
            Welcome, <span className="text-green-600">{username}</span>!
          </p>
        )}

        {error && <p className="text-red-600 mt-2">{error}</p>}
      </div>

      {/* right: cart summary + Pay button */}
      <aside className="w-1/3 bg-white p-4 rounded shadow flex flex-col">
        <h2 className="text-lg font-medium mb-2">Your Cart</h2>
        <ul className="flex-1 overflow-auto mb-4">
          {cartItems.map(item => (
            <li key={item.itemId} className="flex justify-between py-1">
              <span>{item.name} ×{item.quantity}</span>
              <span>${(item.price * item.quantity).toFixed(2)}</span>
            </li>
          ))}
        </ul>

        <div className="border-t pt-2 mb-4 flex justify-between font-semibold">
          <span>Total:</span>
          <span>${total.toFixed(2)}</span>
        </div>

        <button
          onClick={captureAndPay}
          className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Pay
        </button>
      </aside>
    </div>
  );
}
