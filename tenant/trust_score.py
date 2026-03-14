"""Tenant trust score pipeline and Hedera verification helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Dict, Optional

from django.contrib.auth import get_user_model

from service.events import log_user_event
from service.blockchain_service import BlockchainService
from tenant.models import Payment, Lease, Review, TenantTrustScore


def _hash_score_payload(payload: Dict) -> str:
    """Compute a stable hash for a score payload."""
    normalized = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def calculate_trust_score(user_id: int) -> Dict[str, float]:
    """Calculate tenant trust score components from persisted data."""
    # Payment consistency: % of payments marked as paid vs total expected
    payments = Payment.objects.filter(lease__tenant_id=user_id)
    total_payments = payments.count()
    paid_payments = payments.filter(status='paid').count()
    payment_consistency = (paid_payments / total_payments * 100) if total_payments > 0 else 0.0

    # Lease completion: % of leases that are completed/expired vs total
    leases = Lease.objects.filter(tenant_id=user_id)
    total_leases = leases.count()
    completed_leases = leases.filter(status__in=['expired', 'terminated']).count()
    lease_completion_rate = (completed_leases / total_leases * 100) if total_leases > 0 else 0.0

    # Review score: average rating scaled to 0-100
    reviews = Review.objects.filter(target_user_id=user_id)
    ratings = [r.rating for r in reviews if r.rating is not None]
    reviews_score = (sum(ratings) / len(ratings) * 20) if ratings else 0.0

    # Overall: simple average of components
    overall_score = (payment_consistency + lease_completion_rate + reviews_score) / 3

    return {
        'payment_consistency': payment_consistency,
        'lease_completion_rate': lease_completion_rate,
        'reviews_score': reviews_score,
        'overall_score': overall_score,
    }


def store_trust_score_on_chain(user_id: int, score_payload: Dict[str, float]) -> Optional[str]:
    """Store trust score components on Hedera via Reputation contract.

    Returns a transaction id or None if the chain call failed.
    """
    client = BlockchainService()
    if not client.is_available:
        return None

    # Use the reputation contract to store key components
    user_addr = str(user_id)
    try:
        client.update_reputation_components(
            user_id=user_addr,
            payment_consistency=int(round(score_payload['payment_consistency'])),
            lease_completion_rate=int(round(score_payload['lease_completion_rate'])),
            reviews_score=int(round(score_payload['reviews_score'])),
        )
        # In this simplified implementation we don't get a tx hash back.
        return "on_chain_ok"
    except Exception:
        return None


def get_or_create_trust_score(user_id: int, sync_on_chain: bool = False) -> TenantTrustScore:
    """Compute and store the latest trust score for a tenant."""
    score = calculate_trust_score(user_id)
    payload = {
        'user_id': user_id,
        **score,
    }
    score_hash = _hash_score_payload(payload)

    obj, _ = TenantTrustScore.objects.update_or_create(
        user_id=user_id,
        defaults={
            'payment_consistency': score['payment_consistency'],
            'lease_completion_rate': score['lease_completion_rate'],
            'reviews_score': score['reviews_score'],
            'overall_score': score['overall_score'],
            'score_hash': score_hash,
        },
    )

    if sync_on_chain:
        tx = store_trust_score_on_chain(user_id, score)
        if tx:
            obj.hedera_tx = tx
            obj.save(update_fields=['hedera_tx'])

    # Optional: log event for analytics
    log_user_event(
        user_id,
        event_type='trust_score_calculated',
        metadata={'overall_score': score['overall_score'], 'score_hash': score_hash},
    )

    return obj
