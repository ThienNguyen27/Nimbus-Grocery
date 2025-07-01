"use client";

import Header from "@/components/header";
import WhyItsSafe from '@/components/WhyItsSafe';

import Link from "next/link";

import { motion } from "framer-motion";


const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 },
};

const staggerChildren = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

export default function About() {
  return (
    <div className="min-h-screen bg-[#FDF6E9]">
      <Header/>
      <main className="container mx-auto px-4 py-16">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-5xl font-bold text-gray-900 mb-4 text-center">
            About Ni
            <span className="text-[#0288D1]">m</span>
            <span className="text-[#0288D1]">b</span>
            us
          </h1>
          <p className="text-xl text-gray-600 mb-12 text-center max-w-3xl mx-auto">
            Redefining payments with facial recognition
          </p>
        </motion.div>

        <motion.div
          className="grid md:grid-cols-2 gap-12 items-center mb-20"
          variants={staggerChildren}
          initial="initial"
          animate="animate"
        >
          <motion.div variants={fadeIn}>
            <h2 className="text-3xl font-semibold text-gray-900 mb-4">
              Our Mission
            </h2>
            <p className="text-gray-600 mb-6 leading-relaxed">
              At Nimbus, our mission is to revolutionize payments by making them faster, safer, and truly contactless.
Using facial biometric authentication, we enable users to pay securely without touching a card, phone, or keypad.

            </p>
           
          </motion.div>
       
        </motion.div>

    <main >
      <WhyItsSafe />
    </main>
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
  <div className="p-4 rounded-lg shadow bg-white text-center">
    <div className="text-4xl mb-2">👁️</div>
    <h3 className="font-semibold text-lg">AI-driven facial ID Powered</h3>
    <p className="text-sm text-gray-600">Pay instantly with facial recognition — no cards, phones, or pins required.</p>
  </div>
  <div className="p-4 rounded-lg shadow bg-white text-center">
    <div className="text-4xl mb-2">🛡️</div>
    <h3 className="font-semibold text-lg">Secure by Design</h3>
    <p className="text-sm text-gray-600">Biometric data never leaves the device, ensuring top-notch privacy and protection.</p>
  </div>
  <div className="p-4 rounded-lg shadow bg-white text-center">
    <div className="text-4xl mb-2">⚡</div>
    <h3 className="font-semibold text-lg">Frictionless Payments</h3>
    <p className="text-sm text-gray-600">No waiting. No wallets. Just look and go — perfect for modern users on the move.</p>
  </div>
  <div className="p-4 rounded-lg shadow bg-white text-center">
    <div className="text-4xl mb-2">🌍</div>
    <h3 className="font-semibold text-lg">Global Ready</h3>
    <p className="text-sm text-gray-600">Nimbus scales across borders and supports diverse markets and merchants.</p>
  </div>
</div>

<h2 className="text-xl font-bold text-center mt-10">Start Paying Smarter</h2>
<p className="text-center text-gray-600">Join Nimbus and experience the future of payment — contactless, secure, and effortless.</p>

        
      </main>
    </div>
  );
}
