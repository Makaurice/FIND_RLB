# Moving Service AI Agent
# Manages moving service quotes, scheduling, and autonomous pricing based on demand/supply

import random
from datetime import datetime, timedelta

class MovingServiceAgent:
    def __init__(self, service_provider_id):
        self.provider_id = service_provider_id
        self.base_price_per_mile = 2.0  # $/mile
        self.base_hourly_rate = 50.0  # $/hour
        self.available_trucks = {'small': 3, 'medium': 2, 'large': 1}
        self.bookings = []
        self.demand_multiplier = 1.0  # Dynamic pricing

    def get_quote(self, moving_data):
        """Generate dynamic quote based on distance, items, time, and demand."""
        distance = moving_data.get('distance', 10)
        items_weight = moving_data.get('items_weight', 1000)  # kg
        moving_date = moving_data.get('moving_date')
        truck_type = moving_data.get('truck_type', 'medium')
        
        # Estimate time (0.5 hours per 1000kg)
        hours = max(2, items_weight / 1000 * 0.5)
        
        # Base cost
        distance_cost = distance * self.base_price_per_mile
        hourly_cost = hours * self.base_hourly_rate
        base_total = distance_cost + hourly_cost
        
        # Apply truck size premium
        truck_premiums = {'small': 0.8, 'medium': 1.0, 'large': 1.3}
        base_total *= truck_premiums.get(truck_type, 1.0)
        
        # Apply demand multiplier (surge pricing)
        final_total = base_total * self.demand_multiplier
        
        # Calculate breakdown
        quote = {
            'providerId': self.provider_id,
            'quoteId': random.randint(10000, 99999),
            'distance': distance,
            'hours': round(hours, 1),
            'truckType': truck_type,
            'distanceCost': round(distance_cost, 2),
            'hourlyCost': round(hourly_cost, 2),
            'subtotal': round(base_total, 2),
            'demandMultiplier': round(self.demand_multiplier, 2),
            'total': round(final_total, 2),
            'currency': 'USD',
            'validUntil': (datetime.now() + timedelta(days=7)).isoformat(),
        }
        return quote

    def book_moving(self, quote_id, customer_id, moving_date, truck_type):
        """Book a moving service."""
        if self.available_trucks.get(truck_type, 0) <= 0:
            return {'error': f'No {truck_type} trucks available'}
        
        booking = {
            'bookingId': random.randint(100000, 999999),
            'quoteId': quote_id,
            'customerId': customer_id,
            'providerId': self.provider_id,
            'movingDate': moving_date,
            'truckType': truck_type,
            'status': 'CONFIRMED',
            'paymentStatus': 'PENDING',
            'bookedAt': datetime.now().isoformat(),
        }
        
        # Reserve truck
        self.available_trucks[truck_type] -= 1
        self.bookings.append(booking)
        
        # Adjust demand multiplier based on occupancy
        self._update_demand_multiplier()
        
        return booking

    def _update_demand_multiplier(self):
        """Dynamically adjust pricing based on truck utilization."""
        total_trucks = sum(self.available_trucks.values())
        total_capacity = 6  # 3 small + 2 medium + 1 large
        utilization = (total_capacity - total_trucks) / total_capacity
        
        # Demand multiplier ranges from 0.9 (low demand) to 1.5 (high demand)
        if utilization > 0.8:
            self.demand_multiplier = 1.5
        elif utilization > 0.6:
            self.demand_multiplier = 1.2
        elif utilization > 0.4:
            self.demand_multiplier = 1.0
        else:
            self.demand_multiplier = 0.9

    def get_available_trucks(self):
        """Get current truck availability."""
        return {
            'providerId': self.provider_id,
            'available': self.available_trucks,
            'demandMultiplier': round(self.demand_multiplier, 2),
        }

    def get_booking_status(self, booking_id):
        """Get status of a booking."""
        for booking in self.bookings:
            if booking['bookingId'] == booking_id:
                return booking
        return {'error': 'Booking not found'}

    def complete_booking(self, booking_id, actual_hours, actual_distance):
        """Mark booking as complete and bill customer."""
        for booking in self.bookings:
            if booking['bookingId'] == booking_id:
                # Calculate actual cost
                actual_cost = (actual_distance * self.base_price_per_mile + 
                             actual_hours * self.base_hourly_rate)
                
                booking['status'] = 'COMPLETED'
                booking['paymentStatus'] = 'PROCESSING'
                booking['actualCost'] = round(actual_cost, 2)
                booking['completedAt'] = datetime.now().isoformat()
                
                # Release truck
                self.available_trucks[booking['truckType']] += 1
                self._update_demand_multiplier()
                
                return booking
        
        return {'error': 'Booking not found'}
