import React from 'react';
import Link from 'next/link';

export default function Header() {
  return (
    <header className="w-full bg-gradient-to-r from-[#06122b]/80 via-[#06243a]/60 to-[#05304a]/80 backdrop-blur-sm border-b border-white/6">
      <div className="container flex items-center justify-between py-4">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/10 rounded-md flex items-center justify-center text-white font-bold">F</div>
          <div>
            <div className="text-lg font-semibold">FIND RLB</div>
            <div className="text-xs muted">Rent, Save, Own</div>
          </div>
        </Link>

        <div className="flex-1 mx-6 hidden md:block">
          <div className="relative">
            <input aria-label="Search properties" placeholder="Search city, neighborhood, or property" className="w-full rounded-full py-3 px-4 bg-white/6 placeholder:muted text-sm outline-none focus:ring-2 focus:ring-[#5bc0eb]/50" />
            <button className="absolute right-1 top-1 bottom-1 px-4 rounded-full btn-primary">Search</button>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Link href="/login" className="px-4 py-2 text-sm hover:underline">Login</Link>
          <Link href="/register" className="btn-primary">Get Started</Link>
        </div>
      </div>
    </header>
  );
}
