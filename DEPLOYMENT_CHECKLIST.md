# FIND-RLB: Production Deployment Checklist

**Status:** Ready for Deployment  
**Last Updated:** February 24, 2026  
**Target Environment:** Staging → Production

---

## 🚀 Pre-Deployment Phase (Days 1-2)

### Backend Preparation
- [ ] **environment.py** - Create production settings file
  ```bash
  Copy: backend/findrlb_django/settings.py
  Edit: DEBUG=False, ALLOWED_HOSTS, DATABASES
  Add: Email backend, logging configuration
  ```

- [ ] **requirements.txt** - Verify all packages
  ```bash
  pip install -r requirements.txt
  pip check  # Verify no conflicts
  ```

- [ ] **Database Setup** - Create production database
  ```bash
  createdb find_rlb_prod
  pg_restore < find_rlb_backup.sql
  ```

- [ ] **Environment Variables** - Configure .env
  ```
  SECRET_KEY=*generate new*
  DEBUG=False
  ALLOWED_HOSTS=yourdomain.com
  DATABASE_URL=postgresql://user:pass@host:5432/find_rlb_prod
  HEDERA_ACCOUNT_ID=0.0.xxxxx
  HEDERA_PRIVATE_KEY=*copy from Hedera portal*
  HEDERA_NETWORK=testnet (or mainnet)
  ```

- [ ] **Database Migrations** - Apply all migrations
  ```bash
  python manage.py migrate
  python manage.py createsuperuser
  ```

- [ ] **Static Files** - Collect static assets
  ```bash
  python manage.py collectstatic --no-input
  ```

### Frontend Preparation
- [ ] **Environment Configuration** - Create .env.production
  ```
  NEXT_PUBLIC_API_URL=https://api.yourdomain.com
  NEXT_PUBLIC_HEDERA_NETWORK=testnet
  ```

- [ ] **Build Optimization** - Test production build
  ```bash
  npm run build
  npm run analyze  # Check bundle size
  ```

- [ ] **Performance** - Verify metrics
  ```
  First Contentful Paint: < 1.5s
  Time to Interactive: < 2s
  Lighthouse Score: > 90
  ```

### Blockchain Preparation
- [ ] **Hedera Account Setup**
  ```
  1. Go to https://portal.hedera.com
  2. Create testnet account
  3. Export account ID & private key
  4. Add to environment variables
  5. Get testnet HBAR for fees (~10 HBAR)
  ```

- [ ] **Smart Contracts** - Deploy to Hedera testnet
  ```bash
  # For each contract:
  1. Compile: solc contract.sol
  2. Deploy: hedera_integration_v2.deploy_contract()
  3. Save contract ID
  4. Update views with contract ID
  5. Test with sample transaction
  ```

- [ ] **Token Creation** - Create FIND token on Hedera
  ```
  1. Use hedera_integration_v2.create_token()
  2. Symbol: FIND
  3. Initial supply: 1,000,000,000
  4. Decimals: 2
  5. Save token ID: 0.0.xxxxx
  6. Add to settings
  ```

---

## 📊 Staging Deployment Phase (Days 3-7)

### Backend Deployment
- [ ] **Code Deployment**
  ```bash
  # If using Docker:
  docker build -t find-rlb-backend .
  docker run -d --env-file .env find-rlb-backend
  
  # If using direct server:
  git clone repo
  cd backend
  source venv/bin/activate
  pip install -r requirements.txt
  gunicorn findrlb_django.wsgi
  ```

- [ ] **Web Server Setup** - Configure Nginx/Apache
  ```
  - Proxy requests to Django (port 8000)
  - Serve static files directly
  - Enable SSL/TLS certificates (Let's Encrypt)
  - Configure CORS headers
  - Set up compression (gzip)
  ```

- [ ] **Database Backup** - Setup automated backups
  ```bash
  # Daily at 2 AM UTC
  0 2 * * * pg_dump find_rlb_prod | gzip > /backups/find_rlb_$(date +\%Y\%m\%d).sql.gz
  ```

- [ ] **Logging Setup** - Configure application logging
  ```
  - Application logs: /var/log/find_rlb/app.log
  - Access logs: /var/log/find_rlb/access.log
  - Error logs: /var/log/find_rlb/error.log
  - Log rotation: daily, 30-day retention
  ```

### Frontend Deployment
- [ ] **Code Deployment**
  ```bash
  # If using Vercel:
  npm install -g vercel
  vercel --prod
  
  # If using self-hosted:
  npm run build
  npm install -g pm2
  pm2 start "npm start" --name "find-rlb-frontend"
  ```

- [ ] **CDN Configuration** - Setup content delivery
  ```
  - CloudFlare or Cloudfront
  - Bucket: /public folder
  - Cache: 24 hours for static assets
  - Purge: on new deployment
  ```

- [ ] **Domain Setup**
  ```
  - DNS A record: points to server IP
  - CNAME: www → main domain
  - SSL certificate: auto-renew enabled
  - DNSSEC: enabled
  ```

