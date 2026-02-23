// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Reputation {
    struct ReputationScore {
        uint paymentConsistency;
        uint leaseCompletionRate;
        uint reviewsScore;
    }

    mapping(address => ReputationScore) public reputation;

    event ReputationUpdated(address indexed user, uint paymentConsistency, uint leaseCompletionRate, uint reviewsScore);

    function updatePaymentConsistency(address user, uint score) external {
        reputation[user].paymentConsistency = score;
        emit ReputationUpdated(user, score, reputation[user].leaseCompletionRate, reputation[user].reviewsScore);
    }

    function updateLeaseCompletionRate(address user, uint score) external {
        reputation[user].leaseCompletionRate = score;
        emit ReputationUpdated(user, reputation[user].paymentConsistency, score, reputation[user].reviewsScore);
    }

    function updateReviewsScore(address user, uint score) external {
        reputation[user].reviewsScore = score;
        emit ReputationUpdated(user, reputation[user].paymentConsistency, reputation[user].leaseCompletionRate, score);
    }
}
