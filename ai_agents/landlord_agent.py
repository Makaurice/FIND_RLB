# Landlord AI Agent
# Sets pricing, forecasts vacancy, reminders, auto-enforces lease

from backend.contracts import get_contract
from sklearn.linear_model import LinearRegression
import numpy as np

class LandlordAIAgent:
    def __init__(self, landlord_id):
        self.landlord_id = landlord_id
        self.properties = self.fetch_properties_from_contract()
        self.rent_model = LinearRegression()
        self.vacancy_model = LinearRegression()
        self.trained = False

    def fetch_properties_from_contract(self):
        contract = get_contract('PropertyNFT')
        # Example: fetch properties owned by landlord
        # Replace with actual contract call
        return [
            {'propertyId': 1, 'location': 'NYC', 'price': 1800, 'type': 'apartment'},
            {'propertyId': 2, 'location': 'LA', 'price': 2200, 'type': 'condo'}
        ]

    def train_models(self, market_data, history):
        # Train rent model
        X = np.array([[market_data['avg_price'], market_data['demand']]])
        y = np.array([market_data['avg_price']])
        self.rent_model.fit(X, y)
        # Train vacancy model
        Xv = np.array([[h] for h in history])
        yv = np.array(history)
        self.vacancy_model.fit(Xv, yv)
        self.trained = True

    def set_optimal_rent(self, property, market_data):
        self.train_models(market_data, [0.1, 0.2])
        if self.trained:
            X = np.array([[market_data['avg_price'], market_data['demand']]])
            optimal = self.rent_model.predict(X)[0]
            return optimal
        return market_data['avg_price']

    def forecast_vacancy(self, property, history):
        self.train_models({'avg_price': property['price'], 'demand': 1}, history)
        if self.trained:
            Xv = np.array([[h] for h in history])
            rate = self.vacancy_model.predict(Xv)[-1]
            return f"Vacancy risk: {rate*100:.1f}%"
        return f"Vacancy risk: {sum(history)/len(history)*100:.1f}%"

    def send_reminder(self, tenant, lease):
        return f"Reminder sent to {tenant} for lease {lease}"

    def auto_enforce_lease(self, lease):
        # Use LeaseAgreement contract for enforcement
        contract = get_contract('LeaseAgreement')
        # Example: check lease status
        # Replace with actual contract call
        if not lease['active']:
            return "Lease terminated automatically."
        return "Lease active and enforced."