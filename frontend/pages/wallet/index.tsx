import React, { useState } from 'react';
import { findTokenAPI } from '../../services/findToken';

export default function Wallet() {
  const [address, setAddress] = useState('');
  const [balance, setBalance] = useState<number|null>(null);
  const [to, setTo] = useState('');
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleBalance = async () => {
    setLoading(true);
    setMessage('');
    try {
      const res = await findTokenAPI.getBalance(address);
      setBalance(Number(res.data.balance) / 1e18);
    } catch {
      setMessage('Failed to fetch balance');
    }
    setLoading(false);
  };

  const handleTransfer = async () => {
    setLoading(true);
    setMessage('');
    try {
      await findTokenAPI.transfer(address, to, Number(amount) * 1e18);
      setMessage('Transfer simulated');
    } catch {
      setMessage('Transfer failed');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">FIND Token Wallet</h2>
      <div className="mb-4">
        <input placeholder="Your Address" value={address} onChange={e => setAddress(e.target.value)} className="w-full p-2 border rounded mb-2" />
        <button onClick={handleBalance} className="bg-blue-600 text-white px-4 py-2 rounded mr-2" disabled={loading}>Check Balance</button>
        {balance !== null && <span className="ml-2">Balance: {balance} FIND</span>}
      </div>
      <div className="mb-4">
        <input placeholder="Recipient Address" value={to} onChange={e => setTo(e.target.value)} className="w-full p-2 border rounded mb-2" />
        <input placeholder="Amount" type="number" value={amount} onChange={e => setAmount(e.target.value)} className="w-full p-2 border rounded mb-2" />
        <button onClick={handleTransfer} className="bg-green-600 text-white px-4 py-2 rounded" disabled={loading}>Send FIND</button>
      </div>
      {message && <div className="text-red-600 mt-4">{message}</div>}
    </div>
  );
}
