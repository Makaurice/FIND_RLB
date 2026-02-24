from django.urls import path
from ..ai_agent_api import (
    TenantAgentView, LandlordAgentView, MatchingEngineView, TopMatchesView, 
    AdvancedTenantRecommendationView, GuardianAgentView, MovingServiceAgentView, 
    SavingsToOwnAgentView
)

urlpatterns = [
    path('ai/tenant', TenantAgentView.as_view()),
    path('ai/landlord', LandlordAgentView.as_view()),
    path('ai/match', MatchingEngineView.as_view()),
    path('ai/top-matches', TopMatchesView.as_view()),
    path('ai/tenant/advanced', AdvancedTenantRecommendationView.as_view()),
    path('ai/guardian', GuardianAgentView.as_view()),
    path('ai/moving-service', MovingServiceAgentView.as_view()),
    path('ai/savings-to-own', SavingsToOwnAgentView.as_view()),
]
