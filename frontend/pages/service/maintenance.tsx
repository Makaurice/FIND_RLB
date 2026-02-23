import React, { useState } from 'react';

export default function Maintenance() {
  const [requests, setRequests] = useState([
    { id: 1, issue: 'Leaky faucet', priority: 'Medium', status: 'In Progress', date: '2026-02-18', provider: 'Home Fix Pro' },
    { id: 2, issue: 'Broken window latch', priority: 'High', status: 'Scheduled', date: '2026-02-20', provider: 'QuickRepairs' },
    { id: 3, issue: 'Paint touch-up', priority: 'Low', status: 'Completed', date: '2026-02-10', provider: 'Professional Paint' },
  ]);
  const [showRequestForm, setShowRequestForm] = useState(false);
  const [newRequest, setNewRequest] = useState({ issue: '', priority: 'Medium', description: '' });

  const handleSubmitRequest = () => {
    if (newRequest.issue) {
      setRequests([...requests, {
        id: Date.now(),
        issue: newRequest.issue,
        priority: newRequest.priority,
        status: 'Pending',
        date: new Date().toISOString().split('T')[0],
        provider: 'Awaiting Assignment'
      }]);
      setNewRequest({ issue: '', priority: 'Medium', description: '' });
      setShowRequestForm(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch(priority) {
      case 'High': return '#F44336';
      case 'Medium': return '#FF9800';
      case 'Low': return '#4CAF50';
      default: return '#999';
    }
  };

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'Completed': return '#4CAF50';
      case 'In Progress': return '#2196F3';
      case 'Scheduled': return '#FF9800';
      case 'Pending': return '#999';
      default: return '#999';
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Maintenance Providers</h2>
      <div style={{ backgroundColor: '#e8f5e9', padding: 16, marginBottom: 24, borderRadius: 8 }}>
        <h3>Report a Maintenance Issue</h3>
        <p>Submit requests for repairs and maintenance. Our verified providers will respond within 24 hours.</p>
      </div>
      <button onClick={() => setShowRequestForm(!showRequestForm)} style={{ fontSize: 16, padding: 10, marginBottom: 20, backgroundColor: '#007bff', color: 'white' }}>
        {showRequestForm ? 'Cancel' : '+ New Maintenance Request'}
      </button>
      {showRequestForm && (
        <div style={{ border: '1px solid #ddd', padding: 20, marginBottom: 24, borderRadius: 8, backgroundColor: '#f9f9f9' }}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Issue Type:</label>
            <input
              type="text"
              placeholder="e.g., Leaky faucet, Broken window"
              value={newRequest.issue}
              onChange={e => setNewRequest({ ...newRequest, issue: e.target.value })}
              style={{ fontSize: 14, padding: 8, width: '100%' }}
            />
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Priority:</label>
            <select
              value={newRequest.priority}
              onChange={e => setNewRequest({ ...newRequest, priority: e.target.value })}
              style={{ fontSize: 14, padding: 8, width: '100%' }}
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Description:</label>
            <textarea
              placeholder="Describe the issue in detail"
              value={newRequest.description}
              onChange={e => setNewRequest({ ...newRequest, description: e.target.value })}
              style={{ fontSize: 14, padding: 8, width: '100%', minHeight: 80 }}
            />
          </div>
          <button onClick={handleSubmitRequest} style={{ fontSize: 16, padding: 10, backgroundColor: '#28a745', color: 'white' }}>Submit Request</button>
        </div>
      )}
      <h3>Maintenance History</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: 12 }}>Issue</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Priority</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Status</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Provider</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Date</th>
          </tr>
        </thead>
        <tbody>
          {requests.map(r => (
            <tr key={r.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 12 }}>{r.issue}</td>
              <td style={{ padding: 12 }}>
                <span style={{ backgroundColor: getPriorityColor(r.priority), color: 'white', padding: '4 8', borderRadius: 4 }}>
                  {r.priority}
                </span>
              </td>
              <td style={{ padding: 12 }}>
                <span style={{ backgroundColor: getStatusColor(r.status), color: 'white', padding: '4 8', borderRadius: 4 }}>
                  {r.status}
                </span>
              </td>
              <td style={{ padding: 12 }}>{r.provider}</td>
              <td style={{ padding: 12 }}>{r.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}