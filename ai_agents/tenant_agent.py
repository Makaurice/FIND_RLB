# Tenant AI Agent (Web3 version)
# Learns preferences, recommends homes, assists with negotiation, manages savings

from backend.contracts import get_contract, call_hedera_contract
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class TenantAIAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.preferences = {}
        self.history = []
        self.model = RandomForestClassifier(n_estimators=10)
        self.trained = False
        self.property_contract = None
        self._init_contract()

    def _init_contract(self):
        try:
            self.property_contract = get_contract('PropertyNFT')
        except Exception:
            self.property_contract = None

    def learn_preferences(self, data):
        """Learn tenant preferences from interaction data."""
        self.preferences.update(data)
        self.history.append(data)
        if len(self.history) >= 3:
            self.train_model()

    def train_model(self):
        """Train ML model on historical preferences."""
        try:
            X = np.array([
                [
                    d.get('budget', 1000),
                    1 if d.get('location', '').lower() in ['nyc', 'la', 'sf'] else 0,
                    1 if d.get('property_type', '') == 'apartment' else 0,
                ]
                for d in self.history
            ])
            y = np.array([d.get('interested', 1) for d in self.history])
            if len(X) > 0:
                self.model.fit(X, y)
                self.trained = True
        except Exception:
            pass

    def fetch_properties_from_contract(self):
        """Fetch available properties (from PropertyNFT contract)."""
        # try Hedera contract call
        try:
            result = call_hedera_contract('PropertyNFT', 'getOwnerProperties', [self.user_id])
            props = result.get('result')
            if props:
                return props
        except Exception:
            pass

        if self.property_contract:
            try:
                return self.property_contract.functions.getAvailableProperties().call()
            except Exception:
                pass
        # fallback static list
        return [
            {'propertyId': 1, 'location': 'NYC', 'price': 1800, 'type': 'apartment', 'beds': 2, 'baths': 1},
            {'propertyId': 2, 'location': 'LA', 'price': 2200, 'type': 'condo', 'beds': 2, 'baths': 2},
            {'propertyId': 3, 'location': 'SF', 'price': 2500, 'type': 'apartment', 'beds': 1, 'baths': 1},
            {'propertyId': 4, 'location': 'NYC', 'price': 1500, 'type': 'studio', 'beds': 0, 'baths': 1},
        ]

    def recommend_home(self, properties=None):
        """Recommend property based on preferences and ML model."""
        if properties is None:
            properties = self.fetch_properties_from_contract()
        if not properties:
            return None

        budget = self.preferences.get('budget', 2000)

        # Filter by budget
        affordable = [p for p in properties if p.get('price', 0) <= budget]
        if not affordable:
            return min(properties, key=lambda p: p.get('price', float('inf')))

        # Use ML model if trained
        if self.trained:
            X = np.array([
                [
                    p.get('price', 0),
                    1 if p.get('location') in ['NYC', 'LA', 'SF'] else 0,
                    1 if p.get('type') == 'apartment' else 0,
                ]
                for p in affordable
            ])
            scores = self.model.predict_proba(X)[:, 1]
            best_idx = np.argmax(scores)
            return affordable[best_idx]

        # Default: return cheapest within budget
        return min(affordable, key=lambda p: p.get('price', float('inf')))

    def recommend_negotiation(self, property_data):
        """Recommend lease negotiation strategy."""
        if not property_data:
            return None
        price = property_data.get('price', 1000)
        return {
            'propertyId': property_data.get('propertyId'),
            'suggestedRent': round(price * 0.95, 2),
            'negotiationPoints': [
                'Ask for first month free',
                'Request flexible lease term',
                'Negotiate utilities inclusion',
            ],
            'leverage': 'Good rental history will help' if self.history else 'Build rental history',
        }

    def recommend_savings_plan(self, property_data):
        """Recommend a rent-to-own savings plan."""
        if not property_data:
            return None
        price = property_data.get('price', 1000)
        monthly_rent = property_data.get('price', 1000)
        savings_percentage = 10
        monthly_toward_purchase = monthly_rent * (savings_percentage / 100)
        months_to_ownership = price / monthly_toward_purchase if monthly_toward_purchase > 0 else 0
        return {
            'propertyId': property_data.get('propertyId'),
            'targetPrice': round(price, 2),
            'monthlyRent': round(monthly_rent, 2),
            'savingsPercentage': savings_percentage,
            'monthlyTowardsPurchase': round(monthly_toward_purchase, 2),
            'monthlyToLandlord': round(monthly_rent - monthly_toward_purchase, 2),
            'estimatedMonthsToOwnership': round(months_to_ownership),
            'message': f'Save {savings_percentage}% of rent. Own in ~{round(months_to_ownership)} months!',
        }

    def get_profile_summary(self):
        """Get tenant agent profile and stats."""
        return {
            'userId': self.user_id,
            'preferences': self.preferences,
            'historicalDataPoints': len(self.history),
            'modelTrained': self.trained,
            'recommendationAccuracy': 'High' if self.trained and len(self.history) > 5 else 'Learning',
        }

    def ingest_chain_data(self):
        """Fetch on-chain interaction history and incorporate into training set.

        This method pulls events such as rent payments or property views from the
        blockchain and adds them to the agent's history before retraining the
        preference model.  The contract names/functions used are placeholders and
        should be defined in the deployed smart contracts.
        """
        try:
            events = call_hedera_contract('LeaseAgreement', 'getTenantHistory', [self.user_id])
            data = events.get('result', [])
            for entry in data:
                # convert event structure to preference record
                self.history.append({
                    'budget': entry.get('budget', 0),
                    'location': entry.get('location', ''),
                    'property_type': entry.get('type', ''),
                    'interested': entry.get('interested', 1),
                })
            if len(self.history) >= 3:
                self.train_model()
        except Exception:
            pass

    def _score_property(self, prop):
        score = 0
        if prop.get('location') == self.preferences.get('location'): score += 2
        if prop.get('price', 0) <= self.preferences.get('budget', 0): score += 2
        if prop.get('type') == self.preferences.get('property_type'): score += 1
        return score
