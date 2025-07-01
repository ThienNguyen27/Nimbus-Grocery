import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;

/** @type {import('next').NextConfig} */
module.exports = {
  async redirects() {
    return [
      {
        source:      '/signup',                            // catch /signup on port 3000
        destination: 'http://127.0.0.1:8000/signup',    // send to FastAPI
        permanent:   false,                                // 307 temporary redirect
      },
      {
        source:      '/signup/',                           // also catch trailing slash
        destination: 'http://127.0.0.1:8000/signup/',
        permanent:   false,
      },
    ];
  },
};