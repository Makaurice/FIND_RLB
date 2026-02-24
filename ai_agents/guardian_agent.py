# Guardian/Sponsor AI Agent
# Manages third-party rent payments (father paying son's rent, investor backing tenant, etc.)

class GuardianAIAgent:
    def __init__(self, guardian_id):
        self.guardian_id = guardian_id
        self.sponsored_tenants = []
        self.payment_limits = {}
        self.monthly_budget = 0

    def register_tenant(self, tenant_id, max_monthly_support):
        """Register a tenant under this guardian's sponsorship."""
        self.sponsored_tenants.append(tenant_id)
        self.payment_limits[tenant_id] = max_monthly_support
        return {
            'guardianId': self.guardian_id,
            'tenantId': tenant_id,
            'monthlyLimit': max_monthly_support,
            'status': 'REGISTERED',
        }

    def set_budget(self, total_monthly):
        """Set total monthly budget for all sponsored tenants."""
        self.monthly_budget = total_monthly
        return {
            'guardianId': self.guardian_id,
            'totalBudget': total_monthly,
            'status': 'UPDATED',
        }

    def authorize_payment(self, tenant_id, lease_id, amount):
        """Authorize a rent payment on behalf of a tenant."""
        if tenant_id not in self.sponsored_tenants:
            return {'error': 'Tenant not registered under this guardian'}
        
        limit = self.payment_limits.get(tenant_id, 0)
        if amount > limit:
            return {'error': f'Amount exceeds limit of {limit}'}
        
        return {
            'guardianId': self.guardian_id,
            'tenantId': tenant_id,
            'leaseId': lease_id,
            'amount': amount,
            'authorized': True,
            'method': 'ON_CHAIN_ESCROW',
        }

    def set_payment_schedule(self, tenant_id, schedule_type):
        """Set automatic payment schedule (daily, weekly, monthly)."""
        if tenant_id not in self.sponsored_tenants:
            return {'error': 'Tenant not registered'}
        
        return {
            'tenantId': tenant_id,
            'scheduleType': schedule_type,
            'active': True,
        }

    def get_payment_history(self, tenant_id):
        """Get payment history for a sponsored tenant."""
        return {
            'tenantId': tenant_id,
            'guardianId': self.guardian_id,
            'payments': [
                {'date': '2026-02-01', 'amount': 1200, 'status': 'paid'},
                {'date': '2026-01-01', 'amount': 1200, 'status': 'paid'},
            ],
            'totalPaid': 2400,
        }

    def get_balance_summary(self):
        """Get overall balance and spending summary."""
        return {
            'guardianId': self.guardian_id,
            'totalBudget': self.monthly_budget,
            'sponsoredTenants': len(self.sponsored_tenants),
            'tenants': self.sponsored_tenants,
        }
