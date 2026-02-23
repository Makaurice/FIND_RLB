import React, { useState } from 'react';

export default function SavingsWallet() {
  const [savingsPlans, setSavingsPlans] = useState([
    { id: 1, name: 'Dream Apartment', target: 50000, saved: 12500, completion: 25, property: 'Downtown Loft' },
    { id: 2, name: 'Ownership Fund', target: 100000, saved: 35000, completion: 35, property: 'House Purchase' },
  ]);
  const [showDepositForm, setShowDepositForm] = useState(false);
  const [depositAmount, setDepositAmount] = useState(0);

  const handleDeposit = () => {
    if (depositAmount > 0) {
      setSavingsPlans(savingsPlans.map(p => ({
        ...p,
        saved: p.saved + depositAmount,
        completion: Math.round(((p.saved + depositAmount) / p.target) * 100)
      })));
      setDepositAmount(0);
      setShowDepositForm(false);
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Savings Wallet - Save to Own</h2>
      <button onClick={() => setShowDepositForm(!showDepositForm)} style={{ fontSize: 16, padding: 10, marginBottom: 20, backgroundColor: '#007bff', color: 'white' }}>
        {showDepositForm ? 'Cancel' : '+ Add Deposit'}
      </button>
      {showDepositForm && (
        <div style={{ border: '1px solid #ddd', padding: 16, marginBottom: 20, borderRadius: 8 }}>
          <input
            type="number"
            placeholder="Deposit Amount"
            value={depositAmount}
            onChange={e => setDepositAmount(Number(e.target.value))}
            style={{ fontSize: 16, padding: 8, width: '30%', marginRight: 10 }}
          />
          <button onClick={handleDeposit} style={{ fontSize: 16, padding: 8, backgroundColor: '#28a745', color: 'white' }}>Deposit</button>
        </div>
      )}
      {savingsPlans.map(plan => (
        <div key={plan.id} style={{ border: '1px solid #ddd', padding: 16, marginBottom: 16, borderRadius: 8 }}>
          <h3>{plan.name}</h3>
          <p>Target Property: {plan.property}</p>
          <p>Saved: ${plan.saved} / ${plan.target}</p>
          <div style={{ backgroundColor: '#e0e0e0', borderRadius: 4, overflow: 'hidden', height: 20, marginBottom: 12 }}>
            <div style={{ backgroundColor: '#4CAF50', height: '100%', width: `${plan.completion}%` }}></div>
          </div>
          <p style={{ color: '#666' }}>{plan.completion}% Complete</p>
        </div>
      ))}
      <div style={{ marginTop: 24, backgroundColor: '#f0f8ff', padding: 16, borderRadius: 8 }}>
        <h3>Savings Booster</h3>
        <p>Earn up to 5% APY on your saved funds!</p>
        <p>Stake FIND tokens to boost your savings rate.</p>
      </div>
    </div>
  );
}