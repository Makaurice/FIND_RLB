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
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <div className="max-w-2xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl mb-10 text-center border border-[#e6e2d3]">
        <h2 className="text-3xl font-extrabold text-[#23272b] mb-4 tracking-tight">AI Matching Engine</h2>
        <form onSubmit={handleSubmit} className="space-y-4 mb-6">
          <button type="submit" className="px-8 py-3 rounded-xl font-bold text-lg bg-gradient-to-r from-[#5bc0eb] via-[#23272b] to-[#f7ca18] text-white shadow-lg hover:from-[#f7ca18] hover:to-[#5bc0eb] transition border-2 border-[#b3c6e7]" disabled={loading}>
            {loading ? 'Matching...' : 'Match Tenants & Properties'}
          </button>
        </form>
        {result && result.matches && (
          <div className="grid grid-cols-1 gap-6 mt-8">
            {result.matches.map((match: any, idx: number) => (
              <div key={idx} className="bg-gradient-to-br from-[#f8fafc] via-[#e6e2d3] to-[#b3c6e7] border border-[#e6e2d3] rounded-2xl shadow-lg p-6 flex flex-col md:flex-row md:items-center md:justify-between">
                <div className="mb-2 md:mb-0">
                  <div className="text-lg font-bold text-[#23272b]">Tenant: <span className="text-[#5bc0eb]">{match[0]?.id || match.tenant}</span></div>
                  <div className="text-[#6c7a89]">Budget: ${match[0]?.budget || '-'}</div>
                </div>
                <div className="text-2xl font-extrabold text-[#f7ca18] mx-4">→</div>
                <div>
                  <div className="text-lg font-bold text-[#23272b]">Property: <span className="text-[#f7ca18]">{match[1]?.location || match.property}</span></div>
                  <div className="text-[#6c7a89]">Price: ${match[1]?.price || '-'}</div>
                </div>
              </div>
            ))}
          </div>
        )}
        {result && result.error && (
          <div className="text-red-600 mt-4">{result.error}</div>
        )}
      </div>
    </div>
  );
}
