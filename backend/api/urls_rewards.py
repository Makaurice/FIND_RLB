"""
Reward Distribution API URL Routing
"""

from django.urls import path
from .views_rewards import (
    RewardBalanceView,
    ClaimRewardView,
    ReferralRewardView,
    ReviewRewardView,
    PaymentBonusView,
    TierBonusView,
    RewardHistoryView,
    DistributionScheduleView,
    RewardLeaderboardView,
    RewardStatisticsView,
)

app_name = 'rewards'

urlpatterns = [
    # Balance endpoint
    path('balance/<str:user_id>/', RewardBalanceView.as_view(), name='balance'),
    
    # Claim rewards
    path('claim/', ClaimRewardView.as_view(), name='claim'),
    
    # Calculate specific rewards
    path('referral/', ReferralRewardView.as_view(), name='referral-reward'),
    path('review/', ReviewRewardView.as_view(), name='review-reward'),
    path('payment-bonus/', PaymentBonusView.as_view(), name='payment-bonus'),
    path('tier-bonus/<str:user_id>/', TierBonusView.as_view(), name='tier-bonus'),
    
    # History and stats
    path('history/<str:user_id>/', RewardHistoryView.as_view(), name='history'),
    path('schedule/', DistributionScheduleView.as_view(), name='schedule'),
    path('leaderboard/', RewardLeaderboardView.as_view(), name='leaderboard'),
    path('statistics/', RewardStatisticsView.as_view(), name='statistics'),
]
