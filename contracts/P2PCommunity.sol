// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract P2PCommunity {
    enum UserType { TENANT, LANDLORD }
    struct UserProfile {
        address user;
        UserType userType;
        uint256 trustScore;
        uint256 rating;
        uint256 totalReviews;
        uint256 referralsCompleted;
        uint256 joinedAt;
    }

    mapping(address => UserProfile) public profiles;
    address[] public users;
    address public owner;

    event UserRegistered(address indexed user, UserType userType);
    event TrustUpdated(address indexed user, uint256 newTrust);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerUser(address user, uint8 userType) external {
        require(user != address(0), "Invalid user");
        require(profiles[user].user == address(0), "Already registered");
        UserType ut = UserType(userType);
        profiles[user] = UserProfile(user, ut, 0, 0, 0, 0, block.timestamp);
        users.push(user);
        emit UserRegistered(user, ut);
    }

    function updateTrust(address user, uint256 newScore) external onlyOwner {
        require(profiles[user].user != address(0), "Not registered");
        profiles[user].trustScore = newScore;
        emit TrustUpdated(user, newScore);
    }

    // very naive recommendation: return first N landlords/tenants
    function getTenantRecommendations(address tenant, uint256 limit) external view returns (address[] memory) {
        address[] memory recs = new address[](limit);
        uint256 count = 0;
        for (uint i = 0; i < users.length && count < limit; i++) {
            if (profiles[users[i]].userType == UserType.LANDLORD) {
                recs[count++] = users[i];
            }
        }
        return recs;
    }

    function getLandlordRecommendations(address landlord, uint256 limit) external view returns (address[] memory) {
        address[] memory recs = new address[](limit);
        uint256 count = 0;
        for (uint i = 0; i < users.length && count < limit; i++) {
            if (profiles[users[i]].userType == UserType.TENANT) {
                recs[count++] = users[i];
            }
        }
        return recs;
    }
}
