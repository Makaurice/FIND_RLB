import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface RewardRecord {
  userId: string;
  rewardType: string;
  amount: number;
  claimedAt: string;
  newBalance?: number;
}

interface RewardStats {
  totalDistributed: number;
  totalClaims: number;
  uniqueUsers: number;
  averageRewardPerUser: number;
  rewardBreakdown: Record<string, number>;
}

export default function RewardsPage() {
  const [balance, setBalance] = useState<number>(0);
  const [history, setHistory] = useState<RewardRecord[]>([]);
  const [stats, setStats] = useState<RewardStats | null>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('balance');
  
  const userId = 'current_user_id'; // Get from auth context

  useEffect(() => {
    fetchRewardData();
  }, []);

  const fetchRewardData = async () => {
    setLoading(true);
    try {
      const [balRes, histRes, statsRes, leaderRes] = await Promise.all([
        axios.get(`/api/rewards/balance/${userId}/`),
        axios.get(`/api/rewards/history/${userId}/`),
        axios.get(`/api/rewards/statistics/`),
        axios.get(`/api/rewards/leaderboard/?limit=10`),
      ]);

      setBalance(balRes.data.findBalance);
      setHistory(histRes.data.history);
      setStats(statsRes.data);
      setLeaderboard(leaderRes.data.leaderboard);
    } catch (err) {
      console.error('Failed to load rewards data:', err);
    } finally {
      setLoading(false);
    }
  };

  const claimReward = async (rewardType: string, amount: number) => {
    try {
      const response = await axios.post(`/api/rewards/claim/`, {
        userId,
        rewardType,
        amount,
      });
      
      setBalance(response.data.newBalance);
      fetchRewardData(); // Refresh data
    } catch (err) {
      console.error('Failed to claim reward:', err);
    }
  };

  const renderRewardBreakdown = (breakdown: Record<string, number>) => {
    return Object.entries(breakdown).map(([type, amount]) => (
      <div key={type} className="flex justify-between py-2 border-b border-slate-700">
        <span className="text-slate-300 capitalize">{type.replace(/_/g, ' ')}</span>
        <span className="font-semibold text-amber-400">{amount.toFixed(2)} FIND</span>
      </div>
    ));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-black to-slate-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-blue-400 mb-2">
            FIND Rewards
          </h1>
          <p className="text-slate-400">Earn tokens through community participation and payments</p>
        </div>

        {/* Balance Card */}
        <div className="bg-gradient-to-br from-amber-500 to-amber-600 rounded-lg p-8 mb-8 text-white shadow-2xl">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-amber-100 mb-2">Your FIND Balance</p>
              <div className="text-6xl font-bold mb-2">{balance.toFixed(2)}</div>
              <p className="text-amber-100">Ready to use or withdraw</p>
            </div>
            <div className="text-6xl">💎</div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-slate-700">
          {[
            { id: 'balance', label: '💰 Balance & History', icon: '💰' },
            { id: 'leaderboard', label: '🏆 Top Earners', icon: '🏆' },
            { id: 'stats', label: '📊 Statistics', icon: '📊' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 font-semibold transition-colors ${
                activeTab === tab.id
                  ? 'text-amber-400 border-b-2 border-amber-400'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'balance' && (
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Reward Earning Opportunities</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {[
                {
                  title: '🤝 Referrals',
                  base: '100 FIND',
                  description: 'Per successful invite',
                  additional: '+ 5% of referred friend\'s monthly rent',
                  action: 'referral',
                },
                {
                  title: '⭐ Reviews',
                  base: '10-50 FIND',
                  description: 'Based on rating & quality',
                  additional: 'Higher ratings earn more',
                  action: 'review',
                },
                {
                  title: '✅ Payment Streaks',
                  base: '10-50 FIND',
                  description: 'Milestone bonuses',
                  additional: '12 months = 50 FIND',
                  action: 'payment',
                },
                {
                  title: '👑 Tier Bonuses',
                  base: '5-25 FIND',
                  description: 'Monthly based on tier',
                  additional: 'PLATINUM: 25 FIND/month',
                  action: 'tier',
                },
              ].map((reward, idx) => (
                <div
                  key={idx}
                  className="bg-slate-700/50 border border-slate-600 rounded-lg p-6"
                >
                  <h3 className="text-xl font-bold text-white mb-2">{reward.title}</h3>
                  <div className="text-3xl font-bold text-amber-400 mb-2">{reward.base}</div>
                  <p className="text-slate-300 text-sm mb-2">{reward.description}</p>
                  <p className="text-slate-400 text-xs mb-4">{reward.additional}</p>
                </div>
              ))}
            </div>

            <div className="border-t border-slate-700 pt-8">
              <h3 className="text-xl font-bold text-white mb-6">Recent Activity</h3>
              
              {loading ? (
                <div className="text-center py-8 text-slate-400">Loading history...</div>
              ) : history.length > 0 ? (
                <div className="space-y-3">
                  {history.map((record, idx) => (
                    <div key={idx} className="flex justify-between items-center p-4 bg-slate-800/30 rounded">
                      <div>
                        <p className="font-semibold text-white capitalize">
                          {record.rewardType.replace(/_/g, ' ')}
                        </p>
                        <p className="text-sm text-slate-400">
                          {new Date(record.claimedAt).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-amber-400">
                          +{record.amount.toFixed(2)} FIND
                        </p>
                        {record.newBalance !== undefined && (
                          <p className="text-sm text-slate-400">
                            Balance: {record.newBalance.toFixed(2)}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-slate-400">
                  No rewards claimed yet. Start earning!
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'leaderboard' && (
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Top FIND Earners</h2>
            
            {leaderboard.length > 0 ? (
              <div className="space-y-4">
                {leaderboard.map((entry) => (
                  <div
                    key={entry.rank}
                    className={`flex items-center justify-between p-4 rounded-lg ${
                      entry.rank === 1
                        ? 'bg-amber-500/20 border border-amber-500'
                        : entry.rank === 2
                        ? 'bg-slate-400/10 border border-slate-400'
                        : entry.rank === 3
                        ? 'bg-orange-500/10 border border-orange-500'
                        : 'bg-slate-700/50 border border-slate-600'
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <div className="text-3xl font-bold text-white w-12 text-center">
                        {entry.rank === 1 && '🥇'}
                        {entry.rank === 2 && '🥈'}
                        {entry.rank === 3 && '🥉'}
                        {entry.rank > 3 && `#${entry.rank}`}
                      </div>
                      <div>
                        <p className="font-semibold text-white">{entry.userId}</p>
                        <p className="text-sm text-slate-400">Top earner</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-amber-400">
                        {entry.totalEarnings.toFixed(0)}
                      </p>
                      <p className="text-sm text-slate-400">FIND</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-slate-400">
                No leaderboard data available yet
              </div>
            )}
          </div>
        )}

        {activeTab === 'stats' && stats && (
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Reward Statistics</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              {[
                {
                  label: 'Total Distributed',
                  value: stats.totalDistributed.toFixed(0),
                  unit: 'FIND',
                  icon: '💰',
                },
                {
                  label: 'Total Claims',
                  value: stats.totalClaims,
                  unit: 'claims',
                  icon: '✅',
                },
                {
                  label: 'Active Users',
                  value: stats.uniqueUsers,
                  unit: 'users',
                  icon: '👥',
                },
                {
                  label: 'Average Per User',
                  value: stats.averageRewardPerUser.toFixed(1),
                  unit: 'FIND',
                  icon: '📈',
                },
              ].map((stat, idx) => (
                <div key={idx} className="bg-slate-700/50 border border-slate-600 rounded-lg p-6">
                  <div className="text-3xl mb-2">{stat.icon}</div>
                  <p className="text-slate-400 text-sm mb-2">{stat.label}</p>
                  <p className="text-3xl font-bold text-white mb-1">{stat.value}</p>
                  <p className="text-slate-500 text-xs">{stat.unit}</p>
                </div>
              ))}
            </div>

            <div className="bg-slate-700/30 border border-slate-600 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-4">Distribution Breakdown</h3>
              {renderRewardBreakdown(stats.rewardBreakdown)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
