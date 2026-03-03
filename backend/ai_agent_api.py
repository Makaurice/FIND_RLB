from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_agents.tenant_agent import TenantAIAgent
from ai_agents.landlord_agent import LandlordAIAgent
from ai_agents.matching_engine import MatchingEngineAgent
from ai_agents.guardian_agent import GuardianAIAgent
from ai_agents.moving_service_agent import MovingServiceAgent
from ai_agents.savings_to_own_agent import SavingsToOwnAgent
from ai_agents.p2p_community_agent import P2PCommunityAgent
from backend.hedera_auth import generate_challenge, verify_signature
from backend.contracts import call_hedera_contract, get_contract
from backend.hedera_integration_v2 import get_hedera_client
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class TenantAgentView(APIView):
    def post(self, request):
        action = request.data.get('action', 'recommend')
        user_id = request.data.get('user_id')
        agent = TenantAIAgent(user_id)
        if action == 'recommend':
            preferences = request.data.get('preferences')
            properties = request.data.get('properties')
            agent.learn_preferences(preferences)
            recommended = agent.recommend_home(properties)
            negotiation = agent.recommend_negotiation(recommended)
            savings_plan = agent.recommend_savings_plan(recommended)
            return Response({
                'recommended_home': recommended,
                'negotiation': negotiation,
                'savings_plan': savings_plan
            }, status=status.HTTP_200_OK)
        elif action == 'ingest_chain':
            agent.ingest_chain_data()
            return Response({'status': 'ingested'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unknown action'}, status=status.HTTP_400_BAD_REQUEST)

class LandlordAgentView(APIView):
    def post(self, request):
        action = request.data.get('action', 'analyze')
        landlord_id = request.data.get('landlord_id')
        agent = LandlordAIAgent(landlord_id)
        if action == 'analyze':
            property = request.data.get('property')
            market_data = request.data.get('market_data')
            history = request.data.get('history')
            lease = request.data.get('lease')
            tenant = request.data.get('tenant')
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
        elif action == 'ingest_market':
            agent.ingest_market_history()
            return Response({'status': 'market history ingested'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unknown action'}, status=status.HTTP_400_BAD_REQUEST)

class MatchingEngineView(APIView):
    def post(self, request):
        action = request.data.get('action', 'match')
        agent = MatchingEngineAgent()
        if action == 'match':
            tenants = request.data.get('tenants')
            properties = request.data.get('properties')
            matches = agent.match(tenants, properties)
            return Response({'matches': matches}, status=status.HTTP_200_OK)
        elif action == 'ingest_feedback':
            agent.ingest_chain_feedback()
            return Response({'status': 'feedback ingested'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'unknown action'}, status=status.HTTP_400_BAD_REQUEST)

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


class P2PCommunityAgentView(APIView):
    """Endpoint for peer-to-peer community recommendations and insights."""
    def post(self, request):
        try:
            action = request.data.get('action')
            user_id = request.data.get('user_id')
            agent = P2PCommunityAgent()
            
            if action == 'register_user':
                user_type = request.data.get('user_type', 'tenant')
                result = agent.register_user(user_id, user_type)
            elif action == 'tenant_recs':
                limit = request.data.get('limit', 5)
                result = agent.get_tenant_recommendations(user_id, limit)
            elif action == 'landlord_recs':
                limit = request.data.get('limit', 5)
                result = agent.get_landlord_recommendations(user_id, limit)
            elif action == 'peer_insights':
                result = agent.get_peer_insights(user_id)
            elif action == 'stats':
                result = agent.get_community_stats()
            else:
                result = {'error': 'unknown action'}
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HederaAuthView(APIView):
    """Authenticate users via Hedera key signature and issue JWTs."""
    def post(self, request):
        try:
            action = request.data.get('action')
            account_id = request.data.get('account_id')

            if not account_id:
                return Response({'error': 'account_id required'}, status=status.HTTP_400_BAD_REQUEST)

            if action == 'request_challenge':
                challenge = generate_challenge(account_id)
                return Response({'challenge': challenge}, status=status.HTTP_200_OK)

            elif action == 'verify':
                signature = request.data.get('signature')
                user_type = request.data.get('user_type', 'tenant')
                if not signature:
                    return Response({'error': 'signature required'}, status=status.HTTP_400_BAD_REQUEST)

                result = verify_signature(account_id, signature)
                if not isinstance(result, dict) or not result.get('success'):
                    msg = result.get('message') if isinstance(result, dict) else 'verification failed'
                    return Response({'verified': False, 'message': msg}, status=status.HTTP_401_UNAUTHORIZED)

                # Ensure a Django user exists for this Hedera account
                user, _ = User.objects.get_or_create(username=account_id)

                # Issue JWT
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }

                # Attempt on-chain registration: Hedera first, then Web3 fallback
                public_key = None
                try:
                    hedera = get_hedera_client()
                    pk_res = hedera.get_account_public_key(account_id)
                    if pk_res and pk_res.get('publicKey'):
                        public_key = pk_res.get('publicKey')
                except Exception:
                    public_key = None

                # Build params for registration
                register_params = [account_id, public_key or '', user_type]

                registered = False
                try:
                    call_hedera_contract('P2PCommunity', 'registerUser', register_params)
                    registered = True
                except Exception:
                    # fallback to Web3 contract call if configured
                    try:
                        contract = get_contract('P2PCommunity')
                        tx = contract.functions.registerUser(account_id, public_key or '', user_type).transact({})
                        registered = True
                    except Exception:
                        registered = False

                return Response({'verified': True, 'tokens': tokens, 'on_chain_registered': registered}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'unknown action'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
