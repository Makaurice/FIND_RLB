import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { BarChart3, PieChart, LineChart, ArrowLeft, Activity, AlertCircle } from 'lucide-react';

interface UserMetrics {
  new_users_this_week: number;
  new_verified_users_week: number;
  user_growth_trend: Array<{ date: string; registrations: number }>;
  user_retention_rate: string;
  active_users_today: number;
}

interface PropertyMetrics {
  properties_by_type: Array<{ property_type: string; count: number }>;
  price_distribution: Array<{ range: string; count: number }>;
  bedroom_distribution: Array<{ bedrooms: string; count: number }>;
}

interface BlockchainMetrics {
  blockchain: { network: string; chain_id: number; account_id: string };
  smart_contracts: {
    [key: string]: {
      status: string;
      total_nfts_minted?: number;
      active_agreements?: number;
      total_value_locked?: string;
    };
  };
  token_metrics: {
    find_token: {
      total_supply: string;
      circulating_supply: string;
      token_holders: number;
      market_cap: string;
    };
  };
  transaction_volume_24h: string;
  network_health: string;
}

export default function AdvancedAnalytics() {
  const [userMetrics, setUserMetrics] = useState<UserMetrics | null>(null);
  const [propertyMetrics, setPropertyMetrics] = useState<PropertyMetrics | null>(null);
  const [blockchainMetrics, setBlockchainMetrics] = useState<BlockchainMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState('users');

  useEffect(() => {
    fetchAllMetrics();
    
    // Real-time updates every 60 seconds
    const interval = setInterval(fetchAllMetrics, 60000);
    return () => clearInterval(interval);
  }, []);

  const fetchAllMetrics = async () => {
    try {
      setError(null);
      const [users, properties, blockchain] = await Promise.all([
        fetch('http://localhost:8000/api/admin/users/').then(r => r.json()),
        fetch('http://localhost:8000/api/admin/properties/').then(r => r.json()),
        fetch('http://localhost:8000/api/admin/blockchain/').then(r => r.json()),
      ]);
      
      setUserMetrics(users);
      setPropertyMetrics(properties);
      setBlockchainMetrics(blockchain);
      setLoading(false);
    } catch (err) {
      console.error('Metrics error:', err);
      setError('Failed to load metrics');
      setLoading(false);
    }
  };

  const AnalyticsCard = ({ title, children }: any) => (
    <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6">
      <h3 className="text-lg font-bold text-white mb-4">{title}</h3>
      {children}
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading analytics...</p>
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
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Advanced Analytics</h1>
            <Link href="/admin/dashboard" className="flex items-center space-x-2 text-slate-300 hover:text-white transition cursor-pointer">
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Dashboard</span>
            </Link>
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

        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-8 overflow-x-auto scrollbar-hide">
          {[
            { id: 'users', label: 'User Analytics', icon: '👥' },
            { id: 'properties', label: 'Property Analytics', icon: '🏢' },
            { id: 'blockchain', label: 'Blockchain Metrics', icon: '⛓️' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id)}
              className={`px-6 py-3 rounded-lg font-medium transition-all whitespace-nowrap ${
                selectedTab === tab.id
                  ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
                  : 'bg-slate-700/50 text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        {/* User Analytics Tab */}
        {selectedTab === 'users' && userMetrics && (
          <div className="space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">New Users This Week</p>
                <p className="text-3xl font-bold mt-2">{userMetrics.new_users_this_week}</p>
              </div>
              <div className="bg-gradient-to-br from-emerald-600 to-emerald-800 rounded-xl p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">New Verified Users</p>
                <p className="text-3xl font-bold mt-2">{userMetrics.new_verified_users_week}</p>
              </div>
              <div className="bg-gradient-to-br from-amber-600 to-amber-800 rounded-xl p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">Active Users Today</p>
                <p className="text-3xl font-bold mt-2">{userMetrics.active_users_today}</p>
              </div>
              <div className="bg-gradient-to-br from-purple-600 to-purple-800 rounded-xl p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">Retention Rate</p>
                <p className="text-3xl font-bold mt-2">{userMetrics.user_retention_rate}</p>
              </div>
            </div>

            {/* User Growth Chart */}
            <AnalyticsCard title="User Registration Trend (7 Days)">
              <div className="h-64 flex items-end justify-around space-x-2">
                {userMetrics.user_growth_trend.map((day, idx) => (
                  <div key={idx} className="flex-1 flex flex-col items-center">
                    <div
                      className="w-full bg-gradient-to-t from-blue-500 to-cyan-400 rounded-t hover:from-blue-400 hover:to-cyan-300 transition-all cursor-pointer"
                      style={{ height: `${Math.max(20, (day.registrations / 20) * 200)}px` }}
                      title={`${day.registrations} registrations`}
                    />
                    <span className="text-xs text-slate-400 mt-2 text-center w-full truncate">
                      {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}
                    </span>
                  </div>
                ))}
              </div>
            </AnalyticsCard>
          </div>
        )}

        {/* Property Analytics Tab */}
        {selectedTab === 'properties' && propertyMetrics && (
          <div className="space-y-6">
            {/* Price Distribution */}
            <AnalyticsCard title="Property Price Distribution">
              <div className="space-y-4">
                {propertyMetrics.price_distribution.map((item) => {
                  const maxCount = Math.max(...propertyMetrics.price_distribution.map(p => p.count));
                  return (
                    <div key={item.range}>
                      <div className="flex justify-between mb-2">
                        <span className="text-sm text-slate-300">{item.range}</span>
                        <span className="text-sm font-bold text-cyan-400">{item.count} properties</span>
                      </div>
                      <div className="w-full h-3 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 transition-all"
                          style={{ width: `${(item.count / maxCount) * 100}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </AnalyticsCard>

            {/* Bedroom Distribution */}
            <AnalyticsCard title="Bedroom Distribution">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {propertyMetrics.bedroom_distribution.map((item) => (
                  <div key={item.bedrooms} className="bg-slate-700/50 rounded-lg p-4 border border-blue-500/20 text-center">
                    <p className="text-2xl font-bold text-cyan-400">{item.count}</p>
                    <p className="text-xs text-slate-400 mt-2">{item.bedrooms}</p>
                  </div>
                ))}
              </div>
            </AnalyticsCard>

            {/* Property Types */}
            <AnalyticsCard title="Properties by Type">
              <div className="space-y-3">
                {propertyMetrics.properties_by_type.slice(0, 10).map((item) => {
                  const maxCount = Math.max(...propertyMetrics.properties_by_type.map(p => p.count));
                  return (
                    <div key={item.property_type}>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm text-slate-300 capitalize">{item.property_type}</span>
                        <span className="text-sm font-bold text-blue-400">{item.count}</span>
                      </div>
                      <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-emerald-500 to-emerald-400"
                          style={{ width: `${(item.count / maxCount) * 100}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </AnalyticsCard>
          </div>
        )}

        {/* Blockchain Metrics Tab */}
        {selectedTab === 'blockchain' && blockchainMetrics && (
          <div className="space-y-6">
            {/* Blockchain Info */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-indigo-600 to-indigo-800 rounded-xl p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">Network</p>
                <p className="text-2xl font-bold mt-2">{blockchainMetrics.blockchain.network}</p>
                <p className="text-xs mt-2 opacity-75">Chain ID: {blockchainMetrics.blockchain.chain_id}</p>
              </div>
              <div className="bg-gradient-to-br from-cyan-600 to-cyan-800 rounded-xl p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">Network Health</p>
                <p className="text-3xl font-bold mt-2">{blockchainMetrics.network_health}</p>
              </div>
              <div className="bg-gradient-to-br from-pink-600 to-pink-800 rounded-xl p-6 text-white shadow-lg">
                <p className="text-sm opacity-90">24h Transaction Volume</p>
                <p className="text-2xl font-bold mt-2">{blockchainMetrics.transaction_volume_24h}</p>
              </div>
            </div>

            {/* Smart Contracts */}
            <AnalyticsCard title="Smart Contracts Deployment">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(blockchainMetrics.smart_contracts).map(([name, contract]) => (
                  <div key={name} className="bg-slate-700/50 rounded-lg p-4 border border-blue-500/20">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-sm font-bold text-white capitalize">{name.replace(/_/g, ' ')}</h4>
                      <span className="px-2 py-1 bg-emerald-500/30 text-emerald-300 rounded text-xs font-medium">
                        {contract.status}
                      </span>
                    </div>
                    <div className="space-y-2">
                      {contract.total_nfts_minted && (
                        <p className="text-xs text-slate-400">NFTs Minted: <span className="text-cyan-400 font-bold">{contract.total_nfts_minted}</span></p>
                      )}
                      {contract.active_agreements && (
                        <p className="text-xs text-slate-400">Active: <span className="text-cyan-400 font-bold">{contract.active_agreements}</span></p>
                      )}
                      {contract.total_value_locked && (
                        <p className="text-xs text-slate-400">TVL: <span className="text-cyan-400 font-bold">{contract.total_value_locked}</span></p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </AnalyticsCard>

            {/* Token Metrics */}
            <AnalyticsCard title="FIND Token Metrics">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-slate-700/50 rounded-lg p-4 border border-blue-500/20">
                  <p className="text-xs text-slate-400 mb-2">Total Supply</p>
                  <p className="text-xl font-bold text-blue-400">{blockchainMetrics.token_metrics.find_token.total_supply}</p>
                </div>
                <div className="bg-slate-700/50 rounded-lg p-4 border border-emerald-500/20">
                  <p className="text-xs text-slate-400 mb-2">Circulating Supply</p>
                  <p className="text-xl font-bold text-emerald-400">{blockchainMetrics.token_metrics.find_token.circulating_supply}</p>
                </div>
                <div className="bg-slate-700/50 rounded-lg p-4 border border-purple-500/20">
                  <p className="text-xs text-slate-400 mb-2">Token Holders</p>
                  <p className="text-xl font-bold text-purple-400">{blockchainMetrics.token_metrics.find_token.token_holders}</p>
                </div>
                <div className="bg-slate-700/50 rounded-lg p-4 border border-amber-500/20">
                  <p className="text-xs text-slate-400 mb-2">Market Cap</p>
                  <p className="text-xl font-bold text-amber-400">{blockchainMetrics.token_metrics.find_token.market_cap}</p>
                </div>
              </div>
            </AnalyticsCard>
          </div>
        )}
      </div>
    </div>
  );
}
