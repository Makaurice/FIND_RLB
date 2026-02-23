import React, { useState } from 'react';

export default function RentPayments() {
  const [paymentHistory] = useState([
    { id: 1, property: '123 Main St', amount: 1200, dueDate: '2026-03-01', status: 'Upcoming', method: '' },
    { id: 2, property: '123 Main St', amount: 1200, dueDate: '2026-02-01', status: 'Paid', method: 'Card' },
  ]);
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [showPaymentForm, setShowPaymentForm] = useState(false);

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Rent Payments</h2>
      {paymentHistory[0].status === 'Upcoming' && (
        <div style={{ backgroundColor: '#fff3cd', border: '1px solid #ffc107', borderRadius: 8, padding: 16, marginBottom: 24 }}>
          <h3>Payment Due: ${paymentHistory[0].amount}</h3>
          <p>Due: {paymentHistory[0].dueDate}</p>
          <button onClick={() => setShowPaymentForm(!showPaymentForm)} style={{ fontSize: 16, padding: 10, backgroundColor: '#007bff', color: 'white' }}>
            {showPaymentForm ? 'Cancel' : 'Pay Now'}
          </button>
        </div>
      )}
      {showPaymentForm && (
        <div style={{ border: '1px solid #ddd', padding: 20, marginBottom: 24, borderRadius: 8 }}>
          <h3>Payment Method</h3>
          <div style={{ marginBottom: 16 }}>
            <label><input type="radio" value="card" checked={paymentMethod === 'card'} onChange={e => setPaymentMethod(e.target.value)} /> Credit/Debit Card</label>
            <label style={{ marginLeft: 24 }}><input type="radio" value="bank" checked={paymentMethod === 'bank'} onChange={e => setPaymentMethod(e.target.value)} /> Bank Transfer</label>
            <label style={{ marginLeft: 24 }}><input type="radio" value="crypto" checked={paymentMethod === 'crypto'} onChange={e => setPaymentMethod(e.target.value)} /> Cryptocurrency (FIND)</label>
          </div>
          {paymentMethod === 'card' && (
            <div>
              <input type="text" placeholder="Card Number" style={{ fontSize: 14, padding: 8, width: '30%', marginRight: 10, marginBottom: 10 }} />
              <input type="text" placeholder="MM/YY" style={{ fontSize: 14, padding: 8, width: '10%', marginRight: 10, marginBottom: 10 }} />
              <input type="text" placeholder="CVC" style={{ fontSize: 14, padding: 8, width: '10%', marginBottom: 10 }} />
            </div>
          )}
          <button style={{ fontSize: 16, padding: 10, backgroundColor: '#28a745', color: 'white', width: '100%' }}>Confirm Payment</button>
        </div>
      )}
      <h3 style={{ marginTop: 30 }}>Payment History</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: 12 }}>Property</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Amount</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Date</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {paymentHistory.map(p => (
            <tr key={p.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 12 }}>{p.property}</td>
              <td style={{ padding: 12 }}>${p.amount}</td>
              <td style={{ padding: 12 }}>{p.dueDate}</td>
              <td style={{ padding: 12, color: p.status === 'Paid' ? '#4CAF50' : '#FF9800', fontWeight: 'bold' }}>{p.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}