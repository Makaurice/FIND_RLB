import React, { useState } from 'react';
import { aiAgentsAPI } from '../../services/aiAgents';

export default function MatchingEngine() {
  const [tenants, setTenants] = useState([{ id: 't1', location: 'NYC', budget: 2000, property_type: 'apartment', reputation: 2 }]);
  const [properties, setProperties] = useState([{ id: 'p1', location: 'NYC', price: 1800, type: 'apartment' }]);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await aiAgentsAPI.match(tenants, properties);
      setResult(res.data);
    } catch {
      setResult({ error: 'AI agent failed' });
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Matching Engine Agent</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Match Tenants & Properties</button>
      </form>
      {result && (
        <div className="mt-6">
          <div>Matches: {JSON.stringify(result.matches)}</div>
        </div>
      )}
    </div>
  );
}
