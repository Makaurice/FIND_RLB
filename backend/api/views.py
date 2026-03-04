"""
Health check and basic API views for FIND-RLB
"""
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'FIND-RLB backend is running',
        'timestamp': datetime.now().isoformat(),
        'service': 'FIND-RLB API v1.0',
        'blockchain': 'Hedera Testnet',
        'account': '0.0.7974203'
    })


@api_view(['GET'])
def api_status(request):
    """API status endpoint"""
    return JsonResponse({
        'api': 'operational',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health/',
            'auth': '/api/auth/',
            'properties': '/api/properties/',
            'search': '/api/search/',
        },
        'blockchain': {
            'network': 'testnet',
            'account_id': '0.0.7974203',
            'chain_id': 296,
        }
    })


@api_view(['GET'])
def system_info(request):
    """System information endpoint"""
    return JsonResponse({
        'system': 'FIND-RLB',
        'version': '1.0.0',
        'components': {
            'frontend': 'Next.js React',
            'backend': 'Django REST Framework',
            'blockchain': 'Hedera',
            'database': 'SQLite/PostgreSQL',
            'ai_agents': 'Enabled'
        },
        'features': [
            'Property Management (NFTs)',
            'Lease Agreements',
            'Escrow Services',
            'Reputation System',
            'Savings Programs',
            'P2P Community',
            'AI Matching Engine',
            'Reward Distribution',
        ],
        'deployed_at': '2026-03-04T18:13:00Z'
    })
