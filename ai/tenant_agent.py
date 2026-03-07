# ai/tenant_agent.py
"""
Tenant AI Agent for FIND-RLB
Learns preferences, recommends homes, negotiation, savings plan.
"""

from typing import Any, Dict, List, Optional

from data_science.recommender import PropertyRecommender


class TenantAIAgent:
    def __init__(
        self,
        user_profile: Any = None,
        recommender: Optional[PropertyRecommender] = None,
    ):
        """Create a tenant agent.

        Args:
            user_profile: Either a preference dict or a user id for which preferences should be built.
            recommender: Optional recommender instance; if not provided, a default is created.
        """
        # If an integer/string is provided, treat it as a user identifier and build a profile.
        if isinstance(user_profile, (int, str)):
            try:
                from data_science.user_profile import build_user_profile

                user_profile = build_user_profile(user_profile)
            except Exception:
                user_profile = {}

        self.user_profile = user_profile or {}
        self.recommender = recommender or PropertyRecommender()

    def learn_preferences(self, data: Dict):
        # Learn preferences by updating user profile with new data
        self.user_profile.update(data)
        return self.user_profile

    def recommend_home(self, properties: List[Dict]):
        # Recommend using a trained recommender if available, else fall back to simple heuristic
        if not properties:
            return None

        if self.recommender:
            try:
                recommendations = self.recommender.recommend(self.user_profile, properties, k=1)
                if recommendations:
                    return recommendations[0]
            except Exception:
                # Keep fallback behavior if recommender fails
                pass

        return min(properties, key=lambda p: p.get('price', float('inf')))

    def suggest_negotiation(self, property_info: Dict):
        # Suggest a negotiation strategy based on price
        price = property_info.get('price', 0)
        suggested = price * 0.95
        return f"Suggest offering ${suggested:.2f} (5% below asking price)"

    # Backwards compatibility wrappers used by existing API endpoints
    def recommend_negotiation(self, property_info: Dict):
        return self.suggest_negotiation(property_info)

    def savings_plan(self, target_amount: float, current_savings: float):
        # Suggest a 12-month savings plan
        months = 12
        if target_amount <= current_savings:
            return 0
        return (target_amount - current_savings) / months

    def recommend_savings_plan(self, preferred_property: Dict):
        # Use user profile savings if available
        target_price = preferred_property.get('price', 0)
        current_savings = self.user_profile.get('savings', 0)
        return self.savings_plan(target_price, current_savings)
