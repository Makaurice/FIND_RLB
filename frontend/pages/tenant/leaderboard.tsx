import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface LeaderboardEntry {
  rank: number;
  userId: string;
  rating?: number;
  referrals?: number;
  trustScore?: number;
}

interface LeaderboardData {
  category: string;
  leaderboard: LeaderboardEntry[];
}

export default function LeaderboardPage() {
  const [category, setCategory] = useState('top_rated');
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLeaderboard();
  }, [category]);

  const fetchLeaderboard = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/community/leaderboard/', {
        params: { category }
      });
      setLeaderboard(response.data.leaderboard);
      setError('');
    } catch (err) {
      setError('Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryLabel = () => {
    switch (category) {
      case 'top_rated':
        return 'Top Rated Users';
      case 'most_referrals':
        return 'Most Active Referrers';
      case 'most_trusted':
        return 'Most Trusted Community Members';
      default:
        return 'Leaderboard';
    }
  };

  const getValueLabel = () => {
    switch (category) {
      case 'top_rated':
        return 'Rating';
      case 'most_referrals':
        return 'Referrals';
      default:
        return 'Score';
    }
  };

  const getMedalColor = (rank: number) => {
    if (rank === 1) return 'from-amber-300 to-amber-600';
    if (rank === 2) return 'from-slate-300 to-slate-500';
    if (rank === 3) return 'from-orange-600 to-orange-800';
    return '';
  };

  const getMedalEmoji = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return null;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-black to-slate-900 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-blue-400 mb-2">
            Community Leaderboard
          </h1>
          <p className="text-slate-400">See who's building the strongest reputation</p>
        </div>

        {/* Category Selector */}
        <div className="flex gap-4 mb-8 flex-wrap">
          {[
            { id: 'top_rated', label: '⭐ Top Rated' },
            { id: 'most_referrals', label: '🤝 Most Referrals' },
            { id: 'most_trusted', label: '🏆 Most Trusted' },
          ].map((cat) => (
            <button
              key={cat.id}
              onClick={() => setCategory(cat.id)}
              className={`px-6 py-2 rounded font-semibold transition-all ${
                category === cat.id
                  ? 'bg-gradient-to-r from-amber-400 to-amber-600 text-black shadow-lg shadow-amber-500/50'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-600'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Leaderboard */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg overflow-hidden">
          {/* Header */}
          <div className="bg-slate-900 border-b border-slate-700 p-6">
            <h2 className="text-2xl font-bold text-white">{getCategoryLabel()}</h2>
          </div>

          {/* Entries */}
          {loading ? (
            <div className="p-12 text-center text-slate-400">
              Loading leaderboard...
            </div>
          ) : error ? (
            <div className="p-6 bg-red-900/20 border border-red-700 text-red-300 m-4 rounded">
              {error}
            </div>
          ) : leaderboard.length > 0 ? (
            <div className="divide-y divide-slate-700">
              {leaderboard.map((entry) => {
                const medal = getMedalEmoji(entry.rank);
                const medalColor = getMedalColor(entry.rank);
                const value = entry.rating || entry.referrals || entry.trustScore || 0;

                return (
                  <div
                    key={entry.rank}
                    className={`p-6 flex items-center justify-between hover:bg-slate-700/30 transition-colors ${
                      entry.rank <= 3 ? 'bg-slate-800/50' : ''
                    }`}
                  >
                    <div className="flex items-center gap-4 flex-1">
                      {/* Rank */}
                      {medal ? (
                        <div className={`text-4xl font-bold bg-gradient-to-r ${medalColor} bg-clip-text text-transparent w-12 text-center`}>
                          {entry.rank}
                        </div>
                      ) : (
                        <div className="w-12 text-center text-2xl font-bold text-slate-400">
                          {entry.rank}
                        </div>
                      )}

                      {/* Medal */}
                      {medal && (
                        <span className="text-3xl">{medal}</span>
                      )}

                      {/* User Info */}
                      <div className="flex-1">
                        <p className="font-semibold text-white text-lg">
                          {entry.userId}
                        </p>
                      </div>
                    </div>

                    {/* Value */}
                    <div className="text-right">
                      <div className={`text-3xl font-bold ${
                        entry.rank <= 3
                          ? 'bg-gradient-to-r from-amber-400 to-amber-600 bg-clip-text text-transparent'
                          : 'text-blue-400'
                      }`}>
                        {typeof value === 'number' ? value.toFixed(2) : value}
                      </div>
                      <p className="text-sm text-slate-400">
                        {getValueLabel()}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="p-12 text-center text-slate-400">
              No entries in this category yet
            </div>
          )}
        </div>

        {/* Info Box */}
        <div className="mt-8 bg-slate-800/50 border border-slate-700 rounded-lg p-6">
          <h3 className="font-semibold text-white mb-2">📊 How Leaderboards Work</h3>
          <ul className="text-slate-400 text-sm space-y-2">
            <li>
              <span className="font-semibold">⭐ Top Rated:</span> Users ranked by their average review rating from other community members
            </li>
            <li>
              <span className="font-semibold">🤝 Most Referrals:</span> Users who have successfully referred the most new members
            </li>
            <li>
              <span className="font-semibold">🏆 Most Trusted:</span> Overall trust score based on ratings, referrals, and payment reliability
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
