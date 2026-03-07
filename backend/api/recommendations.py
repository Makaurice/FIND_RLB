from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ai.tenant_agent import TenantAIAgent
from property.models import Property


class RecommendationsView(APIView):
    """Provide personalized property recommendations for the authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Build recommendations using the TenantAIAgent + stored user event profile
        agent = TenantAIAgent(user_profile=user.id)

        # Load candidate properties (could be filtered based on availability, location, etc.)
        properties = list(
            Property.objects.values(
                'id',
                'owner',
                'title',
                'location',
                'property_type',
                'beds',
                'price',
                'lat',
                'lon',
                'metadataURI',
                'forRent',
                'forSale',
            )
        )

        top_k = int(request.query_params.get('k', 3))
        recommended = agent.recommend_home(properties)

        # Normalise output to list
        if recommended is None:
            recommended_list = []
        elif isinstance(recommended, list):
            recommended_list = recommended[:top_k]
        else:
            recommended_list = [recommended]

        return Response({'recommended': recommended_list})
