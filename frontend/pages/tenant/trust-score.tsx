import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface TrustBreakdown {
  ratingScore: number;
  referralScore: number;
  paymentScore: number;
  reputationScore: number;
}

interface TrustData {
  userId: string;
  trustScore: number;
  breakdown: TrustBreakdown;
  trustLevel: string;
}

export default function TrustScorePage() {
  const [trustData, setTrustData] = useState<TrustData | null>(null);
  const [targetUser, setTargetUser] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const userId = 'current_user_id'; // Get from auth context

  const fetchTrustScore = async (uid: string) => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/community/trust-score/${uid}/`);
      setTrustData(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load trust score');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrustScore(userId);
  }, []);

  const getTrustColor = (score: number) => {
    if (score >= 90) return 'from-purple-500 to-purple-600';
    if (score >= 75) return 'from-amber-500 to-amber-600';
    if (score >= 60) return 'from-blue-500 to-blue-600';
    if (score >= 45) return 'from-green-500 to-green-600';
    return 'from-slate-500 to-slate-600';
  };

  const getTrustDescription = (level: string) => {
    const descriptions: Record<string, string> = {
      PLATINUM: 'Exceptional community member with proven track record',
      GOLD: 'Highly trusted member with strong reputation',
      SILVER: 'Reliable member with good standing',
      BRONZE: 'Active community member building reputation',
      NEW: 'New member, reputation being established',
    };
    return descriptions[level] || 'Community member';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-black to-slate-900 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-blue-400 mb-2">
            Trust Score
          </h1>
          <p className="text-slate-400">Your reputation in the FIND community</p>
        </div>

        {/* User Lookup */}
        <div className="flex gap-4 mb-8">
          <input
            type="text"
            value={targetUser}
            onChange={(e) => setTargetUser(e.target.value)}
            placeholder="Look up another user's trust score"
            className="flex-1 bg-slate-700 border border-slate-600 rounded px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-amber-400"
          />
          <button
            onClick={() => fetchTrustScore(targetUser || userId)}
            className="px-6 py-2 bg-gradient-to-r from-amber-400 to-amber-600 text-black font-semibold rounded hover:shadow-lg hover:shadow-amber-500/50 transition-all"
          >
            Search
          </button>
        </div>

        {error && (
          <div className="p-4 bg-red-900/20 border border-red-700 text-red-300 rounded mb-8">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12 text-slate-400">
            Loading trust score...
          </div>
        ) : trustData ? (
          <>
            {/* Main Trust Score Card */}
            <div className={`bg-gradient-to-br ${getTrustColor(trustData.trustScore)} rounded-lg p-8 mb-8 text-white shadow-2xl`}>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <p className="text-slate-200 mb-2">Trust Score</p>
                  <div className="text-6xl font-bold mb-2">
                    {trustData.trustScore.toFixed(1)}
                  </div>
                  <p className="text-xl font-semibold text-white/90">
                    {trustData.trustLevel}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-5xl mb-2">
                    {trustData.trustLevel === 'PLATINUM' && '👑'}
                    {trustData.trustLevel === 'GOLD' && '🥇'}
                    {trustData.trustLevel === 'SILVER' && '🥈'}
                    {trustData.trustLevel === 'BRONZE' && '🥉'}
                    {trustData.trustLevel === 'NEW' && '⭐'}
                  </div>
                </div>
              </div>
              <p className="text-white/80">
                {getTrustDescription(trustData.trustLevel)}
              </p>
            </div>

            {/* Trust Breakdown */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              {[
                { label: 'Community Rating', value: trustData.breakdown.ratingScore, icon: '⭐' },
                { label: 'Referral Success', value: trustData.breakdown.referralScore, icon: '🤝' },
                { label: 'Payment History', value: trustData.breakdown.paymentScore, icon: '💰' },
                { label: 'Reputation', value: trustData.breakdown.reputationScore, icon: '🏆' },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-6"
                >
                  <p className="text-3xl mb-2">{item.icon}</p>
                  <p className="text-sm text-slate-400 mb-2">{item.label}</p>
                  <div className="flex-1 h-2 bg-slate-700 rounded mb-2">
                    <div
                      className="h-full bg-gradient-to-r from-amber-400 to-amber-600 rounded"
                      style={{ width: `${item.value}%` }}
                    />
                  </div>
                  <p className="text-lg font-bold text-white">{item.value.toFixed(0)} pt</p>
                </div>
              ))}
            </div>

            {/* Breakdown Details */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-8">
              <h2 className="text-2xl font-bold text-white mb-6">Score Breakdown</h2>

              <div className="space-y-6">
                {[
                  {
                    title: 'Community Rating (40%)',
                    description: 'Based on reviews from other members',
                    score: trustData.breakdown.ratingScore,
                    tips: [
                      'Provide honest reviews of experiences',
                      'Maintain responsive communication',
                      'Pay rent on time consistently',
                    ]
                  },
                  {
                    title: 'Referral Success (20%)',
                    description: 'Based on successful referrals and network growth',
                    score: trustData.breakdown.referralScore,
                    tips: [
                      'Refer engaged members to your network',
                      'Help referred members succeed',
                      'Build a strong referral network',
                    ]
                  },
                  {
                    title: 'Payment History (30%)',
                    description: 'Based on on-time payments and reliability',
                    score: trustData.breakdown.paymentScore,
                    tips: [
                      'Pay rent on time every month',
                      'Maintain escrow deposits',
                      'Early payments boost score',
                    ]
                  },
                  {
                    title: 'Reputation (10%)',
                    description: 'Based on lease compliance and community standing',
                    score: trustData.breakdown.reputationScore,
                    tips: [
                      'Follow lease agreement terms',
                      'Maintain property in good condition',
                      'Resolve disputes fairly',
                    ]
                  },
                ].map((item, idx) => (
                  <div key={idx} className="border-l-4 border-amber-400 pl-4">
                    <h3 className="font-semibold text-white mb-1">{item.title}</h3>
                    <p className="text-sm text-slate-400 mb-3">{item.description}</p>

                    <div className="flex gap-4 items-center mb-3">
                      <div className="flex-1 h-3 bg-slate-700 rounded">
                        <div
                          className="h-full bg-gradient-to-r from-amber-400 to-amber-600 rounded"
                          style={{ width: `${item.score}%` }}
                        />
                      </div>
                      <span className="font-bold text-white w-12 text-right">
                        {item.score.toFixed(0)} pt
                      </span>
                    </div>

                    <div className="text-xs text-slate-400">
                      <p className="font-semibold mb-1">💡 Tips to improve:</p>
                      <ul className="list-disc list-inside space-y-1">
                        {item.tips.map((tip, tipIdx) => (
                          <li key={tipIdx}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Level Info */}
            <div className="mt-8 bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <h3 className="font-semibold text-white mb-4">🎯 Trust Levels</h3>
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4 text-sm">
                {[
                  { level: 'NEW', score: '<45', color: 'text-slate-400' },
                  { level: 'BRONZE', score: '45-60', color: 'text-orange-400' },
                  { level: 'SILVER', score: '60-75', color: 'text-slate-300' },
                  { level: 'GOLD', score: '75-90', color: 'text-amber-400' },
                  { level: 'PLATINUM', score: '90+', color: 'text-purple-400' },
                ].map((level, idx) => (
                  <div key={idx} className="text-center">
                    <p className={`font-bold ${level.color}`}>{level.level}</p>
                    <p className="text-slate-400">{level.score}</p>
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}
