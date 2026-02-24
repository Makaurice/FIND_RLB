"""
P2P Community AI Agent API Views
- Tenant recommendations
- Landlord recommendations
- Community insights
- Negotiation suggestions
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_agents.p2p_community_agent import P2PCommunityAgent

# Initialize P2P community agent
p2p_agent = P2PCommunityAgent()


class TenantRecommendationsView(APIView):
    """Get landlord recommendations for a tenant."""
    
    def get(self, request, tenant_id):
        """
        Get recommended landlords
        Query params: limit (default 5)
        """
        try:
            limit = int(request.query_params.get('limit', 5))
            
            recommendations = p2p_agent.get_tenant_recommendations(tenant_id, limit)
            
            if 'error' in recommendations:
                return Response(recommendations, status=status.HTTP_404_NOT_FOUND)
            
            return Response(recommendations, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LandlordRecommendationsView(APIView):
    """Get tenant recommendations for a landlord."""
    
    def get(self, request, landlord_id):
        """
        Get recommended tenants
        Query params: limit (default 5)
        """
        try:
            limit = int(request.query_params.get('limit', 5))
            
            recommendations = p2p_agent.get_landlord_recommendations(landlord_id, limit)
            
            if 'error' in recommendations:
                return Response(recommendations, status=status.HTTP_404_NOT_FOUND)
            
            return Response(recommendations, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PeerInsightsView(APIView):
    """Get community insights for a user."""
    
    def get(self, request, user_id):
        """Get peer insights and community profile."""
        try:
            insights = p2p_agent.get_peer_insights(user_id)
            
            if 'error' in insights:
                return Response(insights, status=status.HTTP_404_NOT_FOUND)
            
            return Response(insights, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NegotiationSuggestionsView(APIView):
    """Get negotiation topic suggestions for lease negotiations."""
    
    def get(self, request):
        """
        Get negotiation suggestions for two users
        Query params: user1, user2
        """
        try:
            user1_id = request.query_params.get('user1')
            user2_id = request.query_params.get('user2')
            
            if not user1_id or not user2_id:
                return Response(
                    {'error': 'Both user IDs required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            suggestions = p2p_agent.suggest_negotiation_topics(user1_id, user2_id)
            
            if 'error' in suggestions:
                return Response(suggestions, status=status.HTTP_404_NOT_FOUND)
            
            return Response(suggestions, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommunityStatsView(APIView):
    """Get community-wide statistics."""
    
    def get(self, request):
        """Get overall community statistics."""
        try:
            stats = p2p_agent.get_community_stats()
            return Response(stats, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
