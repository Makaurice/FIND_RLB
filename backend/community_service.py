"""
P2P Community & Referral System
- Peer reviews and ratings
- Referral rewards
- Community governance
- Reputation-based incentives
"""

from typing import Optional, Dict, Any, List
from datetime import datetime

class CommunityService:
    """Manages P2P community interactions and referrals."""
    
    def __init__(self):
        self.referrals: Dict[str, List[Dict]] = {}
        self.reviews: Dict[str, List[Dict]] = {}
        self.ratings: Dict[str, List[float]] = {}
        self.reward_pool = 0.0
        self.base_referral_reward = 100.0  # FIND tokens

    def submit_referral(self, referrer_id: str, referred_user_id: str, referral_code: str) -> Dict[str, Any]:
        """
        Submit a referral. Rewards when referred user completes action.
        
        Args:
            referrer_id: User who made the referral
            referred_user_id: New user being referred
            referral_code: Reference code
            
        Returns:
            Referral record
        """
        if referrer_id not in self.referrals:
            self.referrals[referrer_id] = []
        
        referral = {
            'referrerId': referrer_id,
            'referredUserId': referred_user_id,
            'referralCode': referral_code,
            'status': 'PENDING',
            'createdAt': datetime.now().isoformat(),
            'completionRewardWaiting': self.base_referral_reward,
        }
        
        self.referrals[referrer_id].append(referral)
        return referral

    def claim_referral_reward(self, referrer_id: str, referred_user_id: str) -> Dict[str, Any]:
        """
        Claim reward when referred user completes action (sign up, rent payment, etc.).
        """
        if referrer_id not in self.referrals:
            return {'error': 'No referrals found'}
        
        for referral in self.referrals[referrer_id]:
            if referral['referredUserId'] == referred_user_id and referral['status'] == 'PENDING':
                referral['status'] = 'COMPLETED'
                referral['claimedAt'] = datetime.now().isoformat()
                
                return {
                    'referrerId': referrer_id,
                    'referredUserId': referred_user_id,
                    'rewardAmount': self.base_referral_reward,
                    'rewardToken': 'FIND',
                    'status': 'CLAIMED',
                    'claimedAt': datetime.now().isoformat(),
                }
        
        return {'error': 'Referral not found or already claimed'}

    def get_referral_stats(self, user_id: str) -> Dict[str, Any]:
        """Get referral statistics for a user."""
        if user_id not in self.referrals:
            return {
                'userId': user_id,
                'totalReferrals': 0,
                'completedReferrals': 0,
                'pendingReferrals': 0,
                'totalEarnings': 0.0,
            }
        
        referrals = self.referrals[user_id]
        completed = [r for r in referrals if r['status'] == 'COMPLETED']
        pending = [r for r in referrals if r['status'] == 'PENDING']
        
        return {
            'userId': user_id,
            'totalReferrals': len(referrals),
            'completedReferrals': len(completed),
            'pendingReferrals': len(pending),
            'totalEarnings': len(completed) * self.base_referral_reward,
            'referrals': referrals,
        }

    def submit_review(self, reviewer_id: str, target_user_id: str, rating: float, comment: str) -> Dict[str, Any]:
        """
        Submit a review for another user (tenant reviewing landlord, etc.).
        
        Args:
            reviewer_id: User submitting review
            target_user_id: User being reviewed
            rating: Rating 1-5 stars
            comment: Review comment
            
        Returns:
            Review record
        """
        if rating < 1 or rating > 5:
            return {'error': 'Rating must be 1-5 stars'}
        
        if target_user_id not in self.reviews:
            self.reviews[target_user_id] = []
            self.ratings[target_user_id] = []
        
        review = {
            'reviewId': len(self.reviews[target_user_id]) + 1,
            'reviewerId': reviewer_id,
            'targetUserId': target_user_id,
            'rating': rating,
            'comment': comment,
            'createdAt': datetime.now().isoformat(),
            'helpful': 0,
            'unhelpful': 0,
        }
        
        self.reviews[target_user_id].append(review)
        self.ratings[target_user_id].append(rating)
        
        return review

    def get_user_rating(self, user_id: str) -> Dict[str, Any]:
        """Get average rating and reviews for a user."""
        if user_id not in self.ratings or not self.ratings[user_id]:
            return {
                'userId': user_id,
                'averageRating': 0.0,
                'totalReviews': 0,
                'reviewDetails': [],
            }
        
        ratings = self.ratings[user_id]
        avg_rating = sum(ratings) / len(ratings)
        
        return {
            'userId': user_id,
            'averageRating': round(avg_rating, 2),
            'totalReviews': len(ratings),
            'ratingBreakdown': {
                '5': len([r for r in ratings if r == 5.0]),
                '4': len([r for r in ratings if r == 4.0]),
                '3': len([r for r in ratings if r == 3.0]),
                '2': len([r for r in ratings if r == 2.0]),
                '1': len([r for r in ratings if r == 1.0]),
            },
            'reviews': self.reviews.get(user_id, []),
        }

    def help_review(self, review_id: int, target_user_id: str, helpful: bool) -> Dict[str, Any]:
        """Mark a review as helpful or unhelpful."""
        if target_user_id not in self.reviews:
            return {'error': 'User not found'}
        
        for review in self.reviews[target_user_id]:
            if review['reviewId'] == review_id:
                if helpful:
                    review['helpful'] += 1
                else:
                    review['unhelpful'] += 1
                return {
                    'reviewId': review_id,
                    'helpful': review['helpful'],
                    'unhelpful': review['unhelpful'],
                }
        
        return {'error': 'Review not found'}

    def get_leaderboard(self, category: str = 'top_rated') -> Dict[str, Any]:
        """
        Get community leaderboard.
        Categories: top_rated, most_referrals, most_trusted
        """
        if category == 'top_rated':
            sorted_users = sorted(
                [(uid, sum(ratings) / len(ratings)) for uid, ratings in self.ratings.items() if ratings],
                key=lambda x: x[1],
                reverse=True
            )
            return {
                'category': category,
                'leaderboard': [
                    {'rank': i+1, 'userId': uid, 'rating': round(rating, 2)}
                    for i, (uid, rating) in enumerate(sorted_users[:50])
                ],
            }
        
        elif category == 'most_referrals':
            sorted_users = sorted(
                [(uid, len(refs)) for uid, refs in self.referrals.items()],
                key=lambda x: x[1],
                reverse=True
            )
            return {
                'category': category,
                'leaderboard': [
                    {'rank': i+1, 'userId': uid, 'referrals': count}
                    for i, (uid, count) in enumerate(sorted_users[:50])
                ],
            }
        
        else:
            return {'error': f'Unknown category: {category}'}

    def get_trust_score(self, user_id: str) -> Dict[str, Any]:
        """
        Calculate a holistic trust score based on:
        - Payment history
        - Reviews
        - Referrals
        - Reputation
        """
        rating_score = 0.0
        if user_id in self.ratings and self.ratings[user_id]:
            rating_score = (sum(self.ratings[user_id]) / len(self.ratings[user_id])) * 20
        
        referral_score = 0.0
        if user_id in self.referrals:
            completed = len([r for r in self.referrals[user_id] if r['status'] == 'COMPLETED'])
            referral_score = min(completed * 5, 20)  # Max 20 points
        
        # Payment history and reputation would come from other sources
        payment_score = 30  # Placeholder
        reputation_score = 30  # Placeholder
        
        total_trust = rating_score + referral_score + payment_score + reputation_score
        
        return {
            'userId': user_id,
            'trustScore': round(total_trust, 2),
            'breakdown': {
                'ratingScore': round(rating_score, 2),
                'referralScore': round(referral_score, 2),
                'paymentScore': round(payment_score, 2),
                'reputationScore': round(reputation_score, 2),
            },
            'trustLevel': self._get_trust_level(total_trust),
        }

    def _get_trust_level(self, score: float) -> str:
        """Convert trust score to level."""
        if score >= 90:
            return 'PLATINUM'
        elif score >= 75:
            return 'GOLD'
        elif score >= 60:
            return 'SILVER'
        elif score >= 45:
            return 'BRONZE'
        else:
            return 'NEW'
