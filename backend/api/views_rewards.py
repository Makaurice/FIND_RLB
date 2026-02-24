"""
FIND Token Reward Distribution API Endpoints
- Claim rewards
- View balances
- Distribution history
- Reward statistics
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reward_engine import RewardEngine

# Initialize reward engine
reward_engine = RewardEngine()


class RewardBalanceView(APIView):
    """Get FIND token balance for a user."""
    
    def get(self, request, user_id):
        """Get user's FIND token balance."""
        try:
            balance = reward_engine.get_user_balance(user_id)
            
            return Response(
                {
                    'userId': user_id,
                    'findBalance': balance,
                    'unit': 'FIND',
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClaimRewardView(APIView):
    """Claim a reward and add to user's FIND balance."""
    
    def post(self, request):
        """
        Claim a reward
        Body: {
            "userId": "user@example.com",
            "rewardType": "REFERRAL|REVIEW|PAYMENT_BONUS",
            "amount": 100.0
        }
        """
        try:
            user_id = request.data.get('userId')
            reward_type = request.data.get('rewardType')
            amount = request.data.get('amount')
            
            if not all([user_id, reward_type, amount]):
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if amount <= 0:
                return Response(
                    {'error': 'Amount must be positive'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            result = reward_engine.claim_reward(user_id, reward_type, amount)
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReferralRewardView(APIView):
    """Calculate referral rewards."""
    
    def post(self, request):
        """
        Calculate referral reward
        Body: {
            "referrerId": "user@example.com",
            "referredUserId": "friend@example.com",
            "referredMonthlyRent": 2000
        }
        """
        try:
            referrer_id = request.data.get('referrerId')
            referred_user_id = request.data.get('referredUserId')
            referred_rent = request.data.get('referredMonthlyRent', 0)
            
            if not all([referrer_id, referred_user_id]):
                return Response(
                    {'error': 'Missing referrer or referred user ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            reward = reward_engine.calculate_referral_reward(
                referrer_id, referred_user_id, referred_rent
            )
            
            return Response(reward, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviewRewardView(APIView):
    """Calculate review rewards."""
    
    def post(self, request):
        """
        Calculate reward for review
        Body: {
            "reviewerId": "user@example.com",
            "targetUserId": "landlord@example.com",
            "rating": 5,
            "commentLength": 250
        }
        """
        try:
            reviewer_id = request.data.get('reviewerId')
            target_user_id = request.data.get('targetUserId')
            rating = request.data.get('rating')
            comment_length = request.data.get('commentLength', 0)
            
            if not all([reviewer_id, target_user_id, rating]):
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if rating < 1 or rating > 5:
                return Response(
                    {'error': 'Rating must be 1-5'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            reward = reward_engine.calculate_review_reward(
                reviewer_id, target_user_id, rating, comment_length
            )
            
            return Response(reward, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentBonusView(APIView):
    """Calculate payment streak bonuses."""
    
    def post(self, request):
        """
        Calculate payment bonus
        Body: {
            "tenantId": "user@example.com",
            "monthsOnTime": 12,
            "consecutiveOnTime": true
        }
        """
        try:
            tenant_id = request.data.get('tenantId')
            months_on_time = request.data.get('monthsOnTime', 0)
            consecutive = request.data.get('consecutiveOnTime', True)
            
            if not tenant_id:
                return Response(
                    {'error': 'Tenant ID required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            bonus = reward_engine.calculate_payment_bonus(
                tenant_id, months_on_time, consecutive
            )
            
            return Response(bonus, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TierBonusView(APIView):
    """Get tier-based monthly bonuses."""
    
    def get(self, request, user_id):
        """
        Get tier bonus info
        Query params: tier (BRONZE|SILVER|GOLD|PLATINUM)
        """
        try:
            tier = request.query_params.get('tier', 'BRONZE')
            
            bonus = reward_engine.calculate_tier_bonus(user_id, tier)
            
            return Response(bonus, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RewardHistoryView(APIView):
    """Get reward claiming history for a user."""
    
    def get(self, request, user_id):
        """Get reward history for user."""
        try:
            limit = int(request.query_params.get('limit', 50))
            
            history = reward_engine.get_user_reward_history(user_id, limit)
            
            return Response(
                {
                    'userId': user_id,
                    'totalRecords': len(history),
                    'history': history[-limit:],
                },
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DistributionScheduleView(APIView):
    """Get reward distribution schedule."""
    
    def get(self, request):
        """Get distribution information and schedule."""
        try:
            schedule = reward_engine.get_distribution_schedule()
            
            return Response(schedule, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RewardLeaderboardView(APIView):
    """Get top FIND token earners."""
    
    def get(self, request):
        """Get leaderboard of top earners."""
        try:
            limit = int(request.query_params.get('limit', 50))
            
            leaderboard = reward_engine.get_leaderboard(limit)
            
            return Response(
                {
                    'leaderboard': leaderboard,
                    'recordCount': len(leaderboard),
                },
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RewardStatisticsView(APIView):
    """Get reward distribution statistics."""
    
    def get(self, request):
        """Get system-wide reward statistics."""
        try:
            stats = reward_engine.get_statistics()
            
            return Response(stats, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
