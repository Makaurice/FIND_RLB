'use client';

import React, { useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';

export default function Home() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  useEffect(() => {
    // Redirect to login if not authenticated
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center">
        <div className="text-white text-2xl">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'tenant':
        return 'from-blue-500 to-cyan-500';
      case 'landlord':
        return 'from-purple-500 to-pink-500';
      case 'service_provider':
        return 'from-green-500 to-emerald-500';
      default:
        return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] p-0">
      {/* Hero Section */}
      <section className="w-full bg-gradient-to-br from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] py-20 px-4 flex flex-col items-center justify-center text-center shadow-lg">
        <h1 className="text-6xl font-extrabold tracking-tight mb-4 bg-gradient-to-r from-[#f7ca18] via-[#5bc0eb] to-[#b3c6e7] bg-clip-text text-transparent drop-shadow-lg">FIND-RLB</h1>
        <p className="text-2xl text-[#e6e2d3] mb-6 font-medium">AI-Powered Real Estate Autonomous Economy on Hedera</p>
        <div className="flex flex-wrap gap-4 justify-center mb-8">
          <Link href="/tenant/search" className="px-8 py-4 rounded-xl font-bold text-lg bg-gradient-to-r from-[#f7ca18] via-[#5bc0eb] to-[#23272b] text-white shadow-xl hover:from-[#b3c6e7] hover:to-[#5bc0eb] transition border-2 border-[#e6e2d3]">Find a Home</Link>
          <Link href="/landlord/listings" className="px-8 py-4 rounded-xl font-bold text-lg bg-gradient-to-r from-[#23272b] via-[#b3c6e7] to-[#5bc0eb] text-white shadow-xl hover:from-[#f7ca18] hover:to-[#23272b] transition border-2 border-[#b3c6e7]">List Your Property</Link>
        </div>
        <p className="text-[#b3c6e7] text-lg">Transparent. Automated. Intelligent. <span className="font-semibold text-[#f7ca18]">Own your rental journey.</span></p>
      </section>

      {/* Featured Properties Section */}
      <section className="max-w-6xl mx-auto py-16 px-4">
        <h2 className="text-4xl font-bold text-[#23272b] mb-8 text-center tracking-tight">Featured Properties</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Example featured properties - replace with dynamic data */}
          <div className="bg-gradient-to-br from-[#f8fafc] via-[#e6e2d3] to-[#b3c6e7] rounded-2xl shadow-xl p-6 border border-[#e6e2d3] flex flex-col">
            <img src="/images/featured1.jpg" alt="Property 1" className="rounded-xl mb-4 h-48 object-cover" />
            <h3 className="text-2xl font-bold text-[#23272b] mb-2">Oceanview Apartment</h3>
            <p className="text-[#5bc0eb] font-semibold mb-2">$1,800/mo · For Rent</p>
            <p className="text-[#23272b] mb-4">Mombasa, Kenya</p>
            <Link href="/tenant/search" className="mt-auto px-4 py-2 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition text-center">View Details</Link>
          </div>
          <div className="bg-gradient-to-br from-[#f8fafc] via-[#e6e2d3] to-[#b3c6e7] rounded-2xl shadow-xl p-6 border border-[#e6e2d3] flex flex-col">
            <img src="/images/featured2.jpg" alt="Property 2" className="rounded-xl mb-4 h-48 object-cover" />
            <h3 className="text-2xl font-bold text-[#23272b] mb-2">Luxury Villa</h3>
            <p className="text-[#f7ca18] font-semibold mb-2">$250,000 · For Sale</p>
            <p className="text-[#23272b] mb-4">Karen, Nairobi</p>
            <Link href="/tenant/search" className="mt-auto px-4 py-2 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition text-center">View Details</Link>
          </div>
          <div className="bg-gradient-to-br from-[#f8fafc] via-[#e6e2d3] to-[#b3c6e7] rounded-2xl shadow-xl p-6 border border-[#e6e2d3] flex flex-col">
            <img src="/images/featured3.jpg" alt="Property 3" className="rounded-xl mb-4 h-48 object-cover" />
            <h3 className="text-2xl font-bold text-[#23272b] mb-2">Modern Studio</h3>
            <p className="text-[#5bc0eb] font-semibold mb-2">$900/mo · For Rent</p>
            <p className="text-[#23272b] mb-4">Westlands, Nairobi</p>
            <Link href="/tenant/search" className="mt-auto px-4 py-2 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition text-center">View Details</Link>
          </div>
        </div>
      </section>

      {/* Header (moved below hero for visual hierarchy) */}
      <div className="max-w-6xl mx-auto mb-12 mt-8">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-[#23272b] mb-2">Welcome, {user?.username}</h1>
            <p className="text-lg text-[#6c7a89]">Your dashboard</p>
          </div>
          <div className="text-right">
            <div className="mb-4">
              <p className="text-[#6c7a89] text-sm">Logged in as</p>
              <p className="text-white font-semibold">{user?.first_name} {user?.last_name}</p>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold text-white bg-gradient-to-r ${getRoleColor(user?.role || '')} mt-2`}>
                {user?.role.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-semibold transition"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Tenant App Card */}
          <Link href="/tenant">
            <div className="bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg shadow-xl p-8 cursor-pointer hover:shadow-2xl hover:scale-105 transition duration-300 text-white h-full">
              <div className="mb-4 text-5xl">👤</div>
              <h2 className="text-3xl font-bold mb-2">Tenant App</h2>
              <p className="text-blue-100 mb-6">Discover properties, manage payments, and track your savings journey.</p>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold bg-white bg-opacity-20 px-3 py-1 rounded">8 Features</span>
                <span className="text-2xl">→</span>
              </div>
            </div>
          </Link>

          {/* Landlord Dashboard Card */}
          <Link href="/landlord">
            <div className="bg-gradient-to-br from-purple-600 to-pink-500 rounded-lg shadow-xl p-8 cursor-pointer hover:shadow-2xl hover:scale-105 transition duration-300 text-white h-full">
              <div className="mb-4 text-5xl">🏢</div>
              <h2 className="text-3xl font-bold mb-2">Landlord Dashboard</h2>
              <p className="text-purple-100 mb-6">Manage properties, pricing, schedules, and analytics with AI insights.</p>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold bg-white bg-opacity-20 px-3 py-1 rounded">5 Features</span>
                <span className="text-2xl">→</span>
              </div>
            </div>
          </Link>

          {/* Service Provider Portal Card */}
          <Link href="/service">
            <div className="bg-gradient-to-br from-green-600 to-emerald-500 rounded-lg shadow-xl p-8 cursor-pointer hover:shadow-2xl hover:scale-105 transition duration-300 text-white h-full">
              <div className="mb-4 text-5xl">🔧</div>
              <h2 className="text-3xl font-bold mb-2">Service Portal</h2>
              <p className="text-green-100 mb-6">Browse services, manage bookings, maintenance, and storage inventory.</p>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold bg-white bg-opacity-20 px-3 py-1 rounded">3 Services</span>
                <span className="text-2xl">→</span>
              </div>
            </div>
          </Link>
        </div>

        {/* Features Section */}
        <div className="mt-16">
          <h3 className="text-3xl font-bold text-white mb-8">Platform Highlights</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-slate-700 rounded-lg p-6 border border-slate-600">
              <div className="text-3xl mb-2">🤖</div>
              <h4 className="font-bold text-white mb-2">AI Agents</h4>
              <p className="text-gray-400 text-sm">Smart recommendations powered by machine learning</p>
            </div>
            <div className="bg-slate-700 rounded-lg p-6 border border-slate-600">
              <div className="text-3xl mb-2">⛓️</div>
              <h4 className="font-bold text-white mb-2">On-Chain</h4>
              <p className="text-gray-400 text-sm">Secure Hedera blockchain transactions</p>
            </div>
            <div className="bg-slate-700 rounded-lg p-6 border border-slate-600">
              <div className="text-3xl mb-2">💰</div>
              <h4 className="font-bold text-white mb-2">FIND Token</h4>
              <p className="text-gray-400 text-sm">Native cryptocurrency for platform rewards</p>
            </div>
            <div className="bg-slate-700 rounded-lg p-6 border border-slate-600">
              <div className="text-3xl mb-2">📊</div>
              <h4 className="font-bold text-white mb-2">Analytics</h4>
              <p className="text-gray-400 text-sm">Real-time market insights and trends</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
