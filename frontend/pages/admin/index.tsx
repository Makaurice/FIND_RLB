import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { BarChart3, TrendingUp, Zap, Users, Settings, LogOut, ChevronRight } from 'lucide-react';

interface AdminStats {
  total_users: number;
  total_properties: number;
  active_transactions: number;
}

export default function AdminHome() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/admin/analytics/');
      if (res.ok) {
        const data = await res.json();
        setStats(data.overview);
      }
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Navigation Header */}
      <nav className="bg-black/30 backdrop-blur-md border-b border-blue-500/30 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-400 rounded-lg flex items-center justify-center">
                <Zap className="text-white w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  Admin Panel
                </h1>
                <p className="text-xs text-slate-400">FIND-RLB Management</p>
              </div>
            </div>
            <Link href="/" className="flex items-center space-x-2 text-slate-300 hover:text-white transition cursor-pointer">
              <LogOut className="w-4 h-4" />
              <span>Exit Admin</span>
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Section */}
        <div className="mb-12">
          <h2 className="text-4xl font-bold text-white mb-2">Welcome Back</h2>
          <p className="text-slate-300">Manage your platform and monitor real-time analytics</p>
        </div>

        {/* Quick Stats */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border border-blue-500/50 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-300 text-sm">Total Users</p>
                  <p className="text-3xl font-bold text-blue-400 mt-2">{stats.total_users}</p>
                </div>
                <Users className="w-12 h-12 text-blue-500/30" />
              </div>
            </div>
            <div className="bg-gradient-to-br from-emerald-600/20 to-emerald-800/20 border border-emerald-500/50 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-300 text-sm">Total Properties</p>
                  <p className="text-3xl font-bold text-emerald-400 mt-2">{stats.total_properties}</p>
                </div>
                <Zap className="w-12 h-12 text-emerald-500/30" />
              </div>
            </div>
            <div className="bg-gradient-to-br from-amber-600/20 to-amber-800/20 border border-amber-500/50 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-300 text-sm">Active Transactions</p>
                  <p className="text-3xl font-bold text-amber-400 mt-2">{stats.active_transactions}</p>
                </div>
                <TrendingUp className="w-12 h-12 text-amber-500/30" />
              </div>
            </div>
          </div>
        )}

        {/* Main Navigation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Dashboard Card */}
          <Link href="/admin/dashboard" className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-blue-500/30 rounded-xl p-8 hover:border-blue-500/60 hover:shadow-xl transition-all cursor-pointer group block">
            <div className="flex items-start justify-between mb-4">
              <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-4 rounded-lg group-hover:shadow-lg transition-all">
                <BarChart3 className="w-8 h-8 text-white" />
              </div>
              <ChevronRight className="w-6 h-6 text-slate-500 group-hover:text-blue-400 transition-colors" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Main Dashboard</h3>
            <p className="text-slate-400 mb-4">
              Real-time overview with analytics, charts, and system performance metrics
            </p>
            <div className="flex items-center space-x-2 text-blue-400">
              <span className="text-sm font-medium">Open Dashboard</span>
              <ChevronRight className="w-4 h-4" />
            </div>
          </Link>

          {/* Advanced Analytics Card */}
          <Link href="/admin/analytics" className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 hover:border-purple-500/60 hover:shadow-xl transition-all cursor-pointer group block">
            <div className="flex items-start justify-between mb-4">
              <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-4 rounded-lg group-hover:shadow-lg transition-all">
                <TrendingUp className="w-8 h-8 text-white" />
              </div>
              <ChevronRight className="w-6 h-6 text-slate-500 group-hover:text-purple-400 transition-colors" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Advanced Analytics</h3>
            <p className="text-slate-400 mb-4">
              Detailed insights: user trends, property distribution, blockchain metrics
            </p>
            <div className="flex items-center space-x-2 text-purple-400">
              <span className="text-sm font-medium">View Analytics</span>
              <ChevronRight className="w-4 h-4" />
            </div>
          </Link>

          {/* Settings Card */}
          <Link href="/admin/settings" className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-emerald-500/30 rounded-xl p-8 hover:border-emerald-500/60 hover:shadow-xl transition-all cursor-pointer group block">
            <div className="flex items-start justify-between mb-4">
              <div className="bg-gradient-to-br from-emerald-600 to-emerald-800 p-4 rounded-lg group-hover:shadow-lg transition-all">
                <Settings className="w-8 h-8 text-white" />
              </div>
              <ChevronRight className="w-6 h-6 text-slate-500 group-hover:text-emerald-400 transition-colors" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Admin Settings</h3>
            <p className="text-slate-400 mb-4">
              Manage platform configuration, users, and system preferences
            </p>
            <div className="flex items-center space-x-2 text-emerald-400">
              <span className="text-sm font-medium">Configure</span>
              <ChevronRight className="w-4 h-4" />
            </div>
          </Link>

          {/* Users Management Card */}
          <Link href="/admin/users" className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm border border-pink-500/30 rounded-xl p-8 hover:border-pink-500/60 hover:shadow-xl transition-all cursor-pointer group block">
            <div className="flex items-start justify-between mb-4">
              <div className="bg-gradient-to-br from-pink-600 to-pink-800 p-4 rounded-lg group-hover:shadow-lg transition-all">
                <Users className="w-8 h-8 text-white" />
              </div>
              <ChevronRight className="w-6 h-6 text-slate-500 group-hover:text-pink-400 transition-colors" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Users Management</h3>
            <p className="text-slate-400 mb-4">
              View, manage, and verify platform users and their roles
            </p>
            <div className="flex items-center space-x-2 text-pink-400">
              <span className="text-sm font-medium">Manage Users</span>
              <ChevronRight className="w-4 h-4" />
            </div>
          </Link>
        </div>

        {/* Feature Highlights */}
        <div className="mt-16 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-8">
          <h3 className="text-2xl font-bold text-white mb-6">Admin Panel Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { label: 'Real-time Analytics', desc: 'Live data updates every 30 seconds' },
              { label: 'User Management', desc: 'Complete user role and verification control' },
              { label: 'Property Dashboard', desc: 'Monitor listings and distributions' },
              { label: 'Blockchain Monitor', desc: 'Track smart contracts and tokens' },
              { label: 'System Health', desc: 'Real-time service status and performance' },
              { label: 'Activity Carousel', desc: 'Auto-rotating recent platform activities' },
              { label: 'Revenue Tracking', desc: 'Financial metrics and trends' },
              { label: 'Custom Reports', desc: 'Generate detailed analytics reports' },
            ].map((feature, idx) => (
              <div key={idx} className="bg-slate-700/50 rounded-lg p-4 border border-blue-500/20">
                <p className="font-medium text-white text-sm">{feature.label}</p>
                <p className="text-xs text-slate-400 mt-2">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-12 text-center text-slate-400 text-sm">
          <p>Admin Panel v1.0 • Last Updated: {new Date().toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}
