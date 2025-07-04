"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import Image from "next/image";

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const searchParams = useSearchParams();
  const username = searchParams.get("username");
  const balanceStr = searchParams.get("balance");
  const balance = balanceStr ? parseFloat(balanceStr) : null;

  const toggleMenu = () => {
    setIsOpen((prev) => !prev);
  };

  return (
    <header className="w-full z-10 bg-white shadow-sm">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Link href="/" className="flex items-center group">
              <div className="relative w-12 h-12 mr-2">
                <Image
                  src="/Nimbuslogo.png"
                  alt="Nimbus Logo"
                  fill
                  className="object-contain"
                  priority
                />
              </div>
              <span className="text-2xl font-bold text-gray-800 relative">
                Ni
                <span className="text-[#0288D1]">m</span>
                <span className="text-[#0288D1]">b</span>
                us
                <span className="absolute -bottom-1 left-0 w-full h-0.5 bg-[#408830] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 ease-out"></span>
              </span>
            </Link>
          </motion.div>
        </div>

        {/* Show balance if available */}
        {username && balance !== null && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="text-right"
          >
            <div className="text-sm text-gray-700">
              Hello, <span className="font-semibold">{username}</span>!
            </div>
            <div className="text-green-700 font-semibold">
              Balance: ${balance.toFixed(2)}
            </div>
          </motion.div>
        )}
      </div>
    </header>
  );
};

export default Header;
