// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SocialCoordination {
    struct Referral {
        address referrer;
        address referee;
        uint256 timestamp;
    }
    struct Recommendation {
        address from;
        address to;
        string message;
        uint256 timestamp;
    }
    struct Sublease {
        uint256 propertyId;
        address originalTenant;
        address subTenant;
        uint256 startDate;
        uint256 endDate;
        bool active;
    }
    struct Group {
        uint256 id;
        string name;
        address[] members;
    }
    struct Review {
        address reviewer;
        address subject;
        string text;
        uint8 rating;
        uint256 timestamp;
    }

    uint256 public nextGroupId;
    uint256 public nextReviewId;
    mapping(address => Referral[]) public referrals;
    mapping(address => Recommendation[]) public recommendations;
    mapping(uint256 => Sublease) public subleases;
    mapping(uint256 => Group) public groups;
    mapping(uint256 => Review) public reviews;
    mapping(address => uint256[]) public userGroups;
    mapping(address => uint256[]) public userReviews;

    event ReferralMade(address indexed referrer, address indexed referee);
    event RecommendationMade(address indexed from, address indexed to, string message);
    event SubleaseCreated(uint256 indexed propertyId, address indexed originalTenant, address indexed subTenant);
    event GroupCreated(uint256 indexed id, string name);
    event JoinedGroup(uint256 indexed id, address indexed member);
    event ReviewSubmitted(uint256 indexed id, address indexed reviewer, address indexed subject, uint8 rating);

    function makeReferral(address referee) external {
        referrals[msg.sender].push(Referral(msg.sender, referee, block.timestamp));
        emit ReferralMade(msg.sender, referee);
    }
    function recommend(address to, string calldata message) external {
        recommendations[to].push(Recommendation(msg.sender, to, message, block.timestamp));
        emit RecommendationMade(msg.sender, to, message);
    }
    function createSublease(uint256 propertyId, address subTenant, uint256 startDate, uint256 endDate) external {
        subleases[propertyId] = Sublease(propertyId, msg.sender, subTenant, startDate, endDate, true);
        emit SubleaseCreated(propertyId, msg.sender, subTenant);
    }
    function createGroup(string calldata name) external {
        uint256 id = nextGroupId++;
        address[] memory members = new address[](1);
        members[0] = msg.sender;
        groups[id] = Group(id, name, members);
        userGroups[msg.sender].push(id);
        emit GroupCreated(id, name);
    }
    function joinGroup(uint256 id) external {
        Group storage g = groups[id];
        g.members.push(msg.sender);
        userGroups[msg.sender].push(id);
        emit JoinedGroup(id, msg.sender);
    }
    function submitReview(address subject, string calldata text, uint8 rating) external {
        require(rating >= 1 && rating <= 5, "Invalid rating");
        uint256 id = nextReviewId++;
        reviews[id] = Review(msg.sender, subject, text, rating, block.timestamp);
        userReviews[subject].push(id);
        emit ReviewSubmitted(id, msg.sender, subject, rating);
    }
}
