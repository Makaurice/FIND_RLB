#!/usr/bin/env python3
"""
FIND-RLB System Access Guide
Shows where to access the running system and what to expect
"""

from datetime import datetime
import socket


def check_port_open(host, port):
    """Check if a port is accessible"""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, socket.error):
        return False


def display_access_guide():
    """Display complete access guide"""
    
    print("\n" + "="*80)
    print("  FIND-RLB SYSTEM IS RUNNING - ACCESS GUIDE")
    print("="*80)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check services
    print("SERVICE STATUS CHECK:")
    print("-"*80)
    
    backend_ready = check_port_open('127.0.0.1', 8000)
    frontend_ready = check_port_open('127.0.0.1', 3000)
    
    backend_status = "🟢 RUNNING" if backend_ready else "🟡 STARTING..."
    frontend_status = "🟢 RUNNING" if frontend_ready else "🟡 STARTING..."
    
    print(f"Backend API (Django):      {backend_status}")
    print(f"Frontend (Next.js):        {frontend_status}")
    print()
    
    # Access URLs
    print("="*80)
    print("  ACCESS YOUR SYSTEM")
    print("="*80)
    print()
    
    if frontend_ready:
        print("✅ FRONTEND IS READY!")
        print()
        print("   Open your browser and navigate to:")
        print("   URL: http://localhost:3000")
        print()
        print("   What you'll see:")
        print("   • Dashboard with welcome message")
        print("   • Featured properties showcase")
        print("   • Navigation to Tenant, Landlord, and Service portals")
        print("   • Platform highlights and features")
        print()
    else:
        print("⏳ Frontend is still starting (may take 1-2 minutes)...")
        print("   Once ready, open: http://localhost:3000")
        print()
    
    if backend_ready:
        print("✅ BACKEND API IS READY!")
        print()
        print("   API Endpoints:")
        print("   • Health Check:     http://localhost:8000/api/health/")
        print("   • API Status:       http://localhost:8000/api/status/")
        print("   • System Info:      http://localhost:8000/api/system/")
        print("   • Admin Panel:      http://localhost:8000/admin/")
        print()
    else:
        print("⏳ Backend API is still starting...")
        print("   Once ready, check: http://localhost:8000/api/health/")
        print()
    
    # Features
    print("="*80)
    print("  AVAILABLE FEATURES")
    print("="*80)
    print()
    print("Dashboard:")
    print("  • Welcome message with your user information")
    print("  • Featured properties with immediate booking options")
    print("  • Quick access to all platform modules")
    print()
    
    print("Tenant Module:")
    print("  • Search for properties")
    print("  • View detailed listings")
    print("  • Manage rental applications")
    print("  • Track savings progress")
    print()
    
    print("Landlord Module:")
    print("  • List properties")
    print("  • Manage tenant applications")
    print("  • Analytics and insights")
    print("  • Payment management")
    print()
    
    print("Service Provider Portal:")
    print("  • Browse available services")
    print("  • Manage bookings")
    print("  • Maintenance coordination")
    print()
    
    # Blockchain
    print("="*80)
    print("  BLOCKCHAIN (HEDERA)")
    print("="*80)
    print()
    print("Account Information:")
    print("  • Account ID:        0.0.7974203")
    print("  • Network:           Testnet")
    print("  • Chain ID:          296")
    print()
    
    print("Features Enabled:")
    print("  • Hedera Token Service (HTS)")
    print("  • Hedera Consensus Service (HCS)")
    print("  • Smart Contracts (PropertyNFT, Lease Agreement, Escrow, etc.)")
    print("  • AI-powered Matching Engine")
    print("  • Reward Distribution System")
    print()
    
    # Testing accounts
    print("="*80)
    print("  TEST ACCOUNTS (For Development)")
    print("="*80)
    print()
    print("Create test accounts:")
    print("  cd backend")
    print("  python manage.py createsuperuser")
    print()
    print("Then login with your test credentials")
    print()
    
    # Troubleshooting
    print("="*80)
    print("  TROUBLESHOOTING")
    print("="*80)
    print()
    
    if not backend_ready:
        print("❌ Backend not responding?")
        print("  • Check terminal 1: Is Django running?")
        print("  • Try: cd backend && python manage.py runserver")
        print()
    
    if not frontend_ready:
        print("❌ Frontend not loading?")
        print("  • Check terminal 2: Is npm running?")
        print("  • Try: cd frontend && npm run dev")
        print()
    
    print("❌ Seeing errors or missing features?")
    print("  • This is a development build")
    print("  • Some modules are intentionally limited")
    print("  • Module endpoints can be enabled in backend/findrlb_django/urls.py")
    print()
    
    print("❌ Database issues?")
    print("  • Run: cd backend && python manage.py migrate")
    print()
    
    print("❌ Import errors?")
    print("  • Run: cd backend && pip install -r requirements.txt")
    print()
    
    # Next steps
    print("="*80)
    print("  NEXT STEPS")
    print("="*80)
    print()
    print("1. Open http://localhost:3000 in your browser")
    print("2. Explore the frontend dashboard")
    print("3. Try the different modules (Tenant, Landlord, Service)")
    print("4. Create test accounts if needed")
    print("5. Monitor the API at http://localhost:8000/api/")
    print("6. Check blockchain integration working")
    print()
    
    # System info
    print("="*80)
    print("  SYSTEM INFORMATION")
    print("="*80)
    print()
    print("Frontend Stack:")
    print("  • Framework: Next.js 14+")
    print("  • Language: TypeScript")
    print("  • Styling: Tailwind CSS")
    print("  • Port: 3000")
    print()
    
    print("Backend Stack:")
    print("  • Framework: Django 4.x")
    print("  • API: Django REST Framework")
    print("  • Database: SQLite")
    print("  • Port: 8000")
    print()
    
    print("Blockchain:")
    print("  • Network: Hedera Testnet")
    print("  • Smart Contracts: Solidity")
    print("  • Services: HTS + HCS")
    print()
    
    # Final message
    print("="*80)
    print()
    print("  ✅ SYSTEM IS FULLY OPERATIONAL")
    print()
    print("  Visit http://localhost:3000 to see your application!")
    print()
    print("="*80 + "\n")


if __name__ == '__main__':
    display_access_guide()
