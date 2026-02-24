// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Reputation {
    enum ReputationTier { BRONZE, SILVER, GOLD, PLATINUM }

    struct ReputationScore {
        uint paymentConsistency;    // 0-100
        uint leaseCompletionRate;   // 0-100
        uint reviewsScore;          // 0-100
        uint overallScore;          // Calculated average
        ReputationTier tier;
        uint lastUpdated;
    }

    address public owner;
    mapping(address => ReputationScore) public reputation;
    mapping(address => bool) public authorized;

    event ReputationUpdated(address indexed user, uint paymentConsistency, uint leaseCompletionRate, uint reviewsScore, uint overallScore, string tier);
    event TierUpdated(address indexed user, string newTier);
    event AuthorizationChanged(address indexed user, bool authorized);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    modifier onlyAuthorized() {
        require(msg.sender == owner || authorized[msg.sender], "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setAuthorized(address user, bool status) external onlyOwner {
        authorized[user] = status;
        emit AuthorizationChanged(user, status);
    }

    function updatePaymentConsistency(address user, uint score) external onlyAuthorized {
        require(score <= 100, "Score must be 0-100");
        reputation[user].paymentConsistency = score;
        _updateOverallScore(user);
    }

    function updateLeaseCompletionRate(address user, uint score) external onlyAuthorized {
        require(score <= 100, "Score must be 0-100");
        reputation[user].leaseCompletionRate = score;
        _updateOverallScore(user);
    }

    function updateReviewsScore(address user, uint score) external onlyAuthorized {
        require(score <= 100, "Score must be 0-100");
        reputation[user].reviewsScore = score;
        _updateOverallScore(user);
    }

    function _updateOverallScore(address user) internal {
        ReputationScore storage rep = reputation[user];
        rep.overallScore = (rep.paymentConsistency + rep.leaseCompletionRate + rep.reviewsScore) / 3;
        rep.lastUpdated = block.timestamp;
        _updateTier(user);
        emit ReputationUpdated(user, rep.paymentConsistency, rep.leaseCompletionRate, rep.reviewsScore, rep.overallScore, _getTierString(rep.tier));
    }

    function _updateTier(address user) internal {
        ReputationScore storage rep = reputation[user];
        ReputationTier oldTier = rep.tier;
        
        if (rep.overallScore >= 85) {
            rep.tier = ReputationTier.PLATINUM;
        } else if (rep.overallScore >= 70) {
            rep.tier = ReputationTier.GOLD;
        } else if (rep.overallScore >= 55) {
            rep.tier = ReputationTier.SILVER;
        } else {
            rep.tier = ReputationTier.BRONZE;
        }

        if (oldTier != rep.tier) {
            emit TierUpdated(user, _getTierString(rep.tier));
        }
    }

    function _getTierString(ReputationTier tier) internal pure returns (string memory) {
        if (tier == ReputationTier.PLATINUM) return "PLATINUM";
        if (tier == ReputationTier.GOLD) return "GOLD";
        if (tier == ReputationTier.SILVER) return "SILVER";
        return "BRONZE";
    }

    function getReputation(address user) external view returns (ReputationScore memory) {
        return reputation[user];
    }

    function getTier(address user) external view returns (string memory) {
        return _getTierString(reputation[user].tier);
    }
}
