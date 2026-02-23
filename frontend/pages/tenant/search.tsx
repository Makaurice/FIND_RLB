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
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 p-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-gray-800 mb-2">Property Search</h2>
          <p className="text-gray-600 mb-8">AI-powered property discovery</p>

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
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </form>

          {results.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {results.map((property: any) => (
                <div key={property.propertyId || property.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
                  <h3 className="text-xl font-bold text-gray-800 mb-2">
                    {property.location}
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {property.forRent && <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mr-2">For Rent - ${property.price}/mo</span>}
                    {property.forSale && <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">For Sale - ${property.price}</span>}
                  </p>
                  <button className="w-full mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition">
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