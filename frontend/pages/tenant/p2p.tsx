import React, { useState } from 'react';

export default function P2PHelp() {
  const [requests, setRequests] = useState([
    { id: 1, from: 'John Doe', amount: 500, reason: 'Emergency rent assistance', status: 'Pending', date: '2026-02-18' },
    { id: 2, from: 'Jane Smith', amount: 300, reason: 'Short-term help', status: 'Approved', date: '2026-02-10' },
  ]);
  const [showRequestForm, setShowRequestForm] = useState(false);
  const [newRequest, setNewRequest] = useState({ recipient: '', amount: 0, reason: '' });

  const handleSendRequest = () => {
    if (newRequest.recipient && newRequest.amount > 0) {
      setRequests([...requests, { ...newRequest, id: Date.now(), status: 'Pending', date: new Date().toISOString().split('T')[0], from: newRequest.recipient }]);
      setNewRequest({ recipient: '', amount: 0, reason: '' });
      setShowRequestForm(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'Approved': return '#4CAF50';
      case 'Pending': return '#FF9800';
      case 'Rejected': return '#F44336';
      default: return '#999';
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>P2P Help (Father paying son's rent)</h2>
      <div style={{ backgroundColor: '#e3f2fd', padding: 16, borderRadius: 8, marginBottom: 24 }}>
        <h3>How it works</h3>
        <ul>
          <li>Request financial help from family or friends</li>
          <li>They can approve and pay on your behalf</li>
          <li>Fully tracked on-chain for transparency</li>
        </ul>
      </div>
      <button onClick={() => setShowRequestForm(!showRequestForm)} style={{ fontSize: 16, padding: 10, marginBottom: 20, backgroundColor: '#007bff', color: 'white' }}>
        {showRequestForm ? 'Cancel' : '+ Request Help'}
      </button>
      {showRequestForm && (
        <div style={{ border: '1px solid #ddd', padding: 16, marginBottom: 20, borderRadius: 8 }}>
          <input
            type="text"
            placeholder="Recipient's Name"
            value={newRequest.recipient}
            onChange={e => setNewRequest({ ...newRequest, recipient: e.target.value })}
            style={{ fontSize: 14, padding: 8, width: '30%', marginRight: 10, marginBottom: 10 }}
          />
          <input
            type="number"
            placeholder="Amount"
            value={newRequest.amount}
            onChange={e => setNewRequest({ ...newRequest, amount: Number(e.target.value) })}
            style={{ fontSize: 14, padding: 8, width: '20%', marginRight: 10, marginBottom: 10 }}
          />
          <br />
          <textarea
            placeholder="Reason"
            value={newRequest.reason}
            onChange={e => setNewRequest({ ...newRequest, reason: e.target.value })}
            style={{ fontSize: 14, padding: 8, width: '100%', marginBottom: 10, minHeight: 60 }}
          />
          <button onClick={handleSendRequest} style={{ fontSize: 14, padding: 8, backgroundColor: '#28a745', color: 'white' }}>Send Request</button>
        </div>
      )}
      <h3>Your Requests</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: 12 }}>From</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Amount</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Reason</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Status</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Date</th>
          </tr>
        </thead>
        <tbody>
          {requests.map(r => (
            <tr key={r.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 12 }}>{r.from}</td>
              <td style={{ padding: 12 }}>${r.amount}</td>
              <td style={{ padding: 12 }}>{r.reason}</td>
              <td style={{ padding: 12, color: getStatusColor(r.status), fontWeight: 'bold' }}>{r.status}</td>
              <td style={{ padding: 12 }}>{r.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}