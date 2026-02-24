import React, { useEffect, useState } from 'react';
import { rentalHistoryAPI } from '../../services/rentalHistory';

export default function History() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    rentalHistoryAPI.getHistory()
      .then(res => {
        setHistory(res.data.history || []);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load rental history.');
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <div className="max-w-4xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl border border-[#e6e2d3]">
        <h2 className="text-3xl font-extrabold text-[#23272b] mb-8 tracking-tight text-center">Rent Payment History</h2>
        {loading ? (
          <div className="text-center text-[#23272b] py-8">Loading history...</div>
        ) : error ? (
          <div className="text-center text-red-600 py-8">{error}</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full rounded-xl overflow-hidden">
              <thead>
                <tr className="bg-gradient-to-r from-[#f7ca18] to-[#5bc0eb] text-white">
                  <th className="text-left px-6 py-4">Property</th>
                  <th className="text-left px-6 py-4">Tenant</th>
                  <th className="text-left px-6 py-4">Amount</th>
                  <th className="text-left px-6 py-4">Date</th>
                  <th className="text-left px-6 py-4">Status</th>
                </tr>
              </thead>
              <tbody className="bg-white">
                {history.map(h => (
                  <tr key={h.id} className="border-b border-[#e6e2d3]">
                    <td className="px-6 py-4 text-[#23272b]">{h.property}</td>
                    <td className="px-6 py-4 text-[#23272b]">{h.tenant}</td>
                    <td className="px-6 py-4 text-[#23272b] font-semibold">${h.amount}</td>
                    <td className="px-6 py-4 text-[#23272b]">{h.date}</td>
                    <td className={
                      h.status === 'Paid'
                        ? 'px-6 py-4 font-bold text-[#f7ca18]'
                        : 'px-6 py-4 font-bold text-[#5bc0eb]'
                    }>
                      {h.status}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}