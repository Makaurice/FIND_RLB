import React, { useState } from 'react';

export default function Calendar() {
  const [events, setEvents] = useState([
    { id: 1, title: 'Rent Payment Due', date: '2026-03-01', type: 'payment', time: '00:00' },
    { id: 2, title: 'Lease Renewal Notice', date: '2026-05-01', type: 'lease', time: '09:00' },
    { id: 3, title: 'Maintenance Scheduled', date: '2026-02-25', type: 'maintenance', time: '14:00' },
  ]);
  const [selectedMonth, setSelectedMonth] = useState(2);

  const getEventColor = (type: string) => {
    switch(type) {
      case 'payment': return '#FF6B6B';
      case 'lease': return '#4ECDC4';
      case 'maintenance': return '#95E1D3';
      default: return '#95A5A6';
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Calendar (Lease Events, Reminders)</h2>
      <div style={{ marginBottom: 24 }}>
        <label>Month: </label>
        <select value={selectedMonth} onChange={e => setSelectedMonth(Number(e.target.value))} style={{ fontSize: 16, padding: 8 }}>
          <option value={1}>January</option>
          <option value={2}>February</option>
          <option value={3}>March</option>
          <option value={4}>April</option>
          <option value={5}>May</option>
        </select>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 10, marginBottom: 24 }}>
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} style={{ fontWeight: 'bold', textAlign: 'center', padding: 8 }}>{day}</div>
        ))}
        {Array.from({ length: 28 }).map((_, i) => (
          <div key={i} style={{ border: '1px solid #ddd', padding: 8, minHeight: 80, borderRadius: 4 }}>
            <p style={{ margin: '0 0 8px 0', fontWeight: 'bold' }}>{i + 1}</p>
            {events.filter(e => e.date.endsWith(`-${String(selectedMonth).padStart(2, '0')}-${String(i + 1).padStart(2, '0')}`)).map(e => (
              <div key={e.id} style={{ backgroundColor: getEventColor(e.type), color: 'white', fontSize: 12, padding: 4, marginBottom: 4, borderRadius: 2 }}>
                {e.title}
              </div>
            ))}
          </div>
        ))}
      </div>
      <h3>Upcoming Events</h3>
      <ul>
        {events.map(e => (
          <li key={e.id} style={{ marginBottom: 12 }}>
            <span style={{ backgroundColor: getEventColor(e.type), color: 'white', padding: '4 8', marginRight: 10, borderRadius: 4 }}>{e.type}</span>
            <b>{e.title}</b> — {e.date} at {e.time}
          </li>
        ))}
      </ul>
    </div>
  );
}