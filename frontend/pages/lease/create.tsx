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
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <div className="max-w-xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl mb-10 text-center border border-[#e6e2d3]">
        <h2 className="text-3xl font-extrabold text-[#23272b] mb-4 tracking-tight">Create Lease</h2>
        <form onSubmit={handleSubmit} className="space-y-4 mb-6">
          <input name="propertyId" placeholder="Property ID" value={form.propertyId} onChange={handleChange} className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent" />
          <input name="tenant" placeholder="Tenant Address" value={form.tenant} onChange={handleChange} className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent" />
          <input name="monthlyRent" type="number" placeholder="Monthly Rent" value={form.monthlyRent} onChange={handleChange} className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent" />
          <input name="startDate" type="date" placeholder="Start Date" value={form.startDate} onChange={handleChange} className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent" />
          <input name="endDate" type="date" placeholder="End Date" value={form.endDate} onChange={handleChange} className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-2 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent" />
          <button type="submit" className="w-full px-6 py-3 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition" disabled={loading}>
            {loading ? 'Creating...' : 'Create Lease'}
          </button>
        </form>
        {error && <div className="text-red-600 mt-4">{error}</div>}
        {success && <div className="text-green-600 mt-4">Lease created successfully!</div>}
      </div>
    </div>
  );
}
