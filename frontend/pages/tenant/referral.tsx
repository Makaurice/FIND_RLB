import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Referral {
  referrerId: string;
  referredUserId: string;
  referralCode: string;
  status: string;
  completionRewardWaiting: number;
  createdAt: string;
}

interface ReferralStats {
  userId: string;
  totalReferrals: number;
  completedReferrals: number;
  pendingReferrals: number;
  totalEarnings: number;
  referrals: Referral[];
}

export default function ReferralPage() {
  const [stats, setStats] = useState<ReferralStats | null>(null);
  const [newReferralCode, setNewReferralCode] = useState('');
  const [referredEmail, setReferredEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const userId = 'current_user_id'; // Get from auth context

  useEffect(() => {
    fetchReferralStats();
  }, []);

  const fetchReferralStats = async () => {
    try {
      const response = await axios.get(`/api/community/referrals/stats/${userId}/`);
      setStats(response.data);
    } catch (err) {
      setError('Failed to load referral stats');
    }
  };

  const generateReferralCode = () => {
    const code = `REF${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
    setNewReferralCode(code);
    setSuccess('Referral code generated! Share it with friends.');
  };

  const submitReferral = async () => {
    if (!referredEmail || !newReferralCode) {
      setError('Please fill all fields');
      return;
    }

    setLoading(true);
    try {
      await axios.post('/api/community/referrals/submit/', {
        referrerId: userId,
        referredUserId: referredEmail,
        referralCode: newReferralCode,
      });
      setSuccess('Referral submitted! Rewards available when they sign up.');
      setReferredEmail('');
      setNewReferralCode('');
      fetchReferralStats();
    } catch (err) {
      setError('Failed to submit referral');
    } finally {
      setLoading(false);
    }
  };

  const claimReward = async (referredUserId: string) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/community/referrals/claim/', {
        referrerId: userId,
        referredUserId: referredUserId,
      });
      setSuccess(`Claimed ${response.data.rewardAmount} FIND tokens!`);
      fetchReferralStats();
    } catch (err) {
      setError('Failed to claim reward');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-black to-slate-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-blue-400 mb-2">
            Referral Network
          </h1>
          <p className="text-slate-400">Earn FIND tokens by inviting friends to FIND</p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[
              { label: 'Total Referrals', value: stats.totalReferrals, color: 'from-amber-400' },
              { label: 'Completed', value: stats.completedReferrals, color: 'from-green-400' },
              { label: 'Pending', value: stats.pendingReferrals, color: 'from-blue-400' },
              { label: 'Total Earned', value: `${stats.totalEarnings} FIND`, color: 'from-purple-400' },
            ].map((stat, idx) => (
              <div
                key={idx}
                className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-6"
              >
                <div className={`text-3xl font-bold bg-gradient-to-r ${stat.color} to-transparent bg-clip-text text-transparent mb-2`}>
                  {stat.value}
                </div>
                <p className="text-slate-400 text-sm">{stat.label}</p>
              </div>
            ))}
          </div>
        )}

        {/* Generate Referral Code */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6">Create Referral</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Referral Code
              </label>
              <div className="flex gap-4">
                <input
                  type="text"
                  value={newReferralCode}
                  placeholder="Your unique referral code"
                  className="flex-1 bg-slate-700 border border-slate-600 rounded px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-amber-400"
                  readOnly
                />
                <button
                  onClick={generateReferralCode}
                  className="px-6 py-2 bg-gradient-to-r from-amber-400 to-amber-600 text-black font-semibold rounded hover:shadow-lg hover:shadow-amber-500/50 transition-all"
                >
                  Generate
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Friend's Email
              </label>
              <input
                type="email"
                value={referredEmail}
                onChange={(e) => setReferredEmail(e.target.value)}
                placeholder="Enter email of friend you want to refer"
                className="w-full bg-slate-700 border border-slate-600 rounded px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-amber-400"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-900/20 border border-red-700 text-red-300 rounded">
                {error}
              </div>
            )}

            {success && (
              <div className="p-3 bg-green-900/20 border border-green-700 text-green-300 rounded">
                {success}
              </div>
            )}

            <button
              onClick={submitReferral}
              disabled={loading}
              className="w-full py-2 bg-gradient-to-r from-blue-500 to-blue-700 text-white font-semibold rounded hover:shadow-lg hover:shadow-blue-500/50 transition-all disabled:opacity-50"
            >
              {loading ? 'Submitting...' : 'Submit Referral'}
            </button>
          </div>
        </div>

        {/* Referral List */}
        {stats && stats.referrals.length > 0 && (
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Your Referrals</h2>
            
            <div className="space-y-4">
              {stats.referrals.map((referral, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between bg-slate-700/50 border border-slate-600 rounded-lg p-4"
                >
                  <div className="flex-1">
                    <p className="font-semibold text-white">{referral.referralCode}</p>
                    <p className="text-sm text-slate-400">{referral.referredUserId}</p>
                    <p className="text-xs text-slate-500 mt-1">
                      {new Date(referral.createdAt).toLocaleDateString()}
                    </p>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <p className={`text-sm font-semibold ${
                        referral.status === 'COMPLETED' ? 'text-green-400' : 'text-amber-400'
                      }`}>
                        {referral.status}
                      </p>
                      {referral.status === 'PENDING' && (
                        <p className="text-xs text-slate-400">
                          +{referral.completionRewardWaiting} FIND pending
                        </p>
                      )}
                    </div>

                    {referral.status === 'PENDING' && (
                      <button
                        onClick={() => claimReward(referral.referredUserId)}
                        className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded transition-colors"
                      >
                        Claim
                      </button>
                    )}

                    {referral.status === 'COMPLETED' && (
                      <span className="px-4 py-2 bg-slate-600 text-slate-300 rounded">
                        Claimed
                      </span>
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
