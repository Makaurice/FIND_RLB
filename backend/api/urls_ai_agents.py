from django.urls import path
from ..ai_agent_api import TenantAgentView, LandlordAgentView, MatchingEngineView, TopMatchesView, AdvancedTenantRecommendationView

urlpatterns = [
    path('ai/tenant', TenantAgentView.as_view()),
    path('ai/landlord', LandlordAgentView.as_view()),
    path('ai/match', MatchingEngineView.as_view()),
    path('ai/top-matches', TopMatchesView.as_view()),
    path('ai/tenant/advanced', AdvancedTenantRecommendationView.as_view()),
]
