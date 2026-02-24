import React, { useState, useEffect } from 'react';
import { propertiesAPI } from '../../services/api';

export default function Listings() {
  const [properties, setProperties] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [newProp, setNewProp] = useState({ location: '', type: '', forRent: true, forSale: false, price: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProperties();
  }, []);

  const loadProperties = async () => {
    setLoading(true);
    setError('');
    const response = await propertiesAPI.getAll();
    if (response.success && response.data) {
      setProperties(response.data);
    } else {
      setError(response.error || 'Failed to load properties');
    }
    setLoading(false);
  };

  const handleAdd = async () => {
    if (newProp.location && newProp.type && newProp.price) {
      setLoading(true);
      setError('');
      const payload = {
        location: newProp.location,
        metadataURI: '',
        forRent: newProp.forRent,
        forSale: newProp.forSale,
        price: parseInt(newProp.price),
        owner: 'me',
        propertyId: undefined,
      };
      const response = await propertiesAPI.create(payload);
      if (response.success) {
        setShowForm(false);
        setNewProp({ location: '', type: '', forRent: true, forSale: false, price: '' });
        loadProperties();
      } else {
        setError(response.error || 'Failed to add property');
      }
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <h2 className="text-4xl font-extrabold text-[#23272b] mb-6 text-center tracking-tight">List Properties (Rent/Sale/Lease)</h2>
      <div className="flex justify-center mb-8">
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-8 py-3 rounded-xl font-bold text-lg bg-gradient-to-r from-[#5bc0eb] via-[#23272b] to-[#f7ca18] text-white shadow-lg hover:from-[#f7ca18] hover:to-[#5bc0eb] transition border-2 border-[#b3c6e7]"
        >
          {showForm ? 'Cancel' : '+ Add Property'}
        </button>
      </div>
      {showForm && (
        <div className="max-w-xl mx-auto bg-white border border-[#b3c6e7] rounded-2xl shadow-lg p-8 mb-10">
          <h3 className="text-xl font-bold text-[#23272b] mb-4">Add New Property</h3>
          <div className="mb-4">
            <input
              type="text"
              placeholder="Location"
              value={newProp.location}
              onChange={e => setNewProp({ ...newProp, location: e.target.value })}
              className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent"
            />
            <select
              value={newProp.type}
              onChange={e => setNewProp({ ...newProp, type: e.target.value })}
              className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent"
            >
              <option value="">Type</option>
              <option value="Apartment">Apartment</option>
              <option value="House">House</option>
              <option value="Studio">Studio</option>
            </select>
            <div className="flex gap-4 mb-2">
              <label className="flex items-center gap-2">
                <input type="checkbox" checked={newProp.forRent} onChange={e => setNewProp({ ...newProp, forRent: e.target.checked })} /> For Rent
              </label>
              <label className="flex items-center gap-2">
                <input type="checkbox" checked={newProp.forSale} onChange={e => setNewProp({ ...newProp, forSale: e.target.checked })} /> For Sale
              </label>
            </div>
            <input
              type="number"
              placeholder="Price"
              value={newProp.price}
              onChange={e => setNewProp({ ...newProp, price: e.target.value })}
              className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent"
            />
          </div>
          <button
            onClick={handleAdd}
            disabled={loading}
            className="w-full px-6 py-3 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition"
          >
            {loading ? 'Adding...' : 'Add Property'}
          </button>
          {error && <p className="text-red-600 mt-2">{error}</p>}
        </div>
      )}
      <div className="max-w-4xl mx-auto">
        <table className="w-full border-collapse bg-white rounded-2xl shadow-xl overflow-hidden">
          <thead>
            <tr className="bg-gradient-to-r from-[#b3c6e7] to-[#e6e2d3] text-[#23272b]">
              <th className="text-left p-4">Location</th>
              <th className="text-left p-4">Type</th>
              <th className="text-left p-4">For Rent</th>
              <th className="text-left p-4">For Sale</th>
              <th className="text-left p-4">Price</th>
            </tr>
          </thead>
          <tbody>
            {properties.map((p: any) => (
              <tr key={p.propertyId || p.id} className="border-b border-[#e6e2d3]">
                <td className="p-4">{p.location}</td>
                <td className="p-4">{p.type || '-'}</td>
                <td className="p-4">{p.forRent ? 'Yes' : 'No'}</td>
                <td className="p-4">{p.forSale ? 'Yes' : 'No'}</td>
                <td className="p-4">${p.price}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {!loading && properties.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No properties listed yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}