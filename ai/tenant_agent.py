# ai/tenant_agent.py
"""
Tenant AI Agent for FIND-RLB
Learns preferences, recommends homes, negotiation, savings plan.
"""

class TenantAIAgent:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def learn_preferences(self, data):
        # Learn preferences by updating user profile with new data
        self.user_profile.update(data)
        return self.user_profile

    def recommend_home(self, properties):
        # Recommend the property with the lowest price as a simple heuristic
        if not properties:
            return None
        return min(properties, key=lambda p: p.get('price', float('inf')))

    def suggest_negotiation(self, property_info):
        # Suggest a negotiation strategy based on price
        price = property_info.get('price', 0)
        suggested = price * 0.95
        return f"Suggest offering ${suggested:.2f} (5% below asking price)"

    def savings_plan(self, target_amount, current_savings):
        # Suggest a 12-month savings plan
        months = 12
        if target_amount <= current_savings:
            return 0
        return (target_amount - current_savings) / months
