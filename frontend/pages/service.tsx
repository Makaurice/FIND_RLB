'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import ProtectedPage from '../components/ProtectedPage';
import { useAuth } from '../hooks/useAuth';

export default function ServiceProviderPortal() {
  const router = useRouter();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const services = [
    {
      title: 'Moving Services',
      description: 'Manage mover partnerships and track delivery bookings',
      icon: '📦',
      href: '/service/movers',
      gradient: 'from-blue-500 to-blue-600',
    },
    {
      title: 'Maintenance Providers',
      description: 'Handle maintenance requests and service schedules',
      icon: '🔧',
      href: '/service/maintenance',
      gradient: 'from-orange-500 to-orange-600',
    },
    {
      title: 'Warehousing & Storage',
      description: 'Manage storage units and inventory',
      icon: '🏠',
      href: '/service/warehousing',
      gradient: 'from-green-500 to-green-600',
    },
  ];

  return (
    <ProtectedPage requiredRole="service_provider">
      <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-12">
            <div>
              <h1 className="text-4xl font-bold text-slate-900 mb-2">Service Provider Portal</h1>
              <p className="text-slate-600">
                Welcome back, <span className="font-semibold text-blue-600">{user?.first_name || 'Service Provider'}</span>
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="px-6 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition"
            >
              Sign Out
            </button>
          </div>

          {/* Services Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-12">
            {services.map((service) => (
              <Link key={service.href} href={service.href}>
                <div className={`bg-gradient-to-br ${service.gradient} p-8 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105 cursor-pointer text-white`}>
                  <div className="text-5xl mb-4">{service.icon}</div>
                  <h3 className="text-2xl font-bold mb-2">{service.title}</h3>
                  <p className="text-blue-100 mb-4">{service.description}</p>
                  <div className="flex items-center text-sm font-semibold">
                    Manage <span className="ml-2">→</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Info Section */}
          <div className="bg-white rounded-xl shadow-md p-8">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">Service Management Hub</h2>
            <p className="text-slate-600 mb-4">
              Manage all your real estate service needs in one place. Track bookings, manage partnerships,
              and grow your service business with FIND-RLB.
            </p>
            <ul className="space-y-3 text-slate-700">
              <li className="flex items-center">
                <span className="text-green-500 font-bold mr-3">✓</span>
                Real-time booking management
              </li>
              <li className="flex items-center">
                <span className="text-green-500 font-bold mr-3">✓</span>
                Partner performance analytics
              </li>
              <li className="flex items-center">
                <span className="text-green-500 font-bold mr-3">✓</span>
                Secure payment processing
              </li>
            </ul>
          </div>
        </div>
      </main>
    </ProtectedPage>
  );
}
