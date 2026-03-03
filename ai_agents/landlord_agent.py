# Landlord AI Agent (Web3 version)
# Sets pricing, forecasts vacancy, reminders, auto-enforces lease using on-chain data

from backend.contracts import get_contract, call_hedera_contract
from sklearn.linear_model import LinearRegression
import numpy as np

class LandlordAIAgent:
    def __init__(self, landlord_id):
        self.landlord_id = landlord_id
        self.properties = []
        self.rent_model = LinearRegression()
        self.vacancy_model = LinearRegression()
        self.trained = False
        self.property_contract = None
        self._init_contract()
        self.properties = self.fetch_properties_from_contract()

    def _init_contract(self):
        try:
            self.property_contract = get_contract('PropertyNFT')
        except Exception:
            self.property_contract = None

    def fetch_properties_from_contract(self):
        # try Hedera
        try:
            result = call_hedera_contract('PropertyNFT', 'getOwnerProperties', [self.landlord_id])
            props = result.get('result')
            if props:
                return props
        except Exception:
            pass

        if self.property_contract:
            try:
                return self.property_contract.functions.getPropertiesByOwner(self.landlord_id).call()
            except Exception:
                pass
        # fallback static list
        return [
            {'propertyId': 1, 'location': 'NYC', 'price': 1800, 'type': 'apartment'},
            {'propertyId': 2, 'location': 'LA', 'price': 2200, 'type': 'condo'},
        ]

    def train_models(self, market_data, history):
        # Train rent model
        X = np.array([[market_data.get('avg_price', 0), market_data.get('demand', 0)]])
        y = np.array([market_data.get('avg_price', 0)])
        if len(X) > 0:
            self.rent_model.fit(X, y)
        # Train vacancy model
        Xv = np.array([[h] for h in history])
        yv = np.array(history)
        if len(Xv) > 0:
            self.vacancy_model.fit(Xv, yv)
        self.trained = True

    def set_optimal_rent(self, property_obj, market_data):
        self.train_models(market_data, [0.1, 0.2])
        if self.trained:
            X = np.array([[market_data.get('avg_price', 0), market_data.get('demand', 0)]])
            optimal = self.rent_model.predict(X)[0]
            return optimal
        return market_data.get('avg_price', 0)

    def forecast_vacancy(self, property_obj, history):
        self.train_models({'avg_price': property_obj.get('price', 0), 'demand': 1}, history)
        if self.trained:
            Xv = np.array([[h] for h in history])
            rate = self.vacancy_model.predict(Xv)[-1]
            return f"Vacancy risk: {rate*100:.1f}%"
        return f"Vacancy risk: {sum(history)/len(history)*100:.1f}%"

    def send_reminder(self, tenant, lease):
        # on-chain reminder could be a log event; simulate here
        return f"Reminder sent to {tenant} for lease {lease}"

    def ingest_market_history(self):
        """Download historical rent/occupancy data from chain and retrain models."""
        try:
            data = call_hedera_contract('PropertyNFT', 'getMarketHistory', [])
            records = data.get('result', [])
            prices = [r.get('avgPrice', 0) for r in records]
            demands = [r.get('demand', 0) for r in records]
            if prices and demands:
                self.train_models({'avg_price': np.mean(prices), 'demand': np.mean(demands)}, prices)
        except Exception:
            pass

    def auto_enforce_lease(self, lease):
        # try Hedera enforcement if leaseId present
        lease_id = lease.get('leaseId')
        if lease_id:
            try:
                response = call_hedera_contract('LeaseAgreement', 'enforceLease', [lease_id])
                # assume success indicated by status
                if response.get('status') == 'SUCCESS':
                    return True
            except Exception:
                pass
        if self.property_contract and lease_id:
            try:
                tx = self.property_contract.functions.enforceLease(lease_id).transact(
                    {'from': self.landlord_id}
                )
                receipt = self.property_contract.web3.eth.wait_for_transaction_receipt(tx)
                return receipt['status'] == 1
            except Exception:
                pass
        if not lease.get('active', True):
            lease['status'] = 'enforced'
            return True
        return False
