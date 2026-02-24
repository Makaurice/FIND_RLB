"""
FIND Token Distribution & Reward Engine
- Referral rewards
- Review incentive calculations
- Payment bonuses
- Tier-based rewards
- Automated distribution
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

class RewardEngine:
    """Engine for calculating and distributing FIND token rewards."""
    
    def __init__(self):
        self.reward_history: List[Dict] = []
        self.user_balances: Dict[str, float] = {}
        self.pending_distributions: List[Dict] = []
        
        # Reward configuration (in FIND tokens)
        self.REFERRAL_BASE_REWARD = 100.0  # Base reward per referral
        self.REFERRAL_COMMISSION = 0.05  # 5% of referred tenant's monthly rent
        self.REVIEW_MIN_REWARD = 10.0  # Minimum for short review
        self.REVIEW_MAX_REWARD = 50.0  # Maximum for excellent review
        self.PAYMENT_STREAK_REWARD = 50.0  # Reward for 12 months on-time
        self.TIER_MONTHLY_BONUS = {
            'BRONZE': 0.0,
            'SILVER': 5.0,
            'GOLD': 15.0,
            'PLATINUM': 25.0,
        }

    def calculate_referral_reward(self, referrer_id: str, referred_user_id: str, 
                                 referred_monthly_rent: float = 0) -> Dict[str, float]:
        """
        Calculate referral rewards.
        
        Args:
            referrer_id: User making the referral
            referred_user_id: New user being referred
            referred_monthly_rent: Referred user's monthly rent (for commission)
            
        Returns:
            Breakdown of immediate and ongoing rewards
        """
        # Base reward (immediate)
        immediate_reward = self.REFERRAL_BASE_REWARD
        
        # Commission reward (ongoing, monthly)
        monthly_commission = referred_monthly_rent * self.REFERRAL_COMMISSION if referred_monthly_rent > 0 else 0.0
        
        # Total first month
        first_month_total = immediate_reward + monthly_commission
        
        return {
            'referrerId': referrer_id,
            'referredUserId': referred_user_id,
            'immediateReward': immediate_reward,
            'monthlyCommission': monthly_commission,
            'firstMonthTotal': first_month_total,
            'rewardType': 'REFERRAL',
        }

    def calculate_review_reward(self, reviewer_id: str, target_user_id: str,
                               rating: float, comment_length: int) -> Dict[str, float]:
        """
        Calculate review rewards based on quality and length.
        
        Args:
            reviewer_id: User submitting review
            target_user_id: User being reviewed
            rating: Star rating (1-5)
            comment_length: Character length of review
            
        Returns:
            Reward amount with breakdown
        """
        # Base: 10 FIND for any review
        base = self.REVIEW_MIN_REWARD
        
        # Rating bonus: (rating / 5) * 10
        rating_bonus = (rating / 5.0) * 10.0
        
        # Length bonus: up to 30 FIND for detailed reviews
        max_length = 500  # Character threshold for max bonus
        length_bonus = min((comment_length / max_length) * 30.0, 30.0)
        
        # Total (capped at maximum)
        total = min(base + rating_bonus + length_bonus, self.REVIEW_MAX_REWARD)
        
        return {
            'reviewerId': reviewer_id,
            'targetUserId': target_user_id,
            'baseReward': base,
            'ratingBonus': rating_bonus,
            'lengthBonus': length_bonus,
            'totalReward': total,
            'rewardType': 'REVIEW',
        }

    def calculate_payment_bonus(self, tenant_id: str, months_on_time: int,
                               consecutive_on_time: bool = True) -> Dict[str, Any]:
        """
        Calculate bonuses for on-time payment history.
        
        Args:
            tenant_id: Tenant user ID
            months_on_time: Number of on-time payments
            consecutive_on_time: Whether payments are consecutive
            
        Returns:
            Payment bonus details
        """
        bonus_amounts = {}
        
        # Milestone bonuses
        if months_on_time >= 3 and consecutive_on_time:
            bonus_amounts['3_month'] = 10.0
        if months_on_time >= 6 and consecutive_on_time:
            bonus_amounts['6_month'] = 25.0
        if months_on_time >= 12 and consecutive_on_time:
            bonus_amounts['12_month'] = self.PAYMENT_STREAK_REWARD
        
        # Early payment bonus (if applicable)
        bonus_amounts['early_payment'] = 5.0  # Bonus if paid >3 days early
        
        total_bonus = sum(bonus_amounts.values()) if consecutive_on_time else 0.0
        
        return {
            'tenantId': tenant_id,
            'monthsOnTime': months_on_time,
            'bonusBreakdown': bonus_amounts,
            'totalBonus': total_bonus,
            'rewardType': 'PAYMENT_BONUS',
        }

    def calculate_tier_bonus(self, user_id: str, trust_level: str) -> Dict[str, Any]:
        """
        Calculate monthly bonus based on trust tier.
        
        Args:
            user_id: User ID
            trust_level: Trust tier (BRONZE, SILVER, GOLD, PLATINUM)
            
        Returns:
            Monthly tier bonus
        """
        monthly_bonus = self.TIER_MONTHLY_BONUS.get(trust_level, 0.0)
        
        return {
            'userId': user_id,
            'trustLevel': trust_level,
            'monthlyBonus': monthly_bonus,
            'description': f'{trust_level} members earn {monthly_bonus} FIND every month',
            'rewardType': 'TIER_BONUS',
        }

    def claim_reward(self, user_id: str, reward_type: str, amount: float) -> Dict[str, Any]:
        """
        Claim a reward and add to user balance.
        
        Args:
            user_id: User claiming reward
            reward_type: Type of reward (REFERRAL, REVIEW, PAYMENT_BONUS, etc)
            amount: Amount in FIND tokens
            
        Returns:
            Claim confirmation
        """
        if user_id not in self.user_balances:
            self.user_balances[user_id] = 0.0
        
        # Add to balance
        self.user_balances[user_id] += amount
        
        # Record in history
        claim_record = {
            'userId': user_id,
            'rewardType': reward_type,
            'amount': amount,
            'newBalance': self.user_balances[user_id],
            'claimedAt': datetime.now().isoformat(),
            'status': 'CLAIMED',
        }
        
        self.reward_history.append(claim_record)
        
        return claim_record

    def distribute_monthly_tier_bonuses(self, user_tier_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Distribute monthly bonuses to all users based on their tier.
        
        Args:
            user_tier_map: Dict of {user_id: tier_level}
            
        Returns:
            List of distributions
        """
        distributions = []
        
        for user_id, tier in user_tier_map.items():
            monthly_bonus = self.TIER_MONTHLY_BONUS.get(tier, 0.0)
            
            if monthly_bonus > 0:
                if user_id not in self.user_balances:
                    self.user_balances[user_id] = 0.0
                
                self.user_balances[user_id] += monthly_bonus
                
                distribution = {
                    'userId': user_id,
                    'tier': tier,
                    'amount': monthly_bonus,
                    'distributedat': datetime.now().isoformat(),
                    'reason': f'Monthly {tier} tier bonus',
                }
                
                distributions.append(distribution)
                self.reward_history.append(distribution)
        
        return distributions

    def distribute_referral_commissions(self, commission_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Distribute monthly referral commissions.
        
        Commission is 5% of referred user's rent, paid to referrer monthly.
        
        Args:
            commission_data: List of {referrer, referred, rent_amount}
            
        Returns:
            Distribution results
        """
        distributions = []
        
        for record in commission_data:
            referrer_id = record.get('referrerId')
            referred_id = record.get('referredUserId')
            rent = record.get('rentAmount', 0.0)
            
            # Calculate 5% commission
            commission = rent * self.REFERRAL_COMMISSION
            
            if commission > 0 and referrer_id:
                if referrer_id not in self.user_balances:
                    self.user_balances[referrer_id] = 0.0
                
                self.user_balances[referrer_id] += commission
                
                distribution = {
                    'referrerId': referrer_id,
                    'referredUserId': referred_id,
                    'rentAmount': rent,
                    'commissionAmount': commission,
                    'distributedAt': datetime.now().isoformat(),
                    'reason': 'Monthly referral commission (5% of rent)',
                }
                
                distributions.append(distribution)
                self.reward_history.append(distribution)
        
        return distributions

    def get_user_balance(self, user_id: str) -> float:
        """Get current FIND token balance for user."""
        return self.user_balances.get(user_id, 0.0)

    def get_user_reward_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get reward history for a user."""
        user_history = [r for r in self.reward_history if r.get('userId') == user_id or r.get('reviewerId') == user_id or r.get('tenantId') == user_id or r.get('referrerId') == user_id]
        return user_history[-limit:]

    def get_distribution_schedule(self) -> Dict[str, Any]:
        """Get reward distribution schedule."""
        return {
            'referralRewards': {
                'base': self.REFERRAL_BASE_REWARD,
                'commission': f'{self.REFERRAL_COMMISSION * 100}% of tenant rent',
                'frequency': 'Immediate + Monthly',
            },
            'reviewRewards': {
                'min': self.REVIEW_MIN_REWARD,
                'max': self.REVIEW_MAX_REWARD,
                'description': 'Varies by rating and length',
                'frequency': 'Immediate',
            },
            'paymentBonuses': {
                '3_month': 10.0,
                '6_month': 25.0,
                '12_month': self.PAYMENT_STREAK_REWARD,
                'frequency': 'At milestone',
            },
            'tierBonuses': self.TIER_MONTHLY_BONUS,
            'nextDistribution': (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1).isoformat(),
        }

    def get_leaderboard(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get top FIND token earners."""
        sorted_users = sorted(
            [(uid, balance) for uid, balance in self.user_balances.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                'rank': i + 1,
                'userId': uid,
                'totalEarnings': balance,
            }
            for i, (uid, balance) in enumerate(sorted_users[:limit])
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get reward distribution statistics."""
        if not self.reward_history:
            return {
                'totalDistributed': 0.0,
                'totalClaims': 0,
                'uniqueUsers': 0,
                'averageRewardPerUser': 0.0,
            }
        
        total_distributed = sum(r.get('amount', 0) for r in self.reward_history)
        unique_users = len(self.user_balances)
        avg_per_user = total_distributed / unique_users if unique_users > 0 else 0.0
        
        reward_breakdown = {}
        for record in self.reward_history:
            reward_type = record.get('rewardType', 'OTHER')
            if reward_type not in reward_breakdown:
                reward_breakdown[reward_type] = 0.0
            reward_breakdown[reward_type] += record.get('amount', 0)
        
        return {
            'totalDistributed': total_distributed,
            'totalClaims': len(self.reward_history),
            'uniqueUsers': unique_users,
            'averageRewardPerUser': round(avg_per_user, 2),
            'rewardBreakdown': reward_breakdown,
        }
