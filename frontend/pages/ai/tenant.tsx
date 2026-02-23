import React, { useState } from 'react';
import { aiAgentsAPI } from '../../services/aiAgents';

export default function TenantAI() {
  const [preferences, setPreferences] = useState({ location: '', budget: 0, property_type: '', history: [] });
  const [properties, setProperties] = useState([]); // Load from backend or mock
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const user_id = 'demo_user';
    try {
      const res = await aiAgentsAPI.tenant(user_id, preferences, properties);
      setResult(res.data);
    } catch {
      setResult({ error: 'AI agent failed' });
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Tenant AI Agent</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input placeholder="Location" value={preferences.location} onChange={e => setPreferences({ ...preferences, location: e.target.value })} className="w-full p-2 border rounded" />
        <input placeholder="Budget" type="number" value={preferences.budget} onChange={e => setPreferences({ ...preferences, budget: Number(e.target.value) })} className="w-full p-2 border rounded" />
        <input placeholder="Property Type" value={preferences.property_type} onChange={e => setPreferences({ ...preferences, property_type: e.target.value })} className="w-full p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Get Recommendations</button>
      </form>
      {result && (
        <div className="mt-6">
          <div>Recommended Home: {JSON.stringify(result.recommended_home)}</div>
          <div>Negotiation: {result.negotiation}</div>
          <div>Savings Plan: {result.savings_plan}</div>
        </div>
      )}
    </div>
  );
}
