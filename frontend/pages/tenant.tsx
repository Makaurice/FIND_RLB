'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';
import { ProtectedPage } from '../components/ProtectedPage';

export default function TenantHome() {
  const { user, logout } = useAuth();

  const features = [
    {
      icon: '�',
      name: 'Dashboard',
      description: 'View your stats, payments, and recommendations',
      href: '/tenant/dashboard'
    },
    {
      icon: '�🔍',
      name: 'Property Search',
      description: 'Discover properties using AI recommendations',
      href: '/tenant/search'
    },
    {
      icon: '💳',
      name: 'Rent Payments',
      description: 'Manage rent payments with multiple methods',
      href: '/tenant/payments'
    },
    {
      icon: '📅',
      name: 'Calendar',
      description: 'Track lease events and payment reminders',
      href: '/tenant/calendar'
    },
    {
      icon: '💰',
      name: 'Savings Wallet',
      description: 'Track your save-to-own progress',
      href: '/tenant/savings'
    },
    {
      icon: '🤝',
      name: 'P2P Help',
      description: 'Connect with other tenants for assistance',
      href: '/tenant/p2p'
    },
    {
      icon: '⭐',
      name: 'Reviews & Ratings',
      description: 'Share and read tenant reviews',
      href: '/tenant/reviews'
    },
    {
      icon: '💬',
      name: 'Communication',
      description: 'Chat with landlords and service providers',
      href: '/tenant/communication'
    },
  ];

  return (
    <ProtectedPage requiredRole="tenant">
      <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b]">
        {/* Header */}
        <div className="bg-gradient-to-r from-[#f7ca18] to-[#5bc0eb] shadow-xl">
          <div className="max-w-6xl mx-auto px-8 py-6 flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-[#23272b]">Tenant App</h1>
              <p className="text-[#23272b]">Welcome, {user?.first_name}!</p>
            </div>
            <button
              onClick={() => logout()}
              className="px-4 py-2 bg-[#23272b] hover:bg-[#1a1d21] text-white rounded-lg transition"
            >
              Sign Out
            </button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-6xl mx-auto px-8 py-12">
          <h2 className="text-2xl font-bold text-white mb-8">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, idx) => (
              <Link key={idx} href={feature.href}>
                <div className="bg-gradient-to-br from-white to-[#f8fafc] rounded-xl shadow-lg hover:shadow-xl transition cursor-pointer p-6 h-full border border-[#e6e2d3]">
                  <div className="text-4xl mb-3">{feature.icon}</div>
                  <h3 className="text-lg font-bold text-[#23272b] mb-2">{feature.name}</h3>
                  <p className="text-[#6c7a89] text-sm mb-4">{feature.description}</p>
                  <div className="text-[#5bc0eb] font-semibold">View →</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </ProtectedPage>
  );
}
