# Savings-to-Own DeFi Agent
# Manages the rent-to-own mechanism: tenant pays rent, percentage goes to savings vault
# When threshold reached, tenant becomes property owner

class SavingsToOwnAgent:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.plans = {}

    def create_plan(self, property_id, target_price, monthly_rent, savings_percentage):
        """Create a rent-to-own savings plan."""
        if savings_percentage < 0 or savings_percentage > 50:
            return {'error': 'Savings percentage 0-50%'}
        
        plan = {
            'planId': len(self.plans) + 1,
            'tenantId': self.tenant_id,
            'propertyId': property_id,
            'targetPrice': target_price,
            'monthlyRent': monthly_rent,
            'savingsPercentage': savings_percentage,
            'monthlyTowardsPurchase': monthly_rent * (savings_percentage / 100),
            'monthlyToLandlord': monthly_rent * ((100 - savings_percentage) / 100),
            'savedAmount': 0,
            'totalMonths': 0,
            'status': 'ACTIVE',
            'createdAt': str(datetime.now()),
        }
        
        self.plans[plan['planId']] = plan
        return plan

    def simulate_rent_payment(self, plan_id, month_number):
        """Simulate a month of rent payment with split between landlord and savings."""
        if plan_id not in self.plans:
            return {'error': 'Plan not found'}
        
        plan = self.plans[plan_id]
        plan['totalMonths'] += 1
        plan['savedAmount'] += plan['monthlyTowardsPurchase']
        
        payment = {
            'planId': plan_id,
            'month': month_number,
            'totalRent': plan['monthlyRent'],
            'toSavings': plan['monthlyTowardsPurchase'],
            'toLandlord': plan['monthlyToLandlord'],
            'totalSaved': plan['savedAmount'],
            'progressPercent': round((plan['savedAmount'] / plan['targetPrice']) * 100, 2),
        }
        
        # Check if ownership threshold reached
        if plan['savedAmount'] >= plan['targetPrice']:
            plan['status'] = 'COMPLETED'
            payment['ownershipReady'] = True
            payment['message'] = 'Savings goal reached! Ready to convert to ownership.'
        
        return payment

    def get_plan_progress(self, plan_id):
        """Get current progress toward ownership."""
        if plan_id not in self.plans:
            return {'error': 'Plan not found'}
        
        plan = self.plans[plan_id]
        months_remaining = max(0, round((plan['targetPrice'] - plan['savedAmount']) / plan['monthlyTowardsPurchase']))
        
        return {
            'planId': plan_id,
            'propertyId': plan['propertyId'],
            'targetPrice': plan['targetPrice'],
            'savedAmount': plan['savedAmount'],
            'progressPercent': round((plan['savedAmount'] / plan['targetPrice']) * 100, 2),
            'monthsSaved': plan['totalMonths'],
            'monthsRemaining': months_remaining,
            'estimatedOwnershipDate': f'{months_remaining} months',
            'status': plan['status'],
        }

    def convert_to_ownership(self, plan_id):
        """Convert completed savings plan to property ownership."""
        if plan_id not in self.plans:
            return {'error': 'Plan not found'}
        
        plan = self.plans[plan_id]
        
        if plan['status'] != 'COMPLETED':
            return {'error': 'Plan not yet completed'}
        
        # Trigger on-chain ownership transfer
        return {
            'planId': plan_id,
            'tenantId': self.tenant_id,
            'propertyId': plan['propertyId'],
            'ownershipStatus': 'TRANSFERRING',
            'message': 'Ownership transfer initiated. Please wait for confirmation.',
            'estimatedTime': '24 hours',
        }

    def calculate_final_cost(self, plan_id):
        """Calculate total cost to tenant (lower than market price)."""
        if plan_id not in self.plans:
            return {'error': 'Plan not found'}
        
        plan = self.plans[plan_id]
        total_rent_paid = plan['monthlyRent'] * plan['totalMonths']
        savings_applied = plan['savedAmount']
        discount = savings_applied
        final_cost = plan['targetPrice'] - discount
        
        return {
            'planId': plan_id,
            'originalPrice': plan['targetPrice'],
            'totalRentPaid': round(total_rent_paid, 2),
            'savingsCredit': round(savings_applied, 2),
            'effectiveCost': round(final_cost, 2),
            'discountPercent': round((discount / plan['targetPrice']) * 100, 2),
        }

    def get_all_plans(self):
        """Get all savings plans for this tenant."""
        return {
            'tenantId': self.tenant_id,
            'plans': list(self.plans.values()),
            'activePlans': len([p for p in self.plans.values() if p['status'] == 'ACTIVE']),
            'completedPlans': len([p for p in self.plans.values() if p['status'] == 'COMPLETED']),
        }


from datetime import datetime
