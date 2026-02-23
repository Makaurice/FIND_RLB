import React, { useState } from 'react';

export default function Warehousing() {
  const [storageUnits, setStorageUnits] = useState([
    { id: 1, name: 'Downtown Storage Hub', size: '100 sq ft', price: 150, occupancy: 85, climate: 'Yes', security: '24/7' },
    { id: 2, name: 'Suburban Warehouse', size: '200 sq ft', price: 250, occupancy: 60, climate: 'Yes', security: '24/7' },
    { id: 3, name: 'Economy Storage', size: '50 sq ft', price: 75, occupancy: 95, climate: 'No', security: 'Business hours' },
  ]);
  const [inventory, setInventory] = useState([
    { id: 1, item: 'Furniture', quantity: 5, location: 'Downtown Storage Hub', status: 'Stored' },
    { id: 2, item: 'Boxes (Electronics)', quantity: 12, location: 'Suburban Warehouse', status: 'Stored' },
    { id: 3, item: 'Seasonal Items', quantity: 3, location: 'Downtown Storage Hub', status: 'In Transit' },
  ]);
  const [showAddItem, setShowAddItem] = useState(false);
  const [newItem, setNewItem] = useState({ item: '', quantity: 0, location: '' });

  const handleAddItem = () => {
    if (newItem.item && newItem.quantity > 0 && newItem.location) {
      setInventory([...inventory, {
        id: Date.now(),
        item: newItem.item,
        quantity: newItem.quantity,
        location: newItem.location,
        status: 'Stored'
      }]);
      setNewItem({ item: '', quantity: 0, location: '' });
      setShowAddItem(false);
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Warehousing & Storage Agents</h2>
      <div style={{ marginBottom: 24 }}>
        <h3>Available Storage Units</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {storageUnits.map(unit => (
            <div key={unit.id} style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
              <h4>{unit.name}</h4>
              <p><b>Size:</b> {unit.size}</p>
              <p><b>Price:</b> ${unit.price}/month</p>
              <p><b>Occupancy:</b> {unit.occupancy}%</p>
              <div style={{ backgroundColor: '#e0e0e0', borderRadius: 4, height: 8, marginBottom: 8 }}>
                <div style={{ backgroundColor: '#FF9800', height: '100%', width: `${unit.occupancy}%` }}></div>
              </div>
              <p><b>Climate Control:</b> {unit.climate}</p>
              <p><b>Security:</b> {unit.security}</p>
              <button style={{
                width: '100%',
                padding: 10,
                backgroundColor: unit.occupancy === 100 ? '#ccc' : '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: 4,
                cursor: unit.occupancy === 100 ? 'not-allowed' : 'pointer',
                marginTop: 12
              }}
              disabled={unit.occupancy === 100}
              >
                {unit.occupancy === 100 ? 'Full' : 'Rent Unit'}
              </button>
            </div>
          ))}
        </div>
      </div>
      <div style={{ marginBottom: 24 }}>
        <h3>Your Inventory</h3>
        <button onClick={() => setShowAddItem(!showAddItem)} style={{ fontSize: 16, padding: 10, marginBottom: 16, backgroundColor: '#007bff', color: 'white' }}>
          {showAddItem ? 'Cancel' : '+ Add Item'}
        </button>
        {showAddItem && (
          <div style={{ border: '1px solid #ddd', padding: 16, marginBottom: 20, borderRadius: 8, backgroundColor: '#f9f9f9' }}>
            <div style={{ marginBottom: 12 }}>
              <label style={{ display: 'block', marginBottom: 8 }}>Item Description:</label>
              <input
                type="text"
                placeholder="e.g., Furniture, Boxes, Seasonal items"
                value={newItem.item}
                onChange={e => setNewItem({ ...newItem, item: e.target.value })}
                style={{ fontSize: 14, padding: 8, width: '100%' }}
              />
            </div>
            <div style={{ marginBottom: 12 }}>
              <label style={{ display: 'block', marginBottom: 8 }}>Quantity:</label>
              <input
                type="number"
                value={newItem.quantity}
                onChange={e => setNewItem({ ...newItem, quantity: Number(e.target.value) })}
                style={{ fontSize: 14, padding: 8, width: '100%' }}
              />
            </div>
            <div style={{ marginBottom: 12 }}>
              <label style={{ display: 'block', marginBottom: 8 }}>Storage Unit:</label>
              <select
                value={newItem.location}
                onChange={e => setNewItem({ ...newItem, location: e.target.value })}
                style={{ fontSize: 14, padding: 8, width: '100%' }}
              >
                <option value="">Select a unit</option>
                {storageUnits.map(u => (<option key={u.id} value={u.name}>{u.name}</option>))}
              </select>
            </div>
            <button onClick={handleAddItem} style={{ fontSize: 16, padding: 10, backgroundColor: '#28a745', color: 'white' }}>Add to Inventory</button>
          </div>
        )}
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
              <th style={{ textAlign: 'left', padding: 12 }}>Item</th>
              <th style={{ textAlign: 'left', padding: 12 }}>Quantity</th>
              <th style={{ textAlign: 'left', padding: 12 }}>Location</th>
              <th style={{ textAlign: 'left', padding: 12 }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map(inv => (
              <tr key={inv.id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: 12 }}>{inv.item}</td>
                <td style={{ padding: 12 }}>{inv.quantity}</td>
                <td style={{ padding: 12 }}>{inv.location}</td>
                <td style={{ padding: 12, color: inv.status === 'Stored' ? '#4CAF50' : '#FF9800', fontWeight: 'bold' }}>{inv.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}