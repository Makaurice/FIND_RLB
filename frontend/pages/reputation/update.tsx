import React, { useState } from 'react';
import { reputationAPI } from '../../services/reputation';

export default function UpdateReputation() {
  const [user, setUser] = useState('');
  const [action, setAction] = useState('payment');
  const [score, setScore] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    try {
      if (action === 'payment') await reputationAPI.updatePaymentConsistency(user, Number(score));
      if (action === 'lease') await reputationAPI.updateLeaseCompletionRate(user, Number(score));
      if (action === 'reviews') await reputationAPI.updateReviewsScore(user, Number(score));
      setSuccess(true);
    } catch (err) {
      setError('Failed to update reputation');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Update Reputation</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input placeholder="User Address" value={user} onChange={e => setUser(e.target.value)} className="w-full p-2 border rounded" />
        <select value={action} onChange={e => setAction(e.target.value)} className="w-full p-2 border rounded">
          <option value="payment">Payment Consistency</option>
          <option value="lease">Lease Completion Rate</option>
          <option value="reviews">Reviews Score</option>
        </select>
        <input placeholder="Score" type="number" value={score} onChange={e => setScore(e.target.value)} className="w-full p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Update</button>
      </form>
      {error && <div className="text-red-600 mt-4">{error}</div>}
      {success && <div className="text-green-600 mt-4">Reputation updated!</div>}
    </div>
  );
}
