"""
P2P Community API Views
- Referral endpoints
- Review endpoints
- Leaderboard endpoints
- Trust score endpoints
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from community_service import CommunityService

# Initialize community service
community_service = CommunityService()


class ReferralSubmitView(APIView):
    """Submit a new referral."""
    
    def post(self, request):
        """
        Submit referral
        Body: {
            "referrerId": "user123",
            "referredUserId": "newuser456",
            "referralCode": "REF123ABC"
        }
        """
        try:
            referrer_id = request.data.get('referrerId')
            referred_user_id = request.data.get('referredUserId')
            referral_code = request.data.get('referralCode')
            
            if not all([referrer_id, referred_user_id, referral_code]):
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            referral = community_service.submit_referral(
                referrer_id, referred_user_id, referral_code
            )
            
            return Response(referral, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReferralClaimView(APIView):
    """Claim referral reward when referred user completes action."""
    
    def post(self, request):
        """
        Claim reward
        Body: {
            "referrerId": "user123",
            "referredUserId": "newuser456"
        }
        """
        try:
            referrer_id = request.data.get('referrerId')
            referred_user_id = request.data.get('referredUserId')
            
            if not all([referrer_id, referred_user_id]):
                return Response(
                    {'error': 'Missing referrer or referred user ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            reward = community_service.claim_referral_reward(referrer_id, referred_user_id)
            
            if 'error' in reward:
                return Response(reward, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(reward, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReferralStatsView(APIView):
    """Get referral statistics for a user."""
    
    def get(self, request, user_id):
        """Get referral stats for user."""
        try:
            stats = community_service.get_referral_stats(user_id)
            return Response(stats, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviewSubmitView(APIView):
    """Submit a review for another user."""
    
    def post(self, request):
        """
        Submit review
        Body: {
            "reviewerId": "user123",
            "targetUserId": "user456",
            "rating": 5,
            "comment": "Great landlord, very responsive"
        }
        """
        try:
            reviewer_id = request.data.get('reviewerId')
            target_user_id = request.data.get('targetUserId')
            rating = request.data.get('rating')
            comment = request.data.get('comment')
            
            if not all([reviewer_id, target_user_id, rating, comment]):
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
                return Response(
                    {'error': 'Rating must be between 1 and 5'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            review = community_service.submit_review(
                reviewer_id, target_user_id, rating, comment
            )
            
            if 'error' in review:
                return Response(review, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(review, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRatingView(APIView):
    """Get user rating and reviews."""
    
    def get(self, request, user_id):
        """Get average rating and review details."""
        try:
            rating_data = community_service.get_user_rating(user_id)
            return Response(rating_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviewHelpView(APIView):
    """Mark a review as helpful or unhelpful."""
    
    def post(self, request):
        """
        Mark review helpfulness
        Body: {
            "reviewId": 1,
            "targetUserId": "user456",
            "helpful": true
        }
        """
        try:
            review_id = request.data.get('reviewId')
            target_user_id = request.data.get('targetUserId')
            helpful = request.data.get('helpful')
            
            if review_id is None or not target_user_id or helpful is None:
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            result = community_service.help_review(review_id, target_user_id, helpful)
            
            if 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LeaderboardView(APIView):
    """Get community leaderboard."""
    
    def get(self, request):
        """
        Get leaderboard
        Query params: category (top_rated, most_referrals, most_trusted)
        """
        try:
            category = request.query_params.get('category', 'top_rated')
            leaderboard = community_service.get_leaderboard(category)
            
            if 'error' in leaderboard:
                return Response(leaderboard, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(leaderboard, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrustScoreView(APIView):
    """Get trust score for a user."""
    
    def get(self, request, user_id):
        """
        Get holistic trust score based on:
        - Reviews and ratings
        - Referral success
        - Payment history
        - Reputation
        """
        try:
            trust_data = community_service.get_trust_score(user_id)
            return Response(trust_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
