import React from 'react';

export default function TenantDashboard() {
  // Simulated stats and insights
  const stats = [
    { label: 'Active Leases', value: 2 },
    { label: 'Total Paid', value: '$2,400' },
    { label: 'Upcoming Payment', value: '$1,200' },
    { label: 'Next Due Date', value: '2026-03-01' },
  ];
  const recommendations = [
    'Pay rent on time to boost your reputation',
    'Consider renewing your lease early for discounts',
    'Check out new property listings in your area',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <div className="max-w-4xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl border border-[#e6e2d3]">
        <h2 className="text-3xl font-extrabold text-[#23272b] mb-8 tracking-tight text-center">Tenant Dashboard</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
          {stats.map((stat, i) => (
            <div key={i} className="rounded-xl shadow p-6 bg-white border border-[#e6e2d3] flex flex-col items-center">
              <div className="text-2xl font-bold text-[#23272b] mb-2">{stat.value}</div>
              <div className="text-[#6c7a89] text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
        <div className="mt-10">
          <h3 className="text-2xl font-bold text-[#23272b] mb-4">Recommendations</h3>
          <ul className="list-disc pl-6 text-[#23272b]">
            {recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
