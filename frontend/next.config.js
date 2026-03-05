/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  typescript: {
    tsconfigPath: './tsconfig.json',
  },
  turbopack: {
    root: '.',
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_HEDERA_NETWORK: process.env.NEXT_PUBLIC_HEDERA_NETWORK || 'testnet',
  },
};

module.exports = nextConfig;
