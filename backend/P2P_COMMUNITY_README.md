# P2P Community & Referral System

The FIND P2P Community system enables tenants and landlords to build reputation, share reviews, earn rewards through referrals, and get AI-powered recommendations based on community trust.

## Core Features

### 1. Referral Program
- **Unique Referral Codes**: Generate personalized codes to share with friends
- **Reward Tracking**: Track pending and completed referrals
- **Token Rewards**: Earn 100 FIND tokens per successful referral
- **Bonus Incentives**: Receive additional rewards when referred users complete key milestones

**Backend Service**: `backend/community_service.py - CommunityService.submit_referral()`
**API Endpoints**:
- `POST /api/community/referrals/submit/` - Submit a new referral
- `POST /api/community/referrals/claim/` - Claim reward when user completes action
- `GET /api/community/referrals/stats/{user_id}/` - Get referral statistics

**Frontend Pages**: 
- `frontend/pages/tenant/referral.tsx` - Complete referral management interface

### 2. Review & Rating System
- **5-Star Reviews**: Any community member can review other users
- **Detailed Comments**: Share specific experiences and insights
- **Helpful Voting**: Community votes on review usefulness
- **Aggregate Ratings**: View average ratings and breakdowns by star level
- **Trust Building**: Reviews contribute to Trust Score calculation

**Backend Service**: `backend/community_service.py - CommunityService.submit_review()`
**API Endpoints**:
- `POST /api/community/reviews/submit/` - Submit a review
- `GET /api/community/reviews/rating/{user_id}/` - Get user rating and reviews
- `POST /api/community/reviews/help/` - Mark review as helpful/unhelpful

**Frontend Pages**:
- `frontend/pages/tenant/community-reviews.tsx` - Review submission and viewing

### 3. Community Leaderboard
- **Top Rated**: Users ranked by their average review rating
- **Most Referrals**: Active referrers with most successful invitations
- **Most Trusted**: Overall trust score combining all community metrics
- **Badges & Recognition**: Award visual badges to top contributors

**Backend Service**: `backend/community_service.py - CommunityService.get_leaderboard()`
**API Endpoints**:
- `GET /api/community/leaderboard/?category={top_rated|most_referrals|most_trusted}` - Get leaderboard

**Frontend Pages**:
- `frontend/pages/tenant/leaderboard.tsx` - Interactive leaderboard with rankings

### 4. Trust Score System
- **Holistic Score** (0-100):
  - Community Rating: 40%
  - Referral Success: 20%
  - Payment History: 30%
  - Reputation: 10%
- **5 Trust Levels**: NEW, BRONZE, SILVER, GOLD, PLATINUM
- **Score Breakdown**: See how each component contributes to total score
- **Trust Level Benefits**: Higher levels unlock better lease terms, priority matching, and rewards

**Backend Service**: `backend/community_service.py - CommunityService.get_trust_score()`
**API Endpoints**:
- `GET /api/community/trust-score/{user_id}/` - Get trust score and breakdown

**Frontend Pages**:
- `frontend/pages/tenant/trust-score.tsx` - Interactive trust score dashboard

### 5. AI-Powered Peer Recommendations
- **Tenant → Landlord Matching**: Recommend ideal landlords based on tenant preferences and community reviews
- **Landlord → Tenant Matching**: Suggest reliable tenants based on trust score and history
- **Negotiation Suggestions**: AI proposes common negotiation points based on peer experience
- **Community Insights**: Learn from peer experiences and market trends

**AI Agent**: `ai_agents/p2p_community_agent.py - P2PCommunityAgent`
**Key Methods**:
- `get_tenant_recommendations(tenant_id, limit)` - Recommend landlords for tenant
- `get_landlord_recommendations(landlord_id, limit)` - Recommend tenants for landlord
- `get_peer_insights(user_id)` - Get user's community profile and insights
- `suggest_negotiation_topics(user1_id, user2_id)` - Negotiation recommendations
- `get_community_stats()` - Overall community health metrics

**API Endpoints**:
- `GET /api/p2p/tenant/recommendations/{tenant_id}/` - Get landlord recommendations
- `GET /api/p2p/landlord/recommendations/{landlord_id}/` - Get tenant recommendations
- `GET /api/p2p/peer-insights/{user_id}/` - Get peer insights
- `GET /api/p2p/negotiation-suggestions/?user1={id}&user2={id}` - Negotiation suggestions
- `GET /api/p2p/stats/` - Community-wide statistics

## Architecture

### Backend Components

**1. `backend/community_service.py`**
- `CommunityService` class: Core community operations
- 10 main methods covering referrals, reviews, leaderboards, trust scores
- In-memory data structures for development (replace with DB in production)

**2. `ai_agents/p2p_community_agent.py`**
- `P2PCommunityAgent` class: AI-powered recommendations
- 6 main methods for tenant/landlord matching and insights
- Trust score calculation with weighted factors
- Community statistics aggregation

**3. API Views** (`backend/api/views_*.py`)
- `views_community.py`: 8 REST endpoints for referrals, reviews, leaderboards
- `views_p2p_community.py`: 5 REST endpoints for AI recommendations

**4. URL Routing** (`backend/api/urls_*.py`)
- `urls_community.py`: Routes for community endpoints
- `urls_p2p_community.py`: Routes for P2P AI endpoints

### Frontend Components

**1. Referral Management** (`frontend/pages/tenant/referral.tsx`)
- Generate unique referral codes
- Track referral status (pending/completed)
- Claim FIND token rewards
- View referral statistics

