import React, { useState, useEffect } from 'react';
import { tenantEventsAPI } from '../../services/tenantEvents';

export default function Calendar() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);

  const getEventColor = (type: string) => {
    switch(type) {
      case 'payment': return 'bg-gradient-to-r from-[#f7ca18] to-[#5bc0eb]';
      case 'lease': return 'bg-gradient-to-r from-[#5bc0eb] to-[#23272b]';
      case 'maintenance': return 'bg-gradient-to-r from-[#b3c6e7] to-[#e6e2d3]';
      default: return 'bg-[#b3c6e7]';
    }
  };

  useEffect(() => {
    setLoading(true);
    setError(null);
    tenantEventsAPI.getEvents()
      .then(res => {
        setEvents(res.data.events || []);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load events.');
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <div className="max-w-4xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl mb-10 border border-[#e6e2d3]">
        <h2 className="text-3xl font-extrabold text-[#23272b] mb-6 tracking-tight text-center">Calendar (Lease Events, Reminders)</h2>
        <div className="flex justify-center mb-8">
          <label className="mr-2 font-semibold text-[#23272b]">Month:</label>
          <select value={selectedMonth} onChange={e => setSelectedMonth(Number(e.target.value))} className="rounded-lg border border-[#b3c6e7] p-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent">
            <option value={1}>January</option>
            <option value={2}>February</option>
            <option value={3}>March</option>
            <option value={4}>April</option>
            <option value={5}>May</option>
            <option value={6}>June</option>
            <option value={7}>July</option>
            <option value={8}>August</option>
            <option value={9}>September</option>
            <option value={10}>October</option>
            <option value={11}>November</option>
            <option value={12}>December</option>
          </select>
        </div>
        {loading ? (
          <div className="text-center text-[#23272b] py-8">Loading events...</div>
        ) : error ? (
          <div className="text-center text-red-600 py-8">{error}</div>
        ) : (
          <>
            <div className="grid grid-cols-7 gap-2 mb-8">
              {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                <div key={day} className="font-bold text-center py-2 text-[#23272b]">{day}</div>
              ))}
              {Array.from({ length: 31 }).map((_, i) => (
                <div key={i} className="border border-[#e6e2d3] bg-white rounded-xl min-h-[80px] p-2 flex flex-col">
                  <p className="font-bold text-[#23272b] mb-1">{i + 1}</p>
                  {events.filter(e => {
                    const [year, month, day] = e.date.split('-').map(Number);
                    return month === selectedMonth && day === i + 1;
                  }).map(e => (
                    <div key={e.id} className={`${getEventColor(e.type)} text-white text-xs px-2 py-1 mb-1 rounded-lg shadow`}>{e.title}</div>
                  ))}
                </div>
              ))}
            </div>
            <h3 className="text-2xl font-bold text-[#23272b] mb-4 mt-8 text-center">Upcoming Events</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {events.map(e => (
                <div key={e.id} className={`rounded-xl shadow-lg p-4 flex items-center gap-4 border border-[#e6e2d3] ${getEventColor(e.type)}`}>
                  <span className="font-bold text-white px-3 py-1 rounded-lg text-sm uppercase tracking-wide">{e.type}</span>
                  <div className="flex-1">
                    <b className="text-white">{e.title}</b>
                    <div className="text-[#23272b]">{e.date} at {e.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}