'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';
import { ProtectedPage } from '../components/ProtectedPage';

export default function LandlordDashboard() {
  const { user, logout } = useAuth();

  const features = [
    {
      icon: '📋',
      name: 'Property Listings',
      description: 'Add and manage your rental properties',
      href: '/landlord/listings'
    },
    {
      icon: '💲',
      name: 'Pricing & Terms',
      description: 'Set rent, deposits, and lease conditions',
      href: '/landlord/pricing'
    },
    {
      icon: '📅',
      name: 'Payment Schedules',
      description: 'Define when rent is due',
      href: '/landlord/schedules'
    },
    {
      icon: '💰',
      name: 'Rent History',
      description: 'Track payment history and status',
      href: '/landlord/history'
    },
    {
      icon: '📊',
      name: 'AI Analytics',
      description: 'Get market insights and recommendations',
      href: '/landlord/analytics'
    },
  ];

  return (
    <ProtectedPage requiredRole="landlord">
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="max-w-6xl mx-auto px-8 py-6 flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-purple-600">Landlord Dashboard</h1>
              <p className="text-gray-600">Welcome, {user?.first_name}!</p>
            </div>
            <button
              onClick={() => logout()}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition"
            >
              Sign Out
            </button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-6xl mx-auto px-8 py-12">
          <h2 className="text-2xl font-bold text-gray-800 mb-8">Management Tools</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, idx) => (
              <Link key={idx} href={feature.href}>
                <div className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer p-6 h-full">
                  <div className="text-4xl mb-3">{feature.icon}</div>
                  <h3 className="text-lg font-bold text-gray-800 mb-2">{feature.name}</h3>
                  <p className="text-gray-600 text-sm mb-4">{feature.description}</p>
                  <div className="text-purple-600 font-semibold">Manage →</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </ProtectedPage>
  );
}
