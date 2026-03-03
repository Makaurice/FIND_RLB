# Matching Engine Agent (Web3-enhanced)
# Matches tenants & properties, predicts compatibility, uses on-chain reputation

from backend.contracts import get_contract, call_hedera_contract
from sklearn.ensemble import RandomForestRegressor
import numpy as np

class MatchingEngineAgent:
    def __init__(self):
        self.model = RandomForestRegressor()
        self.trained = False
        # try to initialise optional Web3 handle
        try:
            self.reputation_contract = get_contract('Reputation')
        except Exception:
            self.reputation_contract = None

    def train_model(self, tenants, properties):
        X = np.array([[t['budget'], p['price'], t.get('reputation', 1)] for t, p in zip(tenants, properties)])
        y = np.array([t.get('interested', 1) for t in tenants])
        if len(X) > 0:
            self.model.fit(X, y)
            self.trained = True

    def fetch_reputation_from_contract(self, tenant_id):
        # try Hedera first
        try:
            res = call_hedera_contract('Reputation', 'getReputation', [tenant_id])
            # assume result contains numeric reputation
            if isinstance(res, dict) and 'result' in res:
                return res['result']
        except Exception:
            pass

        if self.reputation_contract:
            try:
                return self.reputation_contract.functions.getReputation(tenant_id).call()
            except Exception:
                pass
        # fallback static score
        return 5

    def match(self, tenants, properties):
        # ensure reputation data is up to date, then score
        for tenant in tenants:
            tenant['reputation'] = self.fetch_reputation_from_contract(tenant.get('id'))
        self.train_model(tenants, properties)

        matches = []
        for tenant in tenants:
            suitable = [p for p in properties if p.get('price', 0) <= tenant.get('budget', 0)]
            for prop in suitable:
                if self.trained:
                    X = np.array([[tenant['budget'], prop['price'], tenant['reputation']]])
                    score = self.model.predict(X)[0]
                else:
                    score = self.compatibility_score(tenant, prop)
                matches.append({'tenant': tenant.get('id'), 'property': prop.get('id'), 'score': score})
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches

    def get_top_matches(self, tenants, properties, n=3):
        matches = self.match(tenants, properties)
        return matches[:n]

    def ingest_chain_feedback(self):
        """Pull on-chain match/feedback records to improve the model."""
        try:
            feedback = call_hedera_contract('MatchingEngine', 'getTenantFeedback', [])
            records = feedback.get('result', [])
            # convert feedback entries into training examples
            for rec in records:
                tenants.append({'budget': rec.get('budget'), 'reputation': rec.get('reputation'), 'id': rec.get('tenantId')})
                properties.append({'price': rec.get('price'), 'id': rec.get('propertyId')})
            if tenants and properties:
                self.train_model(tenants, properties)
        except Exception:
            pass

    def compatibility_score(self, tenant, property):
        score = 0
        if property.get('location') == tenant.get('location'): score += 2
        if property.get('price', 0) <= tenant.get('budget', 0): score += 2
        if property.get('type') == tenant.get('property_type'): score += 1
        score += tenant.get('reputation', 0)
        return score