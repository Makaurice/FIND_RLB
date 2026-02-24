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
    <div className="min-h-screen bg-gradient-to-br from-[#e6e2d3] via-[#b3c6e7] to-[#23272b] py-12 px-4 font-sans">
      <h2 className="text-4xl font-extrabold text-[#23272b] mb-6 text-center tracking-tight">Reviews & Ratings</h2>
      <div className="max-w-xl mx-auto bg-gradient-to-r from-[#f7ca18] via-[#f8fafc] to-[#b3c6e7] p-8 rounded-2xl shadow-xl mb-10 text-center border border-[#e6e2d3]">
        <h3 className="text-2xl font-bold text-[#23272b] mb-2">Average Rating: <span className="text-[#f7ca18]">{averageRating}</span> / 5</h3>
        <p className="text-[#6c7a89]">Based on {reviews.length} reviews</p>
      </div>
      <div className="flex justify-center mb-8">
        <button
          onClick={() => setShowReviewForm(!showReviewForm)}
          className="px-8 py-3 rounded-xl font-bold text-lg bg-gradient-to-r from-[#5bc0eb] via-[#23272b] to-[#f7ca18] text-white shadow-lg hover:from-[#f7ca18] hover:to-[#5bc0eb] transition border-2 border-[#b3c6e7]"
        >
          {showReviewForm ? 'Cancel' : '+ Write Review'}
        </button>
      </div>
      {showReviewForm && (
        <div className="max-w-xl mx-auto bg-white border border-[#b3c6e7] rounded-2xl shadow-lg p-8 mb-10">
          <h3 className="text-xl font-bold text-[#23272b] mb-4">Rate Your Landlord</h3>
          <div className="flex justify-center mb-4">
            {[1, 2, 3, 4, 5].map(star => (
              <button
                key={star}
                onClick={() => setMyRating(star)}
                className={`text-3xl mx-1 transition ${star <= myRating ? 'text-[#f7ca18]' : 'text-[#b3c6e7]'}`}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
              >
                ★
              </button>
            ))}
          </div>
          <textarea
            placeholder="Share your experience..."
            value={myComment}
            onChange={e => setMyComment(e.target.value)}
            className="w-full rounded-lg border border-[#b3c6e7] p-4 mb-4 text-[#23272b] focus:ring-2 focus:ring-[#5bc0eb] focus:border-transparent"
            style={{ minHeight: 80 }}
          />
          <button
            onClick={handleSubmitReview}
            className="w-full px-6 py-3 bg-gradient-to-r from-[#23272b] via-[#5bc0eb] to-[#e6e2d3] text-white rounded-lg font-bold shadow hover:from-[#f7ca18] hover:to-[#5bc0eb] transition"
          >
            Submit Review
          </button>
        </div>
      )}
      <h3 className="text-2xl font-bold text-[#23272b] mb-6 mt-12 text-center">Recent Reviews</h3>
      <div className="max-w-3xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        {reviews.map(r => (
          <div key={r.id} className="bg-gradient-to-br from-[#f8fafc] via-[#e6e2d3] to-[#b3c6e7] border border-[#e6e2d3] rounded-2xl shadow-lg p-6">
            <div className="flex justify-between items-center mb-2">
              <b className="text-[#23272b]">{r.landlord}</b>
              <span className="text-[#f7ca18] text-xl">{'★'.repeat(r.rating)}{'☆'.repeat(5 - r.rating)}</span>
            </div>
            <p className="text-[#6c7a89] mb-2">{r.comment}</p>
            <p className="text-xs text-[#b3c6e7]">{r.date}</p>
          </div>
        ))}
      </div>
    </div>
  );
}