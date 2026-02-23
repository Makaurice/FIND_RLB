import React, { useState } from 'react';

export default function Schedules() {
  const [schedules, setSchedules] = useState([
    { id: 1, property: '123 Main St', dueDay: 1, amount: 1200, frequency: 'Monthly' },
    { id: 2, property: '456 Oak Ave', dueDay: 15, amount: 250000, frequency: 'Annual' },
  ]);
  const [showForm, setShowForm] = useState(false);
  const [newSchedule, setNewSchedule] = useState({ property: '', dueDay: 1, amount: 0, frequency: 'Monthly' });

  const handleAddSchedule = () => {
    if (newSchedule.property && newSchedule.amount) {
      setSchedules([...schedules, { ...newSchedule, id: Date.now() }]);
      setNewSchedule({ property: '', dueDay: 1, amount: 0, frequency: 'Monthly' });
      setShowForm(false);
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Define Payment Schedules</h2>
      <button onClick={() => setShowForm(!showForm)} style={{ fontSize: 16, padding: 10, marginBottom: 20 }}>
        {showForm ? 'Cancel' : '+ Add Schedule'}
      </button>
      {showForm && (
        <div style={{ border: '1px solid #ccc', padding: 16, marginBottom: 20, borderRadius: 8 }}>
          <input
            type="text"
            placeholder="Property"
            value={newSchedule.property}
            onChange={e => setNewSchedule({ ...newSchedule, property: e.target.value })}
            style={{ fontSize: 14, padding: 8, width: '30%', marginRight: 10 }}
          />
          <input
            type="number"
            placeholder="Due Day"
            value={newSchedule.dueDay}
            onChange={e => setNewSchedule({ ...newSchedule, dueDay: Number(e.target.value) })}
            style={{ fontSize: 14, padding: 8, width: '15%', marginRight: 10 }}
          />
          <input
            type="number"
            placeholder="Amount"
            value={newSchedule.amount}
            onChange={e => setNewSchedule({ ...newSchedule, amount: Number(e.target.value) })}
            style={{ fontSize: 14, padding: 8, width: '15%', marginRight: 10 }}
          />
          <select
            value={newSchedule.frequency}
            onChange={e => setNewSchedule({ ...newSchedule, frequency: e.target.value })}
            style={{ fontSize: 14, padding: 8, width: '15%', marginRight: 10 }}
          >
            <option value="Monthly">Monthly</option>
            <option value="Quarterly">Quarterly</option>
            <option value="Annual">Annual</option>
          </select>
          <button onClick={handleAddSchedule} style={{ fontSize: 14, padding: 8 }}>Add</button>
        </div>
      )}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: 12 }}>Property</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Due Day</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Amount</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Frequency</th>
          </tr>
        </thead>
        <tbody>
          {schedules.map(s => (
            <tr key={s.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 12 }}>{s.property}</td>
              <td style={{ padding: 12 }}>Day {s.dueDay}</td>
              <td style={{ padding: 12 }}>${s.amount}</td>
              <td style={{ padding: 12 }}>{s.frequency}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}