### Monitoring Setup
- [ ] **Application Monitoring**
  ```bash
  # Install Sentry (error tracking)
  pip install sentry-sdk
  import sentry_sdk
  sentry_sdk.init("your-sentry-dsn")
  
  # Install New Relic (performance)
  pip install newrelic
  newrelic-admin run-program gunicorn ...
  ```

- [ ] **Server Monitoring**
  ```
  - CPU usage: alert if > 80%
  - Memory: alert if > 85%
  - Disk: alert if > 90%
  - Network: monitor latency
  - Database: monitor connections
  ```

- [ ] **Uptime Monitoring**
  ```
  - Ping monitoring every 5 minutes
  - API health checks
  - Database connectivity
  - Blockchain node queries
  - Slack/email alerts enabled
  ```

### Testing in Staging
- [ ] **Smoke Tests** (Critical paths)
  ```
  ✓ User registration flow
  ✓ Login with JWT tokens
  ✓ Create lease agreement
  ✓ Make payment (HBAR transfer)
  ✓ Get FIND rewards
  ✓ View leaderboard
  ```

- [ ] **API Tests** (All 28 endpoints)
  ```bash
  pytest backend/tests/
  Coverage target: 85%+
  ```

- [ ] **Load Tests** (Simulate 1000 users)
  ```bash
  locust -f locustfile.py --host=https://staging.yourdomain.com
  - Target: 1000 concurrent users
  - Ramp-up: 10 users/second
  - Duration: 10 minutes
  - Alert if response time > 500ms
  ```

- [ ] **Security Tests**
  ```
  ✓ OWASP Top 10 vulnerability scan
  ✓ SQL injection attempts
  ✓ Cross-site scripting (XSS) tests
  ✓ CSRF protection validation
  ✓ Authentication bypass attempts
  ✓ Authorization edge cases
  ```

### Staging Sign-Off
- [ ] QA Team Approval
- [ ] Security Team Clearance
- [ ] Performance Baseline Met
- [ ] Documentation Complete

---

## 🌍 Production Deployment Phase (Days 8-10)

### Pre-Production Checklist
- [ ] **Final Code Review** - Peer review all changes
- [ ] **Change Log** - Document all modifications
- [ ] **Rollback Plan** - Document rollback procedures
- [ ] **Runbooks** - Operations documentation ready
- [ ] **On-Call Setup** - Engineers on standby

### Deployment Steps

#### Step 1: Backend Deployment
```bash
# 1. Backup current production database
pg_dump find_rlb_prod | gzip > /backups/find_rlb_pre_deploy.sql.gz

# 2. Pull latest code
git pull origin main

# 3. Install dependencies (if changed)
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --no-input

# 6. Restart application
systemctl restart find-rlb-backend
```

#### Step 2: Frontend Deployment
```bash
# 1. Build optimized bundle
npm run build

# 2. Test build locally
npm start

# 3. Deploy to production
vercel --prod
# OR
pm2 restart find-rlb-frontend
```

#### Step 3: Domain Activation
```
1. Update DNS TTL to 5 minutes (30 min before)
2. Update A/CNAME records
3. Wait for DNS propagation (up to 1 hour)
4. Verify site accessibility
5. Check SSL certificate validity
6. Restore DNS TTL to 3600 seconds
```

#### Step 4: Verification
```bash
# Check backend health
curl https://api.yourdomain.com/api/auth/profile/

# Check frontend load
curl https://yourdomain.com

# Verify blockchain connection
curl https://api.yourdomain.com/api/blockchain/health/

# Check database
psql -h host -d find_rlb_prod -c "SELECT COUNT(*) FROM users;"
```

### Post-Deployment Monitoring

#### Hour 1: Critical Monitoring
- [ ] Application error rate < 0.1%
- [ ] API response times normal
- [ ] Database queries performing well
- [ ] No blockchain connection errors
- [ ] User signups working
- [ ] Payments processing

#### Hour 2-4: Extended Monitoring
- [ ] Payment streaks tracking correctly
- [ ] Reward calculations accurate
- [ ] Leaderboard updating
- [ ] Email notifications sending
- [ ] Referral codes generating

#### Hour 4-24: Full System Verification
- [ ] No critical errors in logs
- [ ] Performance metrics stable
- [ ] User feedback positive
- [ ] All features operational
- [ ] Backup jobs completed
- [ ] Monitoring alerts configured

### Immediate Post-Deployment
- [ ] Announce deployment to users
- [ ] Monitor support channels for issues
- [ ] Gather initial feedback
- [ ] Document any issues encountered
- [ ] Schedule retrospective (24 hours post-deploy)

---

## 📋 Rollback Procedures

### If Critical Issues Occur

#### Immediate (< 5 minutes)
1. **Assess impact**: How many users affected?
2. **Notify team**: Alert engineers & leadership
3. **Decide**: Hotfix or rollback?
4. **Execute**: BEGIN ROLLBACK

