from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_agents.tenant_agent import TenantAIAgent
from ai_agents.landlord_agent import LandlordAIAgent
from ai_agents.matching_engine import MatchingEngineAgent
from ai_agents.guardian_agent import GuardianAIAgent
from ai_agents.moving_service_agent import MovingServiceAgent
from ai_agents.savings_to_own_agent import SavingsToOwnAgent

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


class GuardianAgentView(APIView):
    """Guardian/Sponsor agent for third-party rent payments."""
    def post(self, request):
        try:
            action = request.data.get('action')
            guardian_id = request.data.get('guardian_id')
            agent = GuardianAIAgent(guardian_id)
            
            if action == 'register_tenant':
                tenant_id = request.data.get('tenant_id')
                max_support = request.data.get('max_monthly_support')
                result = agent.register_tenant(tenant_id, max_support)
            elif action == 'authorize_payment':
                tenant_id = request.data.get('tenant_id')
                lease_id = request.data.get('lease_id')
                amount = request.data.get('amount')
                result = agent.authorize_payment(tenant_id, lease_id, amount)
            elif action == 'set_budget':
                budget = request.data.get('monthly_budget')
                result = agent.set_budget(budget)
            elif action == 'payment_history':
                tenant_id = request.data.get('tenant_id')
                result = agent.get_payment_history(tenant_id)
            else:
                result = agent.get_balance_summary()
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovingServiceAgentView(APIView):
    """Moving Service agent for dynamic pricing and booking."""
    def post(self, request):
        try:
            action = request.data.get('action')
            provider_id = request.data.get('provider_id')
            agent = MovingServiceAgent(provider_id)
            
            if action == 'get_quote':
                moving_data = request.data.get('moving_data')
                result = agent.get_quote(moving_data)
            elif action == 'book_moving':
                quote_id = request.data.get('quote_id')
                customer_id = request.data.get('customer_id')
                moving_date = request.data.get('moving_date')
                truck_type = request.data.get('truck_type')
                result = agent.book_moving(quote_id, customer_id, moving_date, truck_type)
            elif action == 'complete_booking':
                booking_id = request.data.get('booking_id')
                actual_hours = request.data.get('actual_hours')
                actual_distance = request.data.get('actual_distance')
                result = agent.complete_booking(booking_id, actual_hours, actual_distance)
            elif action == 'booking_status':
                booking_id = request.data.get('booking_id')
                result = agent.get_booking_status(booking_id)
            else:
                result = agent.get_available_trucks()
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SavingsToOwnAgentView(APIView):
    """Savings-to-Own agent for rent-to-own DeFi mechanism."""
    def post(self, request):
        try:
            action = request.data.get('action')
            tenant_id = request.data.get('tenant_id')
            agent = SavingsToOwnAgent(tenant_id)
            
            if action == 'create_plan':
                property_id = request.data.get('property_id')
                target_price = request.data.get('target_price')
                monthly_rent = request.data.get('monthly_rent')
                savings_percentage = request.data.get('savings_percentage', 10)
                result = agent.create_plan(property_id, target_price, monthly_rent, savings_percentage)
            elif action == 'simulate_payment':
                plan_id = request.data.get('plan_id')
                month = request.data.get('month', 1)
                result = agent.simulate_rent_payment(plan_id, month)
            elif action == 'get_progress':
                plan_id = request.data.get('plan_id')
                result = agent.get_plan_progress(plan_id)
            elif action == 'convert_to_ownership':
                plan_id = request.data.get('plan_id')
                result = agent.convert_to_ownership(plan_id)
            elif action == 'calculate_cost':
                plan_id = request.data.get('plan_id')
                result = agent.calculate_final_cost(plan_id)
            else:
                result = agent.get_all_plans()
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
