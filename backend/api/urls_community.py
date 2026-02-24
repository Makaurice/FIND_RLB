"""
P2P Community API URL routing
"""

from django.urls import path
from .views_community import (
    ReferralSubmitView,
    ReferralClaimView,
    ReferralStatsView,
    ReviewSubmitView,
    UserRatingView,
    ReviewHelpView,
    LeaderboardView,
    TrustScoreView,
)

app_name = 'community'

urlpatterns = [
    # Referral endpoints
    path('referrals/submit/', ReferralSubmitView.as_view(), name='referral-submit'),
    path('referrals/claim/', ReferralClaimView.as_view(), name='referral-claim'),
    path('referrals/stats/<str:user_id>/', ReferralStatsView.as_view(), name='referral-stats'),
    
    # Review endpoints
    path('reviews/submit/', ReviewSubmitView.as_view(), name='review-submit'),
    path('reviews/rating/<str:user_id>/', UserRatingView.as_view(), name='user-rating'),
    path('reviews/help/', ReviewHelpView.as_view(), name='review-help'),
    
    # Community endpoints
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('trust-score/<str:user_id>/', TrustScoreView.as_view(), name='trust-score'),
]
