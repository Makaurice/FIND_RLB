import React, { useState } from 'react';
import { thirdPartyPaymentAPI } from '../../services/thirdPartyPayment';

export default function PayOnBehalf() {
  const [tenant, setTenant] = useState('');
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
      await thirdPartyPaymentAPI.payOnBehalf(tenant, Number(leaseId), Number(amount));
      setSuccess(true);
    } catch (err) {
      setError('Failed to pay on behalf');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Pay On Behalf</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input placeholder="Tenant Address" value={tenant} onChange={e => setTenant(e.target.value)} className="w-full p-2 border rounded" />
        <input placeholder="Lease ID" value={leaseId} onChange={e => setLeaseId(e.target.value)} className="w-full p-2 border rounded" />
        <input placeholder="Amount" type="number" value={amount} onChange={e => setAmount(e.target.value)} className="w-full p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Pay</button>
      </form>
      {error && <div className="text-red-600 mt-4">{error}</div>}
      {success && <div className="text-green-600 mt-4">Payment successful!</div>}
    </div>
  );
}
