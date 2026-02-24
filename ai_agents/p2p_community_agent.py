"""
P2P Community Recommendation Agent
- Peer suggestions
- Trust-based recommendations
- Community insights
"""

from typing import List, Dict, Any
from datetime import datetime

class P2PCommunityAgent:
    """AI agent for peer-to-peer recommendations in the community."""
    
    def __init__(self):
        self.user_profiles: Dict[str, Dict] = {}
        self.recommendation_history: Dict[str, List[Dict]] = {}

    def register_user(self, user_id: str, user_type: str = 'tenant') -> Dict[str, Any]:
        """
        Register a new user in the P2P community.
        
        Args:
            user_id: Unique user identifier
            user_type: 'tenant' or 'landlord'
            
        Returns:
            User profile
        """
        self.user_profiles[user_id] = {
            'userId': user_id,
            'userType': user_type,
            'trustScore': 0.0,
            'rating': 0.0,
            'totalReviews': 0,
            'referralsCompleted': 0,
            'joinedAt': datetime.now().isoformat(),
            'preferences': {},
        }
        self.recommendation_history[user_id] = []
        return self.user_profiles[user_id]

    def get_tenant_recommendations(self, tenant_id: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get landlord recommendations based on tenant's preferences and community trust.
        
        Args:
            tenant_id: Tenant user ID
            limit: Number of recommendations
            
        Returns:
            Recommended landlords list
        """
        if tenant_id not in self.user_profiles:
            return {'error': 'Tenant not found'}
        
        # In production: ML model would score all landlords
        recommendations = []
        
        for user_id, profile in self.user_profiles.items():
            if profile['userType'] == 'landlord':
                score = self._calculate_recommendation_score(tenant_id, user_id)
                recommendations.append({
                    'landlordId': user_id,
                    'trustScore': profile['trustScore'],
                    'rating': profile['rating'],
                    'totalReviews': profile['totalReviews'],
                    'matchScore': score,
                })
        
        recommendations.sort(key=lambda x: x['matchScore'], reverse=True)
        
        recommendation = {
            'tenantId': tenant_id,
            'recommendations': recommendations[:limit],
            'timestamp': datetime.now().isoformat(),
        }
        
        self.recommendation_history[tenant_id].append(recommendation)
        return recommendation

    def get_landlord_recommendations(self, landlord_id: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get ideal tenant recommendations based on landlord's experience and preferences.
        
        Args:
            landlord_id: Landlord user ID
            limit: Number of recommendations
            
        Returns:
            Recommended tenants list
        """
        if landlord_id not in self.user_profiles:
            return {'error': 'Landlord not found'}
        
        recommendations = []
        
        for user_id, profile in self.user_profiles.items():
            if profile['userType'] == 'tenant':
                score = self._calculate_recommendation_score(landlord_id, user_id)
                recommendations.append({
                    'tenantId': user_id,
                    'trustScore': profile['trustScore'],
                    'rating': profile['rating'],
                    'totalReviews': profile['totalReviews'],
                    'matchScore': score,
                })
        
        recommendations.sort(key=lambda x: x['matchScore'], reverse=True)
        
        recommendation = {
            'landlordId': landlord_id,
            'recommendations': recommendations[:limit],
            'timestamp': datetime.now().isoformat(),
        }
        
        self.recommendation_history[landlord_id].append(recommendation)
        return recommendation

    def _calculate_recommendation_score(self, user_a_id: str, user_b_id: str) -> float:
        """
        Calculate recommendation score between two users.
        
        Factors:
        - Trust score (40%)
        - Rating (40%)
        - Review count (20%)
        """
        if user_b_id not in self.user_profiles:
            return 0.0
        
        profile = self.user_profiles[user_b_id]
        
        # Normalize scores
        trust_score = min(profile['trustScore'] / 100, 1.0) if profile['trustScore'] else 0.0
        rating_score = profile['rating'] / 5.0 if profile['rating'] else 0.0
        review_score = min(profile['totalReviews'] / 50, 1.0)  # Cap at 50 reviews
        
        # Weighted calculation
        final_score = (
            trust_score * 0.4 +
            rating_score * 0.4 +
            review_score * 0.2
        )
        
        return round(final_score * 100, 2)

    def get_peer_insights(self, user_id: str) -> Dict[str, Any]:
        """
        Get community insights for a user.
        """
        if user_id not in self.user_profiles:
            return {'error': 'User not found'}
        
        profile = self.user_profiles[user_id]
        
        return {
            'userId': user_id,
            'profile': profile,
            'insights': {
                'trustLevel': self._get_trust_level(profile['trustScore']),
                'receivedReviewsCount': profile['totalReviews'],
                'averageRating': profile['rating'],
                'referralProgram': {
                    'status': 'ACTIVE',
                    'successfulReferrals': profile['referralsCompleted'],
                    'earnedTokens': profile['referralsCompleted'] * 100,
                },
            },
            'recommendations': self.recommendation_history.get(user_id, [])[-5:],
        }

    def _get_trust_level(self, trust_score: float) -> str:
        """Convert trust score to level."""
        if trust_score >= 90:
            return 'PLATINUM'
        elif trust_score >= 75:
            return 'GOLD'
        elif trust_score >= 60:
            return 'SILVER'
        elif trust_score >= 45:
            return 'BRONZE'
        else:
            return 'NEW'

    def suggest_negotiation_topics(self, user1_id: str, user2_id: str) -> Dict[str, Any]:
        """
        Suggest negotiation topics for a lease based on community experience.
        """
        if user1_id not in self.user_profiles or user2_id not in self.user_profiles:
            return {'error': 'One or both users not found'}
        
        profile1 = self.user_profiles[user1_id]
        profile2 = self.user_profiles[user2_id]
        
        suggestions = []
        
        # Suggest common negotiation points based on profile types
        if profile1['userType'] == 'tenant':
            suggestions.extend([
                {
                    'topic': 'Rent Amount',
                    'rationale': 'Similar properties negotiated by others in community',
                    'confidence': 0.85,
                },
                {
                    'topic': 'Lease Duration',
                    'rationale': 'Flexibility beneficial for both parties',
                    'confidence': 0.80,
                },
                {
                    'topic': 'Maintenance Responsibilities',
                    'rationale': 'Clear terms prevent disputes',
                    'confidence': 0.90,
                },
            ])
        
        return {
            'user1Id': user1_id,
            'user2Id': user2_id,
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat(),
        }

    def get_community_stats(self) -> Dict[str, Any]:
        """Get overall community statistics."""
        total_users = len(self.user_profiles)
        tenants = [p for p in self.user_profiles.values() if p['userType'] == 'tenant']
        landlords = [p for p in self.user_profiles.values() if p['userType'] == 'landlord']
        
        avg_trust = sum(p['trustScore'] for p in self.user_profiles.values()) / total_users if total_users > 0 else 0
        avg_rating = sum(p['rating'] for p in self.user_profiles.values()) / total_users if total_users > 0 else 0
        
        return {
            'totalUsers': total_users,
            'tenants': len(tenants),
            'landlords': len(landlords),
            'averageTrustScore': round(avg_trust, 2),
            'averageRating': round(avg_rating, 2),
            'totalRecommendations': sum(len(v) for v in self.recommendation_history.values()),
        }
