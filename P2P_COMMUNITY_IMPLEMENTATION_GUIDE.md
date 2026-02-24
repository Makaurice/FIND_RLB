# P2P Community System - Implementation Guide

## Quick Start

### Backend Setup

1. **Verify all files are created**:
   ```
   ✅ backend/community_service.py - Core referral/review/leaderboard logic
   ✅ backend/api/views_community.py - 8 REST endpoints
   ✅ backend/api/urls_community.py - URL routing for community
   ✅ ai_agents/p2p_community_agent.py - AI recommendations
   ✅ backend/api/views_p2p_community.py - 5 P2P REST endpoints
   ✅ backend/api/urls_p2p_community.py - URL routing for P2P
   ✅ backend/findrlb_django/urls.py - Main URL configuration (updated)
   ```

2. **Start Django server**:
   ```bash
   cd backend
   python manage.py runserver
   ```

3. **Test endpoints**:
   ```bash
   # Referral submission
   curl -X POST http://localhost:8000/api/community/referrals/submit/ \
     -H "Content-Type: application/json" \
     -d '{
       "referrerId": "user123",
       "referredUserId": "user456",
       "referralCode": "REF123ABC"
     }'

   # Get recommendations
   curl http://localhost:8000/api/p2p/tenant/recommendations/user123/?limit=5

   # Get leaderboard
   curl http://localhost:8000/api/community/leaderboard/?category=top_rated
   ```

### Frontend Setup

1. **Verify all pages are created**:
   ```
   ✅ frontend/pages/tenant/referral.tsx - Referral management
   ✅ frontend/pages/tenant/community-reviews.tsx - Review system
   ✅ frontend/pages/tenant/leaderboard.tsx - Leaderboard
   ✅ frontend/pages/tenant/trust-score.tsx - Trust score dashboard
   ```

2. **Add navigation links** in `frontend/pages/tenant.tsx`:
   ```typescript
   const features = [
     { name: 'Dashboard', href: '/tenant/dashboard' },
     { name: 'Referrals', href: '/tenant/referral' },
     { name: 'Reviews', href: '/tenant/community-reviews' },
     { name: 'Leaderboard', href: '/tenant/leaderboard' },
     { name: 'Trust Score', href: '/tenant/trust-score' },
     // ... other features
   ];
   ```

3. **Start Next.js dev server**:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Navigate to pages**:
   - http://localhost:3000/tenant/referral
   - http://localhost:3000/tenant/community-reviews
   - http://localhost:3000/tenant/leaderboard
   - http://localhost:3000/tenant/trust-score

## API Endpoint Reference

### Referral System
```
POST   /api/community/referrals/submit/        - Submit referral
POST   /api/community/referrals/claim/         - Claim reward
GET    /api/community/referrals/stats/{uid}/   - Get stats
```

### Review System
```
POST   /api/community/reviews/submit/          - Submit review
GET    /api/community/reviews/rating/{uid}/    - Get user rating
POST   /api/community/reviews/help/            - Mark helpful
```

### Community Features
```
GET    /api/community/leaderboard/             - Get leaderboard
GET    /api/community/trust-score/{uid}/       - Get trust score
```

### P2P Recommendations
```
GET    /api/p2p/tenant/recommendations/{uid}/   - Landlord recommendations
GET    /api/p2p/landlord/recommendations/{uid}/ - Tenant recommendations
GET    /api/p2p/peer-insights/{uid}/            - Peer insights
GET    /api/p2p/negotiation-suggestions/        - Negotiation tips
GET    /api/p2p/stats/                          - Community stats
```

## Feature Implementation Status

### ✅ Complete Features
1. **Referral Program**
   - Generate unique codes
   - Track pending/completed referrals
   - Claim 100 FIND token rewards
   - View referral statistics

2. **Review System**
   - Submit 5-star reviews with comments
   - View aggregate ratings
   - See rating breakdown (5★, 4★, 3★, 2★, 1★)
   - Vote on review helpfulness

3. **Leaderboard**
   - Top Rated users by average rating
   - Most Referrals by successful invitations
   - Most Trusted by overall score
   - Award badges for top 3 positions

4. **Trust Score**
   - Holistic 0-100 score
   - Five trust levels: NEW, BRONZE, SILVER, GOLD, PLATINUM
   - Detailed breakdown: Rating (40%), Referrals (20%), Payment (30%), Reputation (10%)
   - Personalized improvement tips

5. **AI Recommendations**
   - Tenant → Landlord matching
   - Landlord → Tenant matching
   - Negotiation topic suggestions
   - Community insights and statistics

### 🔄 Pending Integration
1. **Hedera Smart Contracts**
   - Store trust scores on-chain
   - Immutable review attestations
   - Reputation tier enforcement

2. **Database Persistence**
   - Replace in-memory storage with PostgreSQL
   - User profile tables
   - Review/referral history
   - Trust score snapshots

3. **Advanced Analytics**
   - Trust score trends
   - Sentiment analysis for reviews
   - Market insights
   - Success rate metrics

## Testing the System

### 1. Test Referral Flow
```python
# Generate code manually or use UI
code = "REF123ABC"

# Submit referral
POST /api/community/referrals/submit/
{
  "referrerId": "alice@example.com",
  "referredUserId": "bob@example.com",
  "referralCode": code
}

# Claim reward when bob completes action
POST /api/community/referrals/claim/
{
  "referrerId": "alice@example.com",
  "referredUserId": "bob@example.com"
}

# Check stats
GET /api/community/referrals/stats/alice@example.com/
# Returns:
# {
#   "totalReferrals": 1,
#   "completedReferrals": 1,
#   "pendingReferrals": 0,
#   "totalEarnings": 100.0
# }
```

