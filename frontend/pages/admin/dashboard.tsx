import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { ChevronRight, TrendingUp, Users, Building2, Zap, Activity, AlertCircle } from 'lucide-react';

interface AnalyticsData {
  overview: {
    total_users: number;
    total_properties: number;
    total_revenue: number;
    active_transactions: number;
  };
  users: {
    total: number;
    tenants: number;
    landlords: number;
    service_providers: number;
    verified: number;
    user_role_distribution: Array<{ label: string; value: number; color: string }>;
  };
  properties: {
    total: number;
    for_rent: number;
    for_sale: number;
    average_price: number;
    average_beds: number;
  };
  performance_metrics: {
    conversion_rate: string;
    user_engagement: string;
    transaction_success_rate: string;
    platform_uptime: string;
  };
  revenue_trends: Array<{ date: string; users: number; transactions: number; revenue: number }>;
}

interface Activity {
  id: number;
  type: string;
  message: string;
  timestamp: string;
  status: string;
}

interface SystemStatus {
  services: {
    [key: string]: { status: string; response_time?: string; uptime?: string };
  };
  performance: {
    avg_response_time: string;
    cpu_usage: string;
    memory_usage: string;
    database_size: string;
  };
}

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeCarouselIndex, setActiveCarouselIndex] = useState(0);
  const [selectedChart, setSelectedChart] = useState('revenue');

  useEffect(() => {
    fetchAnalytics();
    fetchActivities();
    fetchSystemStatus();

    // Real-time updates every 30 seconds
    const analyticsInterval = setInterval(fetchAnalytics, 30000);
    const activitiesInterval = setInterval(fetchActivities, 30000);
    const statusInterval = setInterval(fetchSystemStatus, 30000);

    return () => {
      clearInterval(analyticsInterval);
      clearInterval(activitiesInterval);
      clearInterval(statusInterval);
    };
  }, []);

  // Auto-rotate carousel every 5 seconds
  useEffect(() => {
    if (activities.length === 0) return;
    const timer = setTimeout(() => {
      setActiveCarouselIndex((prev) => (prev + 1) % Math.ceil(activities.length / 3));
    }, 5000);
    return () => clearTimeout(timer);
  }, [activities, activeCarouselIndex]);

  const fetchAnalytics = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/admin/analytics/');
      if (!res.ok) throw new Error('Failed to fetch analytics');
      const data = await res.json();
      setAnalytics(data);
      setError(null);
    } catch (err) {
      console.error('Analytics error:', err);
      setError('Failed to load analytics data');
    }
  };

  const fetchActivities = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/admin/activities/');
      if (!res.ok) throw new Error('Failed to fetch activities');
      const data = await res.json();
      setActivities(data.activities || []);
      setLoading(false);
    } catch (err) {
      console.error('Activities error:', err);
      setLoading(false);
    }
  };

  const fetchSystemStatus = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/admin/system-status/');
      if (!res.ok) throw new Error('Failed to fetch system status');
      const data = await res.json();
      setSystemStatus(data);
    } catch (err) {
      console.error('System status error:', err);
    }
  };

  const StatCard = ({ icon: Icon, title, value, subtitle, color }: any) => (
    <div className={`bg-gradient-to-br ${color} rounded-xl shadow-lg p-6 text-white hover:shadow-2xl transition-all duration-300 transform hover:scale-105`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium opacity-90">{title}</p>
          <h3 className="text-3xl font-bold mt-2">{value}</h3>
          {subtitle && <p className="text-xs mt-2 opacity-80">{subtitle}</p>}
        </div>
        <div className="bg-white/20 rounded-lg p-3">
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );

  const carouselItems = activities.slice(activeCarouselIndex * 3, (activeCarouselIndex + 1) * 3);

  if (loading && !analytics) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading admin panel...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Navigation Header */}
      <nav className="bg-black/30 backdrop-blur-md border-b border-blue-500/30 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-400 rounded-lg flex items-center justify-center">
                <Zap className="text-white w-6 h-6" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">FIND-RLB Admin</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/" className="text-slate-300 hover:text-white transition cursor-pointer">
                ← Back to Dashboard
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-500/20 border border-red-500/50 rounded-lg p-4 flex items-center space-x-3">
            <AlertCircle className="text-red-400 w-5 h-5" />
            <span className="text-red-200">{error}</span>
          </div>
        )}

        {/* Overview Stats */}
        {analytics && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <StatCard
                icon={Users}
                title="Total Users"
                value={analytics.overview.total_users}
                subtitle={`${analytics.users.verified} verified`}
                color="from-blue-600 to-blue-800"
              />
              <StatCard
                icon={Building2}
                title="Properties"
                value={analytics.overview.total_properties}
                subtitle={`${analytics.properties.for_rent} for rent`}
                color="from-emerald-600 to-emerald-800"
              />
              <StatCard
                icon={TrendingUp}
                title="Total Revenue"
                value={`$${(analytics.overview.total_revenue / 1000).toFixed(0)}K`}
                subtitle="This year"
                color="from-amber-600 to-amber-800"
              />
              <StatCard
                icon={Activity}
                title="Active Transactions"
                value={analytics.overview.active_transactions}
                subtitle="Currently processing"
                color="from-purple-600 to-purple-800"
              />
            </div>

            {/* Charts and Analytics Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              {/* Main Chart */}
              <div className="lg:col-span-2 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-white">Analytics Trends</h2>
                  <select
                    value={selectedChart}
                    onChange={(e) => setSelectedChart(e.target.value)}
                    className="bg-slate-700/50 text-white rounded px-3 py-1 text-sm border border-blue-500/30 focus:outline-none focus:border-blue-500"
                  >
                    <option value="revenue">Revenue</option>
                    <option value="users">Users</option>
                    <option value="transactions">Transactions</option>
                  </select>
                </div>
                <div className="h-64 flex items-end justify-around space-x-2">
                  {analytics.revenue_trends.slice(-15).map((data, idx) => (
                    <div key={idx} className="flex-1 flex flex-col items-center">
                      <div
                        className="w-full bg-gradient-to-t from-blue-500 to-cyan-400 rounded-t transition-all hover:from-blue-400 hover:to-cyan-300 cursor-pointer"
                        style={{ height: `${(data[selectedChart as keyof typeof data] / 100) * 100}%` }}
                      />
                      <span className="text-xs text-slate-400 mt-2 rotate-45 whitespace-nowrap">{data.date}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Performance Metrics */}
              <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6">
                <h2 className="text-xl font-bold text-white mb-4">Performance</h2>
                <div className="space-y-4">
                  {Object.entries(analytics.performance_metrics).map(([key, value]) => (
                    <div key={key}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-slate-300 capitalize">{key.replace(/_/g, ' ')}</span>
                        <span className="text-sm font-bold text-cyan-400">{value}</span>
                      </div>
                      <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-cyan-400"
                          style={{ width: value.includes('%') ? value : '75%' }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* User and Property Distribution */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              {/* User Distribution */}
              <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6">
                <h2 className="text-xl font-bold text-white mb-6">User Distribution</h2>
                <div className="space-y-4">
                  {analytics.users.user_role_distribution.map((role) => (
                    <div key={role.label}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-slate-300">{role.label}</span>
                        <span className="text-sm font-bold text-cyan-400">{role.value}</span>
                      </div>
                      <div className="w-full h-3 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full transition-all"
                          style={{
                            width: `${(role.value / analytics.overview.total_users) * 100}%`,
                            backgroundColor: role.color,
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Property Statistics */}
              <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6">
                <h2 className="text-xl font-bold text-white mb-6">Property Statistics</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-700/50 rounded-lg p-4 border border-blue-500/20">
                    <p className="text-xs text-slate-400 mb-2">For Rent</p>
                    <p className="text-2xl font-bold text-blue-400">{analytics.properties.for_rent}</p>
                  </div>
                  <div className="bg-slate-700/50 rounded-lg p-4 border border-emerald-500/20">
                    <p className="text-xs text-slate-400 mb-2">For Sale</p>
                    <p className="text-2xl font-bold text-emerald-400">{analytics.properties.for_sale}</p>
                  </div>
                  <div className="bg-slate-700/50 rounded-lg p-4 border border-amber-500/20">
                    <p className="text-xs text-slate-400 mb-2">Avg Price</p>
                    <p className="text-2xl font-bold text-amber-400">${(analytics.properties.average_price / 1000).toFixed(0)}K</p>
                  </div>
                  <div className="bg-slate-700/50 rounded-lg p-4 border border-purple-500/20">
                    <p className="text-xs text-slate-400 mb-2">Avg Beds</p>
                    <p className="text-2xl font-bold text-purple-400">{analytics.properties.average_beds.toFixed(1)}</p>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Activities Carousel */}
        {activities.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-6">Recent Activities</h2>
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                {carouselItems.map((activity) => (
                  <div
                    key={activity.id}
                    className={`bg-gradient-to-br ${
                      activity.status === 'success'
                        ? 'from-emerald-900/40 to-emerald-800/40 border-emerald-500/50'
                        : activity.status === 'failed'
                        ? 'from-red-900/40 to-red-800/40 border-red-500/50'
                        : 'from-amber-900/40 to-amber-800/40 border-amber-500/50'
                    } border rounded-lg p-4 hover:shadow-lg transition-all`}
                  >
                    <div className="flex items-start space-x-3">
                      <div
                        className={`w-2 h-2 rounded-full mt-1.5 ${
                          activity.status === 'success'
                            ? 'bg-emerald-400'
                            : activity.status === 'failed'
                            ? 'bg-red-400'
                            : 'bg-amber-400'
                        }`}
                      />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-white truncate">{activity.message}</p>
                        <p className="text-xs text-slate-400 mt-1">
                          {new Date(activity.timestamp).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Carousel Navigation */}
              <div className="flex items-center justify-between pt-4 border-t border-blue-500/30">
                <button
                  onClick={() => setActiveCarouselIndex((prev) => (prev - 1 + Math.ceil(activities.length / 3)) % Math.ceil(activities.length / 3))}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
                >
                  ← Previous
                </button>
                <span className="text-sm text-slate-400">
                  {activeCarouselIndex + 1} / {Math.ceil(activities.length / 3)}
                </span>
                <button
                  onClick={() => setActiveCarouselIndex((prev) => (prev + 1) % Math.ceil(activities.length / 3))}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
                >
                  Next →
                </button>
              </div>
            </div>
          </div>
        )}

        {/* System Status */}
        {systemStatus && (
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6">
            <h2 className="text-xl font-bold text-white mb-6">System Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(systemStatus.services).map(([service, info]) => (
                <div key={service} className="bg-slate-700/50 rounded-lg p-4 border border-blue-500/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-slate-300 capitalize">{service.replace(/_/g, ' ')}</p>
                      <div className="flex items-center space-x-2 mt-2">
                        <div className="w-2 h-2 bg-emerald-400 rounded-full" />
                        <span className="text-xs text-emerald-400">Operational</span>
                      </div>
                    </div>
                    {info.response_time && (
                      <span className="text-xs text-slate-400">{info.response_time}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
