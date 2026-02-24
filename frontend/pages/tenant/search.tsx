'use client';

import React, { useState, useEffect } from 'react';
import { propertiesAPI } from '../../services/api';
import { ProtectedPage } from '../../components/ProtectedPage';

export default function PropertySearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Load properties on mount
  useEffect(() => {
    loadProperties();
  }, []);

  const loadProperties = async () => {
    setLoading(true);
    setError('');
    const response = await propertiesAPI.getAll();
    if (response.success && response.data) {
      setResults(response.data);
    } else {
      setError(response.error || 'Failed to load properties');
    }
    setLoading(false);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    // Fetch properties and filter based on query
    const response = await propertiesAPI.getAll();
    if (response.success && response.data) {
      const filtered = response.data.filter((p: any) =>
        (p.location && p.location.toLowerCase().includes(query.toLowerCase())) ||
        (p.title && p.title.toLowerCase().includes(query.toLowerCase()))
      );
      setResults(filtered);
    } else {
      setError(response.error || 'Search failed');
    }
    setLoading(false);
  };

  return (
    <ProtectedPage requiredRole="tenant">

      <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] p-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-extrabold text-[#23272b] mb-2 tracking-tight" style={{color:'#23272b'}}>Property Search</h2>
          <p className="text-lg text-[#6c7a89] mb-8">AI-powered property discovery</p>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          <form onSubmit={handleSearch} className="mb-8">
            <div className="flex gap-4">
              <input
                type="text"
                placeholder="Search by location, price, type..."
                value={query}
                onChange={e => setQuery(e.target.value)}
                className="flex-1 px-4 py-3 border border-[#b3c6e7] bg-[#f8fafc] text-[#23272b] rounded-lg focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent shadow-sm"
              />
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-gradient-to-r from-[#e6e2d3] via-[#5bc0eb] to-[#23272b] text-white font-semibold rounded-lg shadow-lg hover:from-[#f7ca18] hover:to-[#5bc0eb] transition disabled:opacity-50 border border-[#b3c6e7]"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </form>

          {results.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {results.map((property: any) => (
                <div key={property.propertyId || property.id} className="bg-gradient-to-br from-[#f8fafc] via-[#e6e2d3] to-[#b3c6e7] rounded-2xl shadow-xl p-6 hover:shadow-2xl transition border border-[#e6e2d3]">
                  <h3 className="text-2xl font-bold text-[#23272b] mb-2">
                    {property.location}
                  </h3>
                  <p className="text-[#5bc0eb] mb-4 font-semibold">
                    {property.forRent && <span className="inline-block bg-[#e6e2d3] text-[#23272b] px-3 py-1 rounded-full text-sm mr-2 border border-[#b3c6e7]">For Rent - ${property.price}/mo</span>}
                    {property.forSale && <span className="inline-block bg-[#b3c6e7] text-[#23272b] px-3 py-1 rounded-full text-sm border border-[#e6e2d3]">For Sale - ${property.price}</span>}
                  </p>
                  <button className="w-full mt-4 px-4 py-2 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition">
                    View Details
                  </button>
                </div>
              ))}
            </div>
          )}

          {!loading && results.length === 0 && !error && (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No properties found. Try a different search.</p>
            </div>
          )}
        </div>
      </div>
    </ProtectedPage>
  );
}