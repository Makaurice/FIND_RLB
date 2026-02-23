from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_agents.tenant_agent import TenantAIAgent
from ai_agents.landlord_agent import LandlordAIAgent
from ai_agents.matching_engine import MatchingEngineAgent

class TenantAgentView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        preferences = request.data.get('preferences')
        properties = request.data.get('properties')
        agent = TenantAIAgent(user_id)
        agent.learn_preferences(preferences)
        recommended = agent.recommend_home(properties)
        negotiation = agent.recommend_negotiation(recommended)
        savings_plan = agent.recommend_savings_plan(recommended)
        return Response({
            'recommended_home': recommended,
            'negotiation': negotiation,
            'savings_plan': savings_plan
        }, status=status.HTTP_200_OK)

class LandlordAgentView(APIView):
    def post(self, request):
        landlord_id = request.data.get('landlord_id')
        property = request.data.get('property')
        market_data = request.data.get('market_data')
        history = request.data.get('history')
        lease = request.data.get('lease')
        tenant = request.data.get('tenant')
        agent = LandlordAIAgent(landlord_id)
        optimal_rent = agent.set_optimal_rent(property, market_data)
        vacancy = agent.forecast_vacancy(property, history)
        reminder = agent.send_reminder(tenant, lease)
        enforcement = agent.auto_enforce_lease(lease)
        return Response({
            'optimal_rent': optimal_rent,
            'vacancy': vacancy,
            'reminder': reminder,
            'enforcement': enforcement
        }, status=status.HTTP_200_OK)

class MatchingEngineView(APIView):
    def post(self, request):
        tenants = request.data.get('tenants')
        properties = request.data.get('properties')
        agent = MatchingEngineAgent()
        matches = agent.match(tenants, properties)
        return Response({'matches': matches}, status=status.HTTP_200_OK)

class TopMatchesView(APIView):
    def post(self, request):
        tenants = request.data.get('tenants')
        properties = request.data.get('properties')
        n = request.data.get('n', 3)
        agent = MatchingEngineAgent()
        top_matches = agent.get_top_matches(tenants, properties, n)
        return Response({'top_matches': top_matches}, status=status.HTTP_200_OK)

class AdvancedTenantRecommendationView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        preferences = request.data.get('preferences')
        agent = TenantAIAgent(user_id)
        agent.learn_preferences(preferences)
        # Use ML model for advanced recommendation
        recommended = agent.recommend_home()
        return Response({'advanced_recommendation': recommended}, status=status.HTTP_200_OK)
