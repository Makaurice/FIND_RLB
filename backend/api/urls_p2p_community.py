"""
P2P Community AI Agent URL routing
"""

from django.urls import path
from .views_p2p_community import (
    TenantRecommendationsView,
    LandlordRecommendationsView,
    PeerInsightsView,
    NegotiationSuggestionsView,
    CommunityStatsView,
)

app_name = 'p2p_community'

urlpatterns = [
    # Tenant to landlord recommendations
    path('tenant/recommendations/<str:tenant_id>/', TenantRecommendationsView.as_view(), name='tenant-recommendations'),
    
    # Landlord to tenant recommendations
    path('landlord/recommendations/<str:landlord_id>/', LandlordRecommendationsView.as_view(), name='landlord-recommendations'),
    
    # Peer insights
    path('peer-insights/<str:user_id>/', PeerInsightsView.as_view(), name='peer-insights'),
    
    # Negotiation suggestions
    path('negotiation-suggestions/', NegotiationSuggestionsView.as_view(), name='negotiation-suggestions'),
    
    # Community stats
    path('stats/', CommunityStatsView.as_view(), name='community-stats'),
]
