import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Review {
  reviewId: number;
  reviewerId: string;
  targetUserId: string;
  rating: number;
  comment: string;
  createdAt: string;
  helpful: number;
  unhelpful: number;
}

interface UserRating {
  userId: string;
  averageRating: number;
  totalReviews: number;
  ratingBreakdown: Record<string, number>;
  reviews: Review[];
}

export default function CommunityReviewsPage() {
  const [userRating, setUserRating] = useState<UserRating | null>(null);
  const [targetUser, setTargetUser] = useState('');
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const userId = 'current_user_id'; // Get from auth context

  useEffect(() => {
    if (targetUser) {
      fetchUserRating(targetUser);
    }
  }, [targetUser]);

  const fetchUserRating = async (uid: string) => {
    try {
      const response = await axios.get(`/api/community/reviews/rating/${uid}/`);
      setUserRating(response.data);
    } catch (err) {
      setError('Failed to load reviews');
    }
  };

  const submitReview = async () => {
    if (!targetUser || !comment.trim()) {
      setError('Please select a user and write a comment');
      return;
    }

    setLoading(true);
    try {
      await axios.post('/api/community/reviews/submit/', {
        reviewerId: userId,
        targetUserId: targetUser,
        rating: rating,
        comment: comment,
      });
      setSuccess('Review submitted successfully!');
      setComment('');
      setRating(5);
      if (targetUser) {
        fetchUserRating(targetUser);
      }
    } catch (err) {
      setError('Failed to submit review');
    } finally {
      setLoading(false);
    }
  };

  const markHelpful = async (reviewId: number, helpful: boolean) => {
    try {
      await axios.post('/api/community/reviews/help/', {
        reviewId: reviewId,
        targetUserId: targetUser,
        helpful: helpful,
      });
      if (targetUser) {
        fetchUserRating(targetUser);
      }
    } catch (err) {
      setError('Failed to mark review');
    }
  };

  const renderStars = (value: number, onChange?: (val: number) => void) => {
    return (
      <div className="flex gap-2">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => onChange?.(star)}
            className={`text-3xl transition-all ${
              star <= value ? 'text-amber-400' : 'text-slate-600'
            } ${onChange ? 'cursor-pointer hover:scale-110' : ''}`}
            disabled={!onChange}
          >
            ★
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-black to-slate-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-blue-400 mb-2">
            Community Reviews
          </h1>
          <p className="text-slate-400">Build trust through genuine reviews and ratings</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Submit Review Section */}
          <div className="lg:col-span-1">
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-6 sticky top-8">
              <h2 className="text-xl font-bold text-white mb-4">Write a Review</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Landlord/Tenant
                  </label>
                  <input
                    type="text"
                    value={targetUser}
                    onChange={(e) => setTargetUser(e.target.value)}
                    placeholder="User ID or email"
                    className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 text-sm"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Rating
                  </label>
                  {renderStars(rating, setRating)}
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Comment
                  </label>
                  <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    placeholder="Share your experience..."
                    className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 text-sm h-24"
                  />
                </div>

                {error && (
                  <div className="p-3 bg-red-900/20 border border-red-700 text-red-300 rounded text-sm">
                    {error}
                  </div>
                )}

                {success && (
                  <div className="p-3 bg-green-900/20 border border-green-700 text-green-300 rounded text-sm">
                    {success}
                  </div>
                )}

                <button
                  onClick={submitReview}
                  disabled={loading || !targetUser}
                  className="w-full py-2 bg-gradient-to-r from-amber-400 to-amber-600 text-black font-semibold rounded hover:shadow-lg hover:shadow-amber-500/50 transition-all disabled:opacity-50 text-sm"
                >
                  {loading ? 'Submitting...' : 'Submit Review'}
                </button>
              </div>
            </div>
          </div>

          {/* Reviews List */}
          <div className="lg:col-span-2">
            {userRating ? (
              <>
                {/* Rating Summary */}
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-6 mb-6">
                  <h2 className="text-2xl font-bold text-white mb-4">{targetUser}</h2>

                  <div className="flex items-center gap-6 mb-4">
                    <div>
                      <div className="text-4xl font-bold text-amber-400">
                        {userRating.averageRating.toFixed(1)}
                      </div>
                      <div className="text-slate-400 text-sm">
                        {userRating.totalReviews} reviews
                      </div>
                    </div>

                    {renderStars(Math.round(userRating.averageRating))}
                  </div>

                  {/* Rating Breakdown */}
                  <div className="space-y-2">
                    {[5, 4, 3, 2, 1].map((star) => (
                      <div key={star} className="flex items-center gap-2">
                        <span className="text-sm text-slate-400 w-8">{star}★</span>
                        <div className="flex-1 h-2 bg-slate-700 rounded">
                          <div
                            className="h-full bg-gradient-to-r from-amber-400 to-amber-600 rounded"
                            style={{
                              width: `${(userRating.ratingBreakdown[star.toString()] / userRating.totalReviews) * 100}%`
                            }}
                          />
                        </div>
                        <span className="text-sm text-slate-400 w-8">
                          {userRating.ratingBreakdown[star.toString()]}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Individual Reviews */}
                <div className="space-y-4">
                  {userRating.reviews.map((review) => (
                    <div
                      key={review.reviewId}
                      className="bg-slate-800/50 border border-slate-700 rounded-lg p-4"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <p className="font-semibold text-white">{review.reviewerId}</p>
                          {renderStars(review.rating)}
                        </div>
                        <p className="text-xs text-slate-500">
                          {new Date(review.createdAt).toLocaleDateString()}
                        </p>
                      </div>

                      <p className="text-slate-300 text-sm mb-3">{review.comment}</p>

                      <div className="flex gap-4">
                        <button
                          onClick={() => markHelpful(review.reviewId, true)}
                          className="text-xs px-3 py-1 bg-green-600/20 hover:bg-green-600/40 text-green-300 rounded transition-colors"
                        >
                          👍 Helpful ({review.helpful})
                        </button>
                        <button
                          onClick={() => markHelpful(review.reviewId, false)}
                          className="text-xs px-3 py-1 bg-red-600/20 hover:bg-red-600/40 text-red-300 rounded transition-colors"
                        >
                          👎 Not Helpful ({review.unhelpful})
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : targetUser ? (
              <div className="text-center py-12">
                <p className="text-slate-400">No reviews yet for this user</p>
              </div>
            ) : (
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-12 text-center">
                <p className="text-slate-400">Enter a user ID to view or submit reviews</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
