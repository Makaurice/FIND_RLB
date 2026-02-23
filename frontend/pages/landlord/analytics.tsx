import React from 'react';

export default function Analytics() {
  const insights = [
    { metric: 'Average Market Rent', value: '$1,350', trend: '↑5%' },
    { metric: 'Occupancy Rate', value: '94%', trend: '↓2%' },
    { metric: 'Price Recommendation', value: '$1,250', trend: 'Optimal' },
    { metric: 'Vacancy Risk', value: 'Low (8%)', trend: 'Stable' },
  ];

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>AI Demand Analytics</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 20, marginBottom: 20 }}>
        {insights.map((insight, i) => (
          <div key={i} style={{ border: '1px solid #ddd', borderRadius: 8, padding: 20, backgroundColor: '#f9f9f9' }}>
            <p style={{ margin: '0 0 12px 0', color: '#666' }}>{insight.metric}</p>
            <h3 style={{ margin: '0 0 8px 0', fontSize: 24 }}>{insight.value}</h3>
            <p style={{ margin: 0, color: insight.trend.includes('↑') ? '#4CAF50' : '#FF9800', fontWeight: 'bold' }}>
              {insight.trend}
            </p>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 30 }}>
        <h3>Recommendations</h3>
        <ul>
          <li>Consider raising rent by 3-5% to match market rates</li>
          <li>Offered amenities are key to retaining tenants</li>
          <li>Market demand is strong; expect quick turnovers</li>
        </ul>
      </div>
    </div>
  );
}