### 2. Test Review System
```python
# Submit review
POST /api/community/reviews/submit/
{
  "reviewerId": "alice@example.com",
  "targetUserId": "landlord123@example.com",
  "rating": 5,
  "comment": "Excellent landlord, very responsive to maintenance requests"
}

# Get user rating
GET /api/community/reviews/rating/landlord123@example.com/
# Shows: averageRating: 5.0, reviews: [review_data], ratingBreakdown: {5: 1, 4: 0, ...}

# Mark review helpful
POST /api/community/reviews/help/
{
  "reviewId": 1,
  "targetUserId": "landlord123@example.com",
  "helpful": true
}
```

### 3. Test Leaderboard
```python
# Populate with sample data
# (Note: In development, create users first)

# Get top rated users
GET /api/community/leaderboard/?category=top_rated
# Returns: [{rank: 1, userId: "landlord123", rating: 4.9}, ...]

# Get most referrals
GET /api/community/leaderboard/?category=most_referrals
# Returns: [{rank: 1, userId: "alice", referrals: 15}, ...]

# Get most trusted
GET /api/community/leaderboard/?category=most_trusted
# Returns: [{rank: 1, userId: "alice", trustScore: 98.5}, ...]
```

### 4. Test AI Recommendations
```python
# Get recommendations for tenant
GET /api/p2p/tenant/recommendations/alice@example.com/?limit=5
# Returns: 5 recommended landlords sorted by matchScore

# Get recommendations for landlord
GET /api/p2p/landlord/recommendations/landlord123@example.com/?limit=5
# Returns: 5 recommended tenants sorted by matchScore

# Get peer insights
GET /api/p2p/peer-insights/alice@example.com/
# Returns: Trust level, reviews, referrals, insights

# Get negotiation suggestions
GET /api/p2p/negotiation-suggestions/?user1=alice@example.com&user2=landlord123@example.com
# Returns: Topics to discuss during lease negotiation
```

## Data Model Examples

### User Profile (In-Memory)
```python
{
  'userId': 'alice@example.com',
  'trustScore': 85.5,
  'rating': 4.8,
  'totalReviews': 12,
  'referralsCompleted': 5,
  'joinedAt': '2024-01-15T10:00:00',
}
```

### Referral Record
```python
{
  'referrerId': 'alice@example.com',
  'referredUserId': 'bob@example.com',
  'referralCode': 'REF123ABC',
  'status': 'PENDING',  # or 'COMPLETED'
  'completionRewardWaiting': 100.0,
  'createdAt': '2024-01-20T14:30:00',
}
```

### Review Record
```python
{
  'reviewId': 1,
  'reviewerId': 'alice@example.com',
  'targetUserId': 'landlord123@example.com',
  'rating': 5,
  'comment': 'Great landlord...',
  'createdAt': '2024-01-21T10:00:00',
  'helpful': 3,
  'unhelpful': 0,
}
```

### Leaderboard Entry
```python
{
  'rank': 1,
  'userId': 'landlord123@example.com',
  'rating': 4.95,  # or 'referrals': 25 or 'trustScore': 95.5
}
```

### Trust Score Record
```python
{
  'userId': 'alice@example.com',
  'trustScore': 85.5,
  'breakdown': {
    'ratingScore': 36.0,    # (4.8/5) * 40
    'referralScore': 15.0,  # (5/25) * 20
    'paymentScore': 25.5,   # based on history
    'reputationScore': 9.0, # based on tiers
  },
  'trustLevel': 'GOLD',
}
```

## Integration Checklist

- [ ] Run Django server with all endpoints
- [ ] Test all 13 API endpoints directly
- [ ] Navigate all 4 frontend pages in browser
- [ ] Submit sample referrals and verify rewards
- [ ] Submit sample reviews and check leaderboard
- [ ] Calculate trust scores for test users
- [ ] Request recommendations for multiple users
- [ ] Verify premium color scheme on all pages
- [ ] Test error handling with invalid inputs
- [ ] Check response formats match API docs
- [ ] Document any edge cases found
- [ ] Prepare for database migration

## Next Steps

1. **Database Migration** (~2 hours)
   - Create Django models for users, referrals, reviews
   - Create migrations and apply
   - Migrate in-memory data to database

2. **Hedera Integration** (~3 hours)
   - Store trust scores on-chain
   - Create review attestation contract
   - Link web3 calls to endpoints

3. **Advanced Features** (~4 hours)
   - Add sentiment analysis for reviews
   - Implement trust score trending
   - Build recommendation ML model
   - Create gamification badges

4. **Frontend Enhancements** (~2 hours)
   - Add loading states to all pages
   - Implement real-time leaderboard updates
   - Add user profile views
   - Create notification system for new reviews

5. **Testing & Deployment** (~2 hours)
   - Write unit tests for services
   - Write integration tests for APIs
   - Load testing for leaderboards
   - Deploy to staging environment

## Support & Documentation

- Full P2P Community documentation: `backend/P2P_COMMUNITY_README.md`
- AI Agent reference: See docstrings in `ai_agents/p2p_community_agent.py`
- API test examples included above
- Frontend component examples in created .tsx files

## Performance Notes

Current implementation uses in-memory storage suitable for:
- Development and testing
- Prototype demonstrations
- Single-server deployments (<1000 users)

For production (1000+ users):
1. Migrate to PostgreSQL with proper indexing
2. Implement Redis caching for leaderboards
3. Use async tasks for recommendation calculation
4. Add pagination to all list endpoints
5. Archive old reviews to separate table
6. Implement rate limiting on API endpoints
7. Add monitoring and alerting for anomalies
