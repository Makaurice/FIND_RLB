import React, { useState } from 'react';
import { aiAgentsAPI } from '../../services/aiAgents';

export default function LandlordAI() {
  const [property, setProperty] = useState({ location: '', price: 0, type: '' });
  const [market_data, setMarketData] = useState({ avg_price: 0, demand: 1 });
  const [history, setHistory] = useState([0.1, 0.2]);
  const [lease, setLease] = useState({ active: true });
  const [tenant, setTenant] = useState('demo_tenant');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const landlord_id = 'demo_landlord';
    setLoading(true);
    try {
      const res = await aiAgentsAPI.landlord(landlord_id, property, market_data, history, lease, tenant);
      setResult(res.data);
    } catch {
      setResult({ error: 'AI agent failed' });
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Landlord AI Agent</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input placeholder="Location" value={property.location} onChange={e => setProperty({ ...property, location: e.target.value })} className="w-full p-2 border rounded" />
        <input placeholder="Price" type="number" value={property.price} onChange={e => setProperty({ ...property, price: Number(e.target.value) })} className="w-full p-2 border rounded" />
        <input placeholder="Type" value={property.type} onChange={e => setProperty({ ...property, type: e.target.value })} className="w-full p-2 border rounded" />
        <input placeholder="Avg Price" type="number" value={market_data.avg_price} onChange={e => setMarketData({ ...market_data, avg_price: Number(e.target.value) })} className="w-full p-2 border rounded" />
        <input placeholder="Demand" type="number" value={market_data.demand} onChange={e => setMarketData({ ...market_data, demand: Number(e.target.value) })} className="w-full p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Get Insights</button>
      </form>
      {result && (
        <div className="mt-6">
          <div>Optimal Rent: {result.optimal_rent}</div>
          <div>Vacancy: {result.vacancy}</div>
          <div>Reminder: {result.reminder}</div>
          <div>Enforcement: {result.enforcement}</div>
        </div>
      )}
    </div>
  );
}
