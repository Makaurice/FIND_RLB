import React, { useState } from 'react';

export default function History() {
  const [history] = useState([
    { id: 1, property: '123 Main St', tenant: 'John Doe', amount: 1200, date: '2026-02-01', status: 'Paid' },
    { id: 2, property: '123 Main St', tenant: 'John Doe', amount: 1200, date: '2026-01-01', status: 'Paid' },
    { id: 3, property: '456 Oak Ave', tenant: 'Jane Smith', amount: 1500, date: '2026-02-15', status: 'Pending' },
  ]);

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>See Rent History</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: 12 }}>Property</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Tenant</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Amount</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Date</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {history.map(h => (
            <tr key={h.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 12 }}>{h.property}</td>
              <td style={{ padding: 12 }}>{h.tenant}</td>
              <td style={{ padding: 12 }}>${h.amount}</td>
              <td style={{ padding: 12 }}>{h.date}</td>
              <td style={{ padding: 12, color: h.status === 'Paid' ? '#4CAF50' : '#FF9800', fontWeight: 'bold' }}>
                {h.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}