import React, { useState } from 'react';

export default function Listings() {
  const [properties, setProperties] = useState([
    { id: 1, address: '123 Main St', type: 'Apt', status: 'For Rent', price: 1200 },
    { id: 2, address: '456 Oak Ave', type: 'House', status: 'For Sale', price: 250000 },
  ]);
  const [showForm, setShowForm] = useState(false);
  const [newProp, setNewProp] = useState({ address: '', type: '', status: '' });

  const handleAdd = () => {
    if (newProp.address && newProp.type && newProp.status) {
      setProperties([...properties, { ...newProp, id: Date.now(), price: 0 }]);
      setNewProp({ address: '', type: '', status: '' });
      setShowForm(false);
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>List Properties (Rent/Sale/Lease)</h2>
      <button onClick={() => setShowForm(!showForm)} style={{ fontSize: 16, padding: 10, marginBottom: 20 }}>
        {showForm ? 'Cancel' : '+ Add Property'}
      </button>
      {showForm && (
        <div style={{ border: '1px solid #ccc', padding: 16, marginBottom: 20, borderRadius: 8 }}>
          <input
            type="text"
            placeholder="Address"
            value={newProp.address}
            onChange={e => setNewProp({ ...newProp, address: e.target.value })}
            style={{ fontSize: 14, padding: 8, width: '30%', marginRight: 10 }}
          />
          <select
            value={newProp.type}
            onChange={e => setNewProp({ ...newProp, type: e.target.value })}
            style={{ fontSize: 14, padding: 8, width: '20%', marginRight: 10 }}
          >
            <option value="">Type</option>
            <option value="Apt">Apartment</option>
            <option value="House">House</option>
            <option value="Studio">Studio</option>
          </select>
          <select
            value={newProp.status}
            onChange={e => setNewProp({ ...newProp, status: e.target.value })}
            style={{ fontSize: 14, padding: 8, width: '20%', marginRight: 10 }}
          >
            <option value="">Status</option>
            <option value="For Rent">For Rent</option>
            <option value="For Sale">For Sale</option>
            <option value="Lease">Lease</option>
          </select>
          <button onClick={handleAdd} style={{ fontSize: 14, padding: 8 }}>Add</button>
        </div>
      )}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: 12 }}>Address</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Type</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Status</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Price</th>
          </tr>
        </thead>
        <tbody>
          {properties.map(p => (
            <tr key={p.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 12 }}>{p.address}</td>
              <td style={{ padding: 12 }}>{p.type}</td>
              <td style={{ padding: 12 }}>{p.status}</td>
              <td style={{ padding: 12 }}>${p.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}