import React, { useState } from 'react';
import { aiAgentsAdvancedAPI } from '../../services/aiAgentsAdvanced';

export default function TopMatches() {
  const [tenants, setTenants] = useState([{ id: 't1', location: 'NYC', budget: 2000, property_type: 'apartment', reputation: 2 }]);
  const [properties, setProperties] = useState([{ id: 'p1', location: 'NYC', price: 1800, type: 'apartment' }]);
  const [n, setN] = useState(3);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await aiAgentsAdvancedAPI.topMatches(tenants, properties, n);
      setResult(res.data);
    } catch {
      setResult({ error: 'AI agent failed' });
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Top Matches Engine</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input placeholder="Number of Matches" type="number" value={n} onChange={e => setN(Number(e.target.value))} className="w-full p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Get Top Matches</button>
      </form>
      {result && (
        <div className="mt-6">
          <div>Top Matches: {JSON.stringify(result.top_matches)}</div>
        </div>
      )}
    </div>
  );
}
