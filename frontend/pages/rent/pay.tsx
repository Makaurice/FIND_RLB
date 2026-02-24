import React, { useState } from 'react';
import { rentEscrowAPI } from '../../services/rentEscrow';

export default function PayRent() {
  const [leaseId, setLeaseId] = useState('');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    try {
      await rentEscrowAPI.payRent(Number(leaseId), Number(amount));
      setSuccess(true);
    } catch (err) {
      setError('Failed to pay rent');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <div className="max-w-xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl mb-10 text-center border border-[#e6e2d3]">
        <h2 className="text-3xl font-extrabold text-[#23272b] mb-4 tracking-tight">Pay Rent</h2>
        <form onSubmit={handleSubmit} className="space-y-4 mb-6">
          <input placeholder="Lease ID" value={leaseId} onChange={e => setLeaseId(e.target.value)} className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent" />
          <input placeholder="Amount" type="number" value={amount} onChange={e => setAmount(e.target.value)} className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent" />
          <button type="submit" className="w-full px-6 py-3 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition" disabled={loading}>
            {loading ? 'Paying...' : 'Pay Rent'}
          </button>
        </form>
        {error && <div className="text-red-600 mt-4">{error}</div>}
        {success && <div className="text-green-600 mt-4">Rent paid successfully!</div>}
      </div>
    </div>
  );
}
