import React, { useState } from 'react';
import { leaseAgreementAPI } from '../../services/leaseAgreement';

export default function CreateLease() {
  const [form, setForm] = useState({
    propertyId: '',
    tenant: '',
    monthlyRent: '',
    startDate: '',
    endDate: '',
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
      await leaseAgreementAPI.create(form);
      setSuccess(true);
    } catch (err) {
      setError('Failed to create lease');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Create Lease</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="propertyId" placeholder="Property ID" value={form.propertyId} onChange={handleChange} className="w-full p-2 border rounded" />
        <input name="tenant" placeholder="Tenant Address" value={form.tenant} onChange={handleChange} className="w-full p-2 border rounded" />
        <input name="monthlyRent" type="number" placeholder="Monthly Rent" value={form.monthlyRent} onChange={handleChange} className="w-full p-2 border rounded" />
        <input name="startDate" type="date" placeholder="Start Date" value={form.startDate} onChange={handleChange} className="w-full p-2 border rounded" />
        <input name="endDate" type="date" placeholder="End Date" value={form.endDate} onChange={handleChange} className="w-full p-2 border rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>Create Lease</button>
      </form>
      {error && <div className="text-red-600 mt-4">{error}</div>}
      {success && <div className="text-green-600 mt-4">Lease created successfully!</div>}
    </div>
  );
}
