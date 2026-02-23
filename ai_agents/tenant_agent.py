# Tenant AI Agent
# Learns preferences, recommends homes, negotiation, savings

from backend.contracts import get_contract
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class TenantAIAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.preferences = {}
        self.history = []
        self.model = RandomForestClassifier()
        self.trained = False

    def learn_preferences(self, data):
        # data: dict with location, budget, property_type, history
        self.preferences.update(data)
        self.history.append(data)
        self.train_model()

    def train_model(self):
        if len(self.history) < 3:
            return
        X = np.array([[d['budget'], d['location'] == 'NYC', d['property_type'] == 'apartment'] for d in self.history])
        y = np.array([1 for _ in self.history])  # Dummy target
        self.model.fit(X, y)
        self.trained = True

    def fetch_properties_from_contract(self):
        contract = get_contract('PropertyNFT')
        # Example: fetch all properties
        # This would be replaced with actual contract call logic
        return [
            {'propertyId': 1, 'location': 'NYC', 'price': 1800, 'type': 'apartment'},
            {'propertyId': 2, 'location': 'LA', 'price': 2200, 'type': 'condo'}
        ]

    def recommend_home(self, properties=None):
        if properties is None:
            properties = self.fetch_properties_from_contract()
        if self.trained:
            X = np.array([[prop['price'], prop['location'] == 'NYC', prop['type'] == 'apartment'] for prop in properties])
            scores = self.model.predict_proba(X)[:, 1]
            best_idx = np.argmax(scores)
            return properties[best_idx]
        else:
            scored = [(prop, self._score_property(prop)) for prop in properties]
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[0][0] if scored else None

    def _score_property(self, prop):
        score = 0
        if prop['location'] == self.preferences.get('location'): score += 2
        if prop['price'] <= self.preferences.get('budget', 0): score += 2
        if prop['type'] == self.preferences.get('property_type'): score += 1
        return score

    def recommend_negotiation(self, property):
        # Simple negotiation strategy
        if property['price'] > self.preferences.get('budget', 0):
            return f"Offer {int(property['price']*0.95)} as negotiation."
        return "Accept listed price."

    def recommend_savings_plan(self, property):
        # Suggest savings plan to own
        price = property['price']
        budget = self.preferences.get('budget', 0)
        months = price // (budget // 2) if budget else 0
        return f"Save {budget//2} per month for {months} months to own."