# Matching Engine Agent
# Matches tenants & properties, predicts compatibility, uses reputation

from backend.contracts import get_contract
from sklearn.ensemble import RandomForestRegressor
import numpy as np

class MatchingEngineAgent:
    def __init__(self):
        self.model = RandomForestRegressor()
        self.trained = False

    def train_model(self, tenants, properties):
        X = np.array([[t['budget'], p['price'], t.get('reputation', 1)] for t, p in zip(tenants, properties)])
        y = np.array([t.get('interested', 1) for t in tenants])
        self.model.fit(X, y)
        self.trained = True

    def fetch_reputation_from_contract(self, tenant_id):
        contract = get_contract('Reputation')
        # Simulate fetching reputation (replace with contract call in production)
        return 5  # Example static value

    def match(self, tenants, properties):
        self.train_model(tenants, properties)
        matches = []
        for tenant in tenants:
            tenant['reputation'] = self.fetch_reputation_from_contract(tenant['id'])
            # Match to property with price <= budget
            suitable = [p for p in properties if p['price'] <= tenant['budget']]
            if suitable:
                matches.append((tenant, suitable[0]))
        return matches
                if self.trained:
                    X = np.array([[tenant['budget'], prop['price'], tenant['reputation']]])
                    score = self.model.predict(X)[0]
                else:
                    score = self.compatibility_score(tenant, prop)
                matches.append({'tenant': tenant['id'], 'property': prop['id'], 'score': score})
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches

    def get_top_matches(self, tenants, properties, n=3):
        matches = self.match(tenants, properties)
        return matches[:n]

    def compatibility_score(self, tenant, property):
        score = 0
        if property['location'] == tenant.get('location'): score += 2
        if property['price'] <= tenant.get('budget', 0): score += 2
        if property['type'] == tenant.get('property_type'): score += 1
        score += tenant.get('reputation', 0)
        return score