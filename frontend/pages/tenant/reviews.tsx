import React, { useState } from 'react';

export default function Reviews() {
  const [reviews, setReviews] = useState([
    { id: 1, property: '123 Main St', landlord: 'John Smith', rating: 5, comment: 'Great landlord, very responsive!', date: '2026-01-15' },
    { id: 2, property: '123 Main St', landlord: 'John Smith', rating: 4, comment: 'Good maintenance, minor issues', date: '2025-12-20' },
  ]);
  const [myRating, setMyRating] = useState(0);
  const [myComment, setMyComment] = useState('');
  const [showReviewForm, setShowReviewForm] = useState(false);

  const handleSubmitReview = () => {
    if (myRating > 0 && myComment) {
      setReviews([...reviews, {
        id: Date.now(),
        property: '123 Main St',
        landlord: 'John Smith',
        rating: myRating,
        comment: myComment,
        date: new Date().toISOString().split('T')[0]
      }]);
      setMyRating(0);
      setMyComment('');
      setShowReviewForm(false);
    }
  };

  const averageRating = (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1);

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2>Reviews & Ratings</h2>
      <div style={{ backgroundColor: '#f9f9f9', padding: 16, marginBottom: 24, borderRadius: 8 }}>
        <h3>Average Rating: {averageRating} / 5</h3>
        <p>Based on {reviews.length} reviews</p>
      </div>
      <button onClick={() => setShowReviewForm(!showReviewForm)} style={{ fontSize: 16, padding: 10, marginBottom: 20, backgroundColor: '#007bff', color: 'white' }}>
        {showReviewForm ? 'Cancel' : '+ Write Review'}
      </button>
      {showReviewForm && (
        <div style={{ border: '1px solid #ddd', padding: 16, marginBottom: 20, borderRadius: 8 }}>
          <h3>Rate Your Landlord</h3>
          <div style={{ marginBottom: 12 }}>
            {[1, 2, 3, 4, 5].map(star => (
              <button
                key={star}
                onClick={() => setMyRating(star)}
                style={{
                  fontSize: 24,
                  marginRight: 8,
                  backgroundColor: star <= myRating ? '#FFD700' : '#ddd',
                  border: 'none',
                  cursor: 'pointer',
                  borderRadius: 4
                }}
              >
                ★
              </button>
            ))}
          </div>
          <textarea
            placeholder="Share your experience..."
            value={myComment}
            onChange={e => setMyComment(e.target.value)}
            style={{ fontSize: 14, padding: 8, width: '100%', minHeight: 80, marginBottom: 10 }}
          />
          <button onClick={handleSubmitReview} style={{ fontSize: 16, padding: 10, backgroundColor: '#28a745', color: 'white' }}>Submit Review</button>
        </div>
      )}
      <h3 style={{ marginTop: 30 }}>Recent Reviews</h3>
      {reviews.map(r => (
        <div key={r.id} style={{ border: '1px solid #eee', padding: 16, marginBottom: 12, borderRadius: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <b>{r.landlord}</b>
            <span style={{ color: '#FFD700' }}>{'★'.repeat(r.rating)}{'☆'.repeat(5 - r.rating)}</span>
          </div>
          <p style={{ margin: '0 0 8px 0', color: '#666' }}>{r.comment}</p>
          <p style={{ margin: 0, fontSize: 12, color: '#999' }}>{r.date}</p>
        </div>
      ))}
    </div>
  );
}