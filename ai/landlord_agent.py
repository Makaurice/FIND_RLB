# ai/landlord_agent.py
"""
Landlord AI Agent for FIND-RLB
Sets optimal rent, forecasts vacancy, reminders, auto-enforcement.
"""

class LandlordAIAgent:
    def __init__(self, property_profile):
        self.property_profile = property_profile

    def set_optimal_rent(self, market_data):
        # Set optimal rent as average rent plus 5% if demand is high
        avg = market_data.get('average_rent', 1000)
        demand = market_data.get('demand', 1)
        if demand > 1:
            return avg * 1.05
        return avg

    def forecast_vacancy(self, history):
        # Forecast vacancy risk as the average of the last 12 months
        if not history:
            return 0.0
        return sum(history[-12:]) / min(len(history), 12)

    def send_reminder(self, event):
        # Simulate sending a reminder
        return f"Reminder sent for {event}"

    def auto_enforce_lease(self, lease):
        # Simulate lease enforcement
        if lease.get('status') == 'breach':
            lease['status'] = 'enforced'
            return True
        return False
