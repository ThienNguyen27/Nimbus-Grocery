'use client';

import React, { useRef, useCallback, useState, useEffect } from 'react';
import Webcam from 'react-webcam';

type CartItem = { itemId: number; name: string; quantity: number; price: number; };

export default function PaymentPage() {
  const webcamRef = useRef<Webcam>(null);
  const [error, setError]       = useState<string | null>(null);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);

  useEffect(() => {
    setCartItems([
      { itemId: 1, name: 'Apple',  quantity: 3, price: 0.5 },
      { itemId: 2, name: 'Banana', quantity: 2, price: 0.75 },
      { itemId: 7, name: 'Milk',   quantity: 1, price: 2.50 },
    ]);
  }, []);

  const total = cartItems.reduce((sum, i) => sum + i.quantity * i.price, 0);

  const captureAndPay = useCallback(async () => {
    setError(null);

    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) {
      setError('Could not capture your face.');
      return;
    }

    // Convert dataURL → Blob
    const res  = await fetch(imageSrc);
    const blob = await res.blob();

    // Build multipart/form-data
    const form = new FormData();
    form.append('file', blob, 'face.jpg');

    const payRequest = {
      items: cartItems.map(item => ({
        item_id: item.itemId,
        quantity: item.quantity,
        price: item.price,
      })),
      total_amount: total,
      description: 'Grocery purchase',
    };
    form.append('request_json', JSON.stringify(payRequest));


    try {
      const response = await fetch('http://localhost:8000/pay', {
        method: 'POST',
        body: form,
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "Payment failed");
      }

      const data = await response.json();
      console.log("Payment successful:", data);
      alert(`Thank you for shopping with us, ${data.user_name}! \nTransaction ID: ${data.transaction_id}`);
      window.location.href = `http://localhost:3001/signin?username=${encodeURIComponent(data.user_name)}&balance=${encodeURIComponent(data.balance)}`;
    } catch (err: any) {
      console.error(err);
      setError("Payment failed: " + (err?.message || ""));
    }
  }, [cartItems, total]);

  return (
    <div className="flex p-4 gap-6">

      {/* left: live webcam + Pay button */}
      <div className="flex-1 flex flex-col items-center">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={{ width: 1280, height: 960, facingMode: 'user' }}
          className="rounded shadow mb-2"
          onUserMediaError={() => setError('Camera access denied')}
        />

        <button
          onClick={captureAndPay}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Pay
        </button>

        {error && <p className="text-red-600 mt-2">{error}</p>}
      </div>

      {/* right: cart summary */}
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
      </aside>
    </div>
  );
}
