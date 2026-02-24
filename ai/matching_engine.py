# ai/matching_engine.py
"""
Matching Engine Agent for FIND-RLB
Matches tenants & properties, predicts compatibility, uses on-chain reputation.
"""

class MatchingEngineAgent:
    def __init__(self):
        self.match_history = []

    def match(self, tenants, properties):
        # Match tenants to properties by budget (simple greedy match)
        matches = []
        for tenant in tenants:
            suitable = [p for p in properties if p.get('price', 0) <= tenant.get('budget', 0)]
            if suitable:
                matches.append((tenant, suitable[0]))
                self.match_history.append((tenant, suitable[0]))
        return matches

    def predict_compatibility(self, tenant, property_):
        # Predict compatibility based on location and type match
        score = 0.5
        if tenant.get('preferred_location') == property_.get('location'):
            score += 0.25
        if tenant.get('preferred_type') == property_.get('type'):
            score += 0.25
        return score

    def use_onchain_reputation(self, tenant):
        # Return a dummy on-chain reputation score (simulate)
        return tenant.get('onchain_reputation', 0.8)