**2. Community Reviews** (`frontend/pages/tenant/community-reviews.tsx`)
- Submit detailed reviews with ratings
- View user profile with average rating
- See rating distribution breakdown
- Vote on review usefulness

**3. Leaderboard** (`frontend/pages/tenant/leaderboard.tsx`)
- Three category tabs: Top Rated, Most Referrals, Most Trusted
- Ranking badges for top 3 positions
- Real-time position updates
- User discovery and networking

**4. Trust Score** (`frontend/pages/tenant/trust-score.tsx`)
- Interactive trust score visualization
- Detailed breakdown of contributing factors
- Personalized improvement tips
- Trust level information and benefits
- Compare scores with other users

## Data Flow Examples

### Referral Flow
```
User A generates code → Shares with User B →
User B signs up with code → 
User B completes first rent payment →
User A claims reward → 
User A receives 100 FIND tokens
```

### Review & Reputation Flow
```
User A writes review → Submitted to backend →
Review stored in community database →
User B sees review on their profile →
Community votes on helpfulness →
Review influences User B's trust score →
Trust score affects future lease offers
```

### Recommendation Flow
```
Tenant A searches for landlords →
P2P Community Agent queries all landlords →
Score each by: reviews, referral success, payment history →
Rank by match score (40% trust, 40% rating, 20% reviews) →
Display top 5 recommendations to Tenant A
```

## Trust Score Calculation

```python
Trust Score = (
    (avg_rating / 5) * 40        +  # Reviews contribution
    (referrals_completed / max) * 20 +  # Referral contribution
    payment_score                  30 +  # Payment history
    reputation_score              10    # Reputation tiers
)
```

### Why Each Component Matters:
- **Rating (40%)**: Reflects how others rate your reliability and honesty
- **Referrals (20%)**: Shows your network strength and ability to bring quality members
- **Payment (30%)**: Demonstrates financial responsibility
- **Reputation (10%)**: Reflects lease compliance and community standing

## Integration with Other Systems

### AI Matching Engine
P2P recommendations feed into the main matching algorithm for:
- Better tenant-property matching
- Conflict avoidance based on past reviews
- Customized lease term recommendations

### Wallet System
Referral rewards are claimed as FIND tokens:
- `wallet_service.py`: Manages token deposits to user wallets
- Tokens can be used for fees, rent rebates, or savings

### Smart Contracts
- Trust scores stored on-chain for transparency
- Review hashes for immutable record
- Reputation tiers unlock contract features

## API Usage Examples

### Submit Referral
```bash
POST /api/community/referrals/submit/
{
  "referrerId": "user123",
  "referredUserId": "newuser456",
  "referralCode": "REF123ABC"
}
```

### Get Tenant Recommendations
```bash
GET /api/p2p/tenant/recommendations/user123/?limit=5
```

### Submit Review
```bash
POST /api/community/reviews/submit/
{
  "reviewerId": "user123",
  "targetUserId": "landlord456",
  "rating": 5,
  "comment": "Great landlord, very responsive!"
}
```

### Get Trust Score
```bash
GET /api/community/trust-score/user123/
```

### Get Leaderboard
```bash
GET /api/community/leaderboard/?category=top_rated
```

## Future Enhancements

1. **Social Features**
   - User profiles with photos and bios
   - Follow/friend system
   - Direct messaging between members
   - Public posts and discussion threads

2. **Advanced Analytics**
   - Trust score trends over time
   - Review sentiment analysis
   - Market insights from peer reviews
   - Success rate metrics

3. **Gamification**
   - Achievement badges for milestones
   - Tier progression rewards
   - Streak bonuses for on-time payments
   - Community contribution rewards

4. **Smart Contracts**
   - On-chain review attestations
   - Reputation score oracle
   - Trust-based access control for contracts
   - Automated incentive distributions

5. **Mobile Integration**
   - Push notifications for review requests
   - Referral code sharing
   - Trust score monitoring
   - Quick access to recommendations

## Database Schema (Future)

```sql
-- Users
CREATE TABLE users (
  id PRIMARY KEY,
  trust_score FLOAT,
  average_rating FLOAT,
  trust_level ENUM('NEW', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM')
);

-- Referrals
CREATE TABLE referrals (
  id PRIMARY KEY,
  referrer_id FK users,
  referred_user_id FK users,
  status ENUM('PENDING', 'COMPLETED'),
  reward_amount FLOAT,
  created_at TIMESTAMP
);

-- Reviews
CREATE TABLE reviews (
  id PRIMARY KEY,
  reviewer_id FK users,
  target_user_id FK users,
  rating INT,
  comment TEXT,
  helpful_count INT,
  unhelpful_count INT,
  created_at TIMESTAMP
);

-- Community Stats
CREATE TABLE community_stats (
  id PRIMARY KEY,
  metric TEXT,
  value FLOAT,
  recorded_at TIMESTAMP
);
```

## Performance Optimization Notes

For production deployment:
1. Cache trust scores (recalculate every 24 hours)
2. Index reviews by target_user_id for faster lookups
3. Batch referral reward claims to reduce transactions
4. Use Redis for leaderboard rankings
5. Implement pagination for large result sets (reviews, referrals)
6. Archive old reviews to archive table
7. Denormalize trust score components for faster queries

## Security Considerations

1. **Review Moderation**: Filter spam/abusive reviews
2. **Fake Referrals**: Verify referred users complete actual actions
3. **Voting Manipulation**: Rate-limit and require verified accounts
4. **Trust Score Gaming**: Monitor unusual patterns, implement caps
5. **Data Privacy**: Encrypt sensitive review content
6. **Access Control**: Only allow users to modify their own profiles