#### Database Rollback
```bash
# 1. Backup current (broken) database
pg_dump find_rlb_prod > /backups/find_rlb_broken.sql.gz

# 2. Restore previous backup
psql find_rlb_prod < /backups/find_rlb_pre_deploy.sql.gz

# 3. Verify data integrity
psql -d find_rlb_prod -c "SELECT COUNT(*) FROM users, leases, payments;"

# 4. Restart application
systemctl restart find-rlb-backend
```

#### Code Rollback
```bash
# 1. Revert to previous commit
git revert <commit-hash>
git push origin main

# 2. Rebuild (backend)
pip install -r requirements.txt
python manage.py migrate
systemctl restart find-rlb-backend

# 3. Rebuild (frontend)
npm run build
npm start  # or deploy

# 4. Verify rollback succeeded
curl https://api.yourdomain.com/api/status/
```

#### Communication
```
1. Send status update to Slack/Email
2. Notify users via in-app banner
3. Document issue in incident log
4. Plan for post-mortem (within 24 hours)
5. Prevent recurrence before next deploy
```

---

## 🔒 Security Hardening

### Pre-Production Security Checklist
- [ ] **SSL/TLS** 
  - [x] Valid certificate
  - [x] Auto-renewal configured
  - [x] TLS 1.3 enabled
  - [x] HTTP → HTTPS redirect

- [ ] **API Security**
  - [x] Rate limiting enabled
  - [x] CORS properly configured
  - [x] JWT tokens with expiration
  - [x] Input validation on all endpoints
  - [x] Output encoding enabled
  - [x] SQL injection prevention (ORM)

- [ ] **Data Protection**
  - [x] Database encryption at rest
  - [x] Encryption in transit (TLS)
  - [x] Secrets management (.env not in git)
  - [x] PII data handling compliant
  - [x] Backup encryption enabled

- [ ] **Access Control**
  - [x] Admin panel behind 2FA
  - [x] Database credentials rotated
  - [x] SSH keys configured
  - [x] Firewall rules: allow only necessary ports
  - [x] No default credentials

### Ongoing Security
- [ ] Monthly security patches
- [ ] Quarterly penetration testing
- [ ] Annual security audit
- [ ] Dependency vulnerability scanning
- [ ] Log monitoring for suspicious activity

---

## 📞 Support & Escalation

### During Deployment (8 AM - 6 PM)
- **Lead Engineer**: [name] - on-call, makes decisions
- **Backend Engineer**: [name] - deploy & monitoring
- **Frontend Engineer**: [name] - frontend deployment
- **DevOps Engineer**: [name] - infrastructure
- **QA Lead**: [name] - testing & verification

### First Responder (If Issue)
1. **Assess**: Impact, severity, user count affected
2. **Communicate**: Notify stakeholders
3. **Investigate**: Check logs, monitoring
4. **Execute**: Hotfix or rollback
5. **Document**: Create incident report
6. **Prevent**: Plan improvements

### Contact Information
```
Slack Channel: #find-rlb-deploy
War Room: Zoom link in channel
On-Call Phone: [number]
Escalation VP: [email]
```

---

## ✅ Final Pre-Deployment Verification

Run this 1 hour before deployment:

```bash
# Backend Health
python manage.py check
python manage.py test

# Frontend Build
npm run build
npm run lint

# Database Backup
pg_dump find_rlb_prod | gzip > /backups/pre_deploy_$(date +%s).sql.gz

# Git Status
git status
git log --oneline -5

# Environment Check
echo $HEDERA_ACCOUNT_ID
echo $HEDERA_NETWORK
echo $DATABASE_URL

# Deployment Approval
# [ ] Lead engineer approval: _________________
# [ ] QA sign-off: _________________
# [ ] Product owner approval: _________________
# [ ] Ready to proceed: YES / NO
```

---

## 📊 Post-Deployment Dashboard

Create monitoring dashboard with:
- API response times (target: < 200ms)
- Error rate (target: < 0.1%)
- CPU usage (alert: > 80%)
- Memory usage (alert: > 85%)
- Database connections (alert: > 80% of max)
- User registrations (tracking metric)
- Payment success rate (target: > 99.5%)
- Blockchain operations status
- Leaderboard update frequency
- Reward distribution status

---

## 🎊 Deployment Success Criteria

✅ **All 28 API endpoints operational**  
✅ **Frontend loads in < 2 seconds**  
✅ **No critical errors in logs**  
✅ **Database queries performing well**  
✅ **Blockchain transactions confirmed**  
✅ **User registration working**  
✅ **Payments processing successfully**  
✅ **Rewards calculating correctly**  
✅ **Leaderboards updating**  
✅ **Monitoring alerts configured**

---

**Status:** Ready for Deployment  
**Target Date:** [Set by team]  
**Estimated Duration:** 4-6 hours  
**Rollback Window:** 24 hours  
**Communication Channel:** [Slack/Teams]

---

**Last Updated:** February 24, 2026  
**Next Review:** Upon deployment completion
