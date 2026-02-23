import React, { useState } from 'react';

export default function Movers() {
  const [services, setServices] = useState([
    { id: 1, name: 'Quick Movers Co.', rating: 4.8, price: 500, availability: 'Available', reviews: 245 },
    { id: 2, name: 'Professional Relocations', rating: 4.6, price: 600, availability: 'Available', reviews: 189 },
    { id: 3, name: 'Local Moving Experts', rating: 4.9, price: 450, availability: 'Booked', reviews: 312 },
  ]);
  const [bookings, setBookings] = useState([
    { id: 1, provider: 'Quick Movers Co.', date: '2026-03-15', status: 'Scheduled', amount: 500 },
    { id: 2, provider: 'Professional Relocations', date: '2026-02-20', status: 'Completed', amount: 600 },
  ]);
  const [showBookingForm, setShowBookingForm] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<any>(null);
  const [bookingDetails, setBookingDetails] = useState({ date: '', items: '', destination: '' });

  const handleBook = () => {
    if (selectedProvider && bookingDetails.date) {
      setBookings([...bookings, {
        id: Date.now(),
        provider: selectedProvider.name,
        date: bookingDetails.date,
        status: 'Scheduled',
        amount: selectedProvider.price
      }]);
      setBookingDetails({ date: '', items: '', destination: '' });
      setShowBookingForm(false);
      setSelectedProvider(null);
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Movers</h2>
      <div style={{ marginBottom: 24 }}>
        <h3>Available Moving Services</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {services.map(service => (
            <div key={service.id} style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
              <h4>{service.name}</h4>
              <div style={{ marginBottom: 12 }}>
                <span style={{ color: '#FFD700', fontWeight: 'bold' }}>★ {service.rating}</span>
                <span style={{ marginLeft: 12, color: '#666' }}>({service.reviews} reviews)</span>
              </div>
              <p style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 8 }}>${service.price}</p>
              <p style={{ marginBottom: 12, color: service.availability === 'Available' ? '#4CAF50' : '#FF9800' }}>
                {service.availability}
              </p>
              <button
                onClick={() => {
                  setSelectedProvider(service);
                  setShowBookingForm(true);
                }}
                disabled={service.availability === 'Booked'}
                style={{
                  width: '100%',
                  padding: 10,
                  backgroundColor: service.availability === 'Booked' ? '#ccc' : '#007bff',
                  color: 'white',
                  border: 'none',
                  borderRadius: 4,
                  cursor: service.availability === 'Booked' ? 'not-allowed' : 'pointer'
                }}
              >
                {service.availability === 'Booked' ? 'Booked' : 'Book'}
              </button>
            </div>
          ))}
        </div>
      </div>
      {showBookingForm && selectedProvider && (
        <div style={{ border: '1px solid #ddd', padding: 20, marginBottom: 24, borderRadius: 8, backgroundColor: '#f9f9f9' }}>
          <h3>Book {selectedProvider.name}</h3>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 8 }}>Moving Date:</label>
            <input
              type="date"
              value={bookingDetails.date}
              onChange={e => setBookingDetails({ ...bookingDetails, date: e.target.value })}
              style={{ fontSize: 14, padding: 8, width: '100%' }}
            />
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 8 }}>Items to Move:</label>
            <textarea
              placeholder="List furniture, boxes, etc."
              value={bookingDetails.items}
              onChange={e => setBookingDetails({ ...bookingDetails, items: e.target.value })}
              style={{ fontSize: 14, padding: 8, width: '100%', minHeight: 80 }}
            />
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 8 }}>Destination Address:</label>
            <input
              type="text"
              placeholder="Enter destination address"
              value={bookingDetails.destination}
              onChange={e => setBookingDetails({ ...bookingDetails, destination: e.target.value })}
              style={{ fontSize: 14, padding: 8, width: '100%' }}
            />
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <button onClick={handleBook} style={{ fontSize: 16, padding: 10, backgroundColor: '#28a745', color: 'white', cursor: 'pointer' }}>Confirm Booking</button>
            <button onClick={() => setShowBookingForm(false)} style={{ fontSize: 16, padding: 10, backgroundColor: '#ccc', cursor: 'pointer' }}>Cancel</button>
          </div>
        </div>
      )}
      <h3>Your Bookings</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ccc' }}>
            <th style={{ textAlign: 'left', padding: 12 }}>Provider</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Date</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Amount</th>
            <th style={{ textAlign: 'left', padding: 12 }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {bookings.map(b => (
            <tr key={b.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 12 }}>{b.provider}</td>
              <td style={{ padding: 12 }}>{b.date}</td>
              <td style={{ padding: 12 }}>${b.amount}</td>
              <td style={{ padding: 12, color: b.status === 'Completed' ? '#4CAF50' : '#FF9800', fontWeight: 'bold' }}>{b.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}