// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IFindToken {
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function transfer(address to, uint256 value) external returns (bool);
    function burn(uint256 value) external;
}

interface IUSDC {
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

contract TokenPayment {
    address public findToken;
    address public usdcToken;
    address public owner;
    uint256 public constant CASHBACK_MIN = 2;
    uint256 public constant CASHBACK_MAX = 5;
    uint256 public constant BURN_FEE = 1; // 1%
    mapping(address => uint256) public staked;
    mapping(address => uint256) public votingPower;
    mapping(address => uint256) public savings;
    mapping(address => uint256) public yieldRewards;
    uint256 public totalBurned;

    event Payment(address indexed payer, address indexed recipient, uint256 amount, string tokenType);
    event Cashback(address indexed user, uint256 amount);
    event Staked(address indexed landlord, uint256 amount);
    event Unstaked(address indexed landlord, uint256 amount);
    event SavingsBoost(address indexed user, uint256 reward);
    event Vote(address indexed user, string proposal, uint256 weight);
    event Burn(address indexed from, uint256 amount);

    constructor(address _findToken, address _usdcToken) {
        findToken = _findToken;
        usdcToken = _usdcToken;
        owner = msg.sender;
    }

    // 1️⃣ Rent Cashback
    function payRentWithFind(address recipient, uint256 amount) external {
        uint256 burnAmount = (amount * BURN_FEE) / 100;
        uint256 cashback = (amount * (CASHBACK_MIN + (block.timestamp % (CASHBACK_MAX - CASHBACK_MIN + 1)))) / 100;
        require(IFindToken(findToken).transferFrom(msg.sender, recipient, amount - burnAmount - cashback), "FIND transfer failed");
        require(IFindToken(findToken).transferFrom(msg.sender, address(this), cashback), "Cashback transfer failed");
        require(IFindToken(findToken).transferFrom(msg.sender, address(this), burnAmount), "Burn transfer failed");
        IFindToken(findToken).burn(burnAmount);
        totalBurned += burnAmount;
        emit Payment(msg.sender, recipient, amount, "FIND");
        emit Cashback(msg.sender, cashback);
        emit Burn(msg.sender, burnAmount);
    }

    // 2️⃣ Staking for Landlords
    function stake(uint256 amount) external {
        require(IFindToken(findToken).transferFrom(msg.sender, address(this), amount), "Stake transfer failed");
        staked[msg.sender] += amount;
        votingPower[msg.sender] += amount;
        emit Staked(msg.sender, amount);
    }
    function unstake(uint256 amount) external {
        require(staked[msg.sender] >= amount, "Not enough staked");
        staked[msg.sender] -= amount;
        votingPower[msg.sender] -= amount;
        require(IFindToken(findToken).transfer(msg.sender, amount), "Unstake transfer failed");
        emit Unstaked(msg.sender, amount);
    }

    // 3️⃣ Savings Booster
    function depositSavings(uint256 amount) external {
        require(IFindToken(findToken).transferFrom(msg.sender, address(this), amount), "Deposit failed");
        savings[msg.sender] += amount;
        uint256 reward = (amount * 5) / 100; // 5% yield
        yieldRewards[msg.sender] += reward;
        emit SavingsBoost(msg.sender, reward);
    }
    function claimYield() external {
        uint256 reward = yieldRewards[msg.sender];
        require(reward > 0, "No rewards");
        yieldRewards[msg.sender] = 0;
        require(IFindToken(findToken).transfer(msg.sender, reward), "Reward transfer failed");
    }

    // 4️⃣ Governance
    function vote(string calldata proposal, uint256 weight) external {
        require(votingPower[msg.sender] >= weight, "Not enough voting power");
        // Voting logic (record vote)
        emit Vote(msg.sender, proposal, weight);
    }

    // Premium listing fee burn
    function payPremiumListing(uint256 amount) external {
        require(IFindToken(findToken).transferFrom(msg.sender, address(this), amount), "Premium fee failed");
        IFindToken(findToken).burn(amount);
        totalBurned += amount;
        emit Burn(msg.sender, amount);
    }

    // Penalty burn
    function burnLatePenalty(uint256 amount) external {
        require(IFindToken(findToken).transferFrom(msg.sender, address(this), amount), "Penalty transfer failed");
        IFindToken(findToken).burn(amount);
        totalBurned += amount;
        emit Burn(msg.sender, amount);
    }
}
