import React, { useState } from 'react';
import { propertyNFTAPI } from '../../services/propertyNFT';

export default function RegisterProperty() {
  const [form, setForm] = useState({
    location: '',
    metadataURI: '',
    forRent: false,
    forSale: false,
    price: 0,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    try {
      await propertyNFTAPI.register(form);
      setSuccess(true);
    } catch (err) {
      setError('Failed to register property');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Register Property</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="location" placeholder="Location" value={form.location} onChange={handleChange} className="w-full p-2 border rounded" />
        <input name="metadataURI" placeholder="Metadata URI" value={form.metadataURI} onChange={handleChange} className="w-full p-2 border rounded" />
        <input name="price" type="number" placeholder="Price" value={form.price} onChange={handleChange} className="w-full p-2 border rounded" />
        <label>
          <input type="checkbox" name="forRent" checked={form.forRent} onChange={e => setForm({ ...form, forRent: e.target.checked })} /> For Rent
        </label>
        <label>
          <input type="checkbox" name="forSale" checked={form.forSale} onChange={e => setForm({ ...form, forSale: e.target.checked })} /> For Sale
        </label>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Register</button>
      </form>
      {error && <div className="text-red-600 mt-4">{error}</div>}
      {success && <div className="text-green-600 mt-4">Property registered successfully!</div>}
    </div>
  );
}
