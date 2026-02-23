import React, { useState } from 'react';

export default function Pricing() {
  const [pricing, setPricing] = useState({
    monthlyRent: 1200,
    securityDeposit: 2400,
    leaseTermMonths: 12,
    lateFeesPercentage: 5,
  });

  const handleChange = (field: string, value: any) => {
    setPricing({ ...pricing, [field]: value });
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Set Pricing & Lease Terms</h2>
      <div style={{ maxWidth: 500, backgroundColor: '#f9f9f9', padding: 20, borderRadius: 8 }}>
        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Monthly Rent: ${pricing.monthlyRent}</label>
          <input
            type="range"
            min="500"
            max="5000"
            value={pricing.monthlyRent}
            onChange={e => handleChange('monthlyRent', Number(e.target.value))}
            style={{ width: '100%' }}
          />
        </div>
        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Security Deposit: ${pricing.securityDeposit}</label>
          <input
            type="number"
            value={pricing.securityDeposit}
            onChange={e => handleChange('securityDeposit', Number(e.target.value))}
            style={{ fontSize: 16, padding: 8, width: '100%' }}
          />
        </div>
        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Lease Term (months): {pricing.leaseTermMonths}</label>
          <input
            type="number"
            value={pricing.leaseTermMonths}
            onChange={e => handleChange('leaseTermMonths', Number(e.target.value))}
            style={{ fontSize: 16, padding: 8, width: '100%' }}
          />
        </div>
        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Late Fees (%): {pricing.lateFeesPercentage}%</label>
          <input
            type="number"
            value={pricing.lateFeesPercentage}
            onChange={e => handleChange('lateFeesPercentage', Number(e.target.value))}
            style={{ fontSize: 16, padding: 8, width: '100%' }}
          />
        </div>
        <button style={{ fontSize: 16, padding: 12, width: '100%', backgroundColor: '#4CAF50', color: 'white', cursor: 'pointer' }}>
          Save Pricing
        </button>
      </div>
    </div>
  );
}