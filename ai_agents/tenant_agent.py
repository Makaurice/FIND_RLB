# Tenant AI Agent
# Learns preferences, recommends homes, assists with negotiation, manages savings

from backend.contracts import get_contract
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class TenantAIAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.preferences = {}
        self.history = []
        self.model = RandomForestClassifier(n_estimators=10)
        self.trained = False

    def learn_preferences(self, data):
        """Learn tenant preferences from interaction data."""
        # data: dict with location, budget, property_type, history
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
                    1 if d.get('property_type', '') == 'apartment' else 0
                ]
                for d in self.history
            ])
            y = np.array([d.get('interested', 1) for d in self.history])
            self.model.fit(X, y)
            self.trained = True
        except:
            pass  # Model training failed, continue with defaults

    def fetch_properties_from_contract(self):
        """Fetch available properties (from PropertyNFT contract in production)."""
        # In production: contract = get_contract('PropertyNFT')
        # properties = contract.functions.getAvailableProperties().call()
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
        preferred_location = self.preferences.get('location', '')
        
        # Filter by budget
        affordable = [p for p in properties if p.get('price', 0) <= budget]
        
        if not affordable:
            return min(properties, key=lambda p: p.get('price', float('inf')))
        
        # Use ML model if trained
        if self.trained:
            X = np.array([[p.get('price', 0), 1 if p.get('location') in ['NYC', 'LA', 'SF'] else 0, 
                          1 if p.get('type') == 'apartment' else 0] for p in affordable])
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
            'suggestedRent': round(price * 0.95, 2),  # Suggest 5% discount
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
        
        # Recommend saving 10% of rent toward ownership
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