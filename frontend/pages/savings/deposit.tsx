import React, { useState } from 'react';
import { savingsVaultAPI } from '../../services/savingsVault';

export default function DepositSavings() {
  const [planId, setPlanId] = useState('');
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
      await savingsVaultAPI.deposit(Number(planId), Number(amount));
      setSuccess(true);
    } catch (err) {
      setError('Failed to deposit savings');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Deposit to Savings</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input placeholder="Plan ID" value={planId} onChange={e => setPlanId(e.target.value)} className="w-full p-2 border rounded" />
        <input placeholder="Amount" type="number" value={amount} onChange={e => setAmount(e.target.value)} className="w-full p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Deposit</button>
      </form>
      {error && <div className="text-red-600 mt-4">{error}</div>}
      {success && <div className="text-green-600 mt-4">Deposit successful!</div>}
    </div>
  );
}
