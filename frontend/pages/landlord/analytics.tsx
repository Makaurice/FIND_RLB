import React, { useEffect, useState } from 'react';
import { Chart, ArcElement, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

Chart.register(ArcElement, CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function Analytics() {
  const [insights, setInsights] = useState([
    { metric: 'Average Market Rent', value: '$1,350', trend: '↑5%' },
    { metric: 'Occupancy Rate', value: '94%', trend: '↓2%' },
    { metric: 'Price Recommendation', value: '$1,250', trend: 'Optimal' },
    { metric: 'Vacancy Risk', value: 'Low (8%)', trend: 'Stable' },
  ]);
  // Simulated chart data
  const barData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      {
        label: 'Avg Rent',
        data: [1200, 1250, 1300, 1350, 1400],
        backgroundColor: 'rgba(247,202,24,0.7)',
        borderColor: '#f7ca18',
        borderWidth: 2,
      },
      {
        label: 'Your Rent',
        data: [1200, 1200, 1200, 1200, 1200],
        backgroundColor: 'rgba(91,192,235,0.7)',
        borderColor: '#5bc0eb',
        borderWidth: 2,
      },
    ],
  };
  const doughnutData = {
    labels: ['Occupied', 'Vacant'],
    datasets: [
      {
        data: [94, 6],
        backgroundColor: ['#23272b', '#b3c6e7'],
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <div className="max-w-5xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl border border-[#e6e2d3]">
        <h2 className="text-3xl font-extrabold text-[#23272b] mb-8 tracking-tight text-center">AI Demand Analytics</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          {insights.map((insight, i) => (
            <div key={i} className="rounded-xl shadow p-6 bg-white border border-[#e6e2d3]">
              <p className="mb-2 text-[#6c7a89]">{insight.metric}</p>
              <h3 className="mb-1 text-2xl font-bold text-[#23272b]">{insight.value}</h3>
              <p className={
                insight.trend.includes('↑')
                  ? 'text-[#4CAF50] font-bold'
                  : insight.trend.includes('↓')
                  ? 'text-[#FF9800] font-bold'
                  : 'text-[#5bc0eb] font-bold'
              }>
                {insight.trend}
              </p>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          <div className="bg-white rounded-xl shadow p-6 border border-[#e6e2d3]">
            <h4 className="font-bold text-[#23272b] mb-4">Market Rent Trend</h4>
            <Bar data={barData} options={{
              responsive: true,
              plugins: { legend: { labels: { color: '#23272b' } } },
              scales: { x: { ticks: { color: '#23272b' } }, y: { ticks: { color: '#23272b' } } },
            }} />
          </div>
          <div className="bg-white rounded-xl shadow p-6 border border-[#e6e2d3] flex flex-col items-center justify-center">
            <h4 className="font-bold text-[#23272b] mb-4">Occupancy Rate</h4>
            <Doughnut data={doughnutData} options={{
              plugins: { legend: { labels: { color: '#23272b' } } },
            }} />
          </div>
        </div>
        <div className="mt-10">
          <h3 className="text-2xl font-bold text-[#23272b] mb-4">Recommendations</h3>
          <ul className="list-disc pl-6 text-[#23272b]">
            <li>Consider raising rent by 3-5% to match market rates</li>
            <li>Offered amenities are key to retaining tenants</li>
            <li>Market demand is strong; expect quick turnovers</li>
          </ul>
        </div>
      </div>
    </div>
  );
}