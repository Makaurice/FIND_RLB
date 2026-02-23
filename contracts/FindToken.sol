// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FindToken {
    string public name = "FIND Utility Token";
    string public symbol = "FIND";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    // Allocation addresses
    address public ecosystem;
    address public staking;
    address public team;
    address public treasury;
    address public partners;
    address public liquidity;
    address public publicSale;

    uint256 public constant INITIAL_SUPPLY = 1_000_000_000 * 10**18;
    uint256 public teamVested;
    uint256 public teamClaimed;
    uint256 public vestingStart;
    uint256 public constant VESTING_DURATION = 4 * 365 days;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event TeamClaim(address indexed to, uint256 amount);

    constructor(
        address _ecosystem,
        address _staking,
        address _team,
        address _treasury,
        address _partners,
        address _liquidity,
        address _publicSale
    ) {
        ecosystem = _ecosystem;
        staking = _staking;
        team = _team;
        treasury = _treasury;
        partners = _partners;
        liquidity = _liquidity;
        publicSale = _publicSale;
        totalSupply = INITIAL_SUPPLY;
        vestingStart = block.timestamp;
        // Allocation
        balanceOf[ecosystem] = (INITIAL_SUPPLY * 25) / 100;
        balanceOf[staking] = (INITIAL_SUPPLY * 20) / 100;
        teamVested = (INITIAL_SUPPLY * 15) / 100;
        balanceOf[treasury] = (INITIAL_SUPPLY * 15) / 100;
        balanceOf[partners] = (INITIAL_SUPPLY * 10) / 100;
        balanceOf[liquidity] = (INITIAL_SUPPLY * 10) / 100;
        balanceOf[publicSale] = (INITIAL_SUPPLY * 5) / 100;
        emit Transfer(address(0), ecosystem, balanceOf[ecosystem]);
        emit Transfer(address(0), staking, balanceOf[staking]);
        emit Transfer(address(0), treasury, balanceOf[treasury]);
        emit Transfer(address(0), partners, balanceOf[partners]);
        emit Transfer(address(0), liquidity, balanceOf[liquidity]);
        emit Transfer(address(0), publicSale, balanceOf[publicSale]);
    }

    function claimTeamTokens() external {
        require(msg.sender == team, "Not team");
        uint256 vested = vestedTeamTokens();
        uint256 claimable = vested - teamClaimed;
        require(claimable > 0, "Nothing to claim");
        teamClaimed += claimable;
        balanceOf[team] += claimable;
        emit TeamClaim(team, claimable);
        emit Transfer(address(0), team, claimable);
    }

    function vestedTeamTokens() public view returns (uint256) {
        if (block.timestamp < vestingStart) return 0;
        uint256 elapsed = block.timestamp - vestingStart;
        if (elapsed >= VESTING_DURATION) return teamVested;
        return (teamVested * elapsed) / VESTING_DURATION;
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) public returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(balanceOf[from] >= value, "Insufficient balance");
        require(allowance[from][msg.sender] >= value, "Allowance exceeded");
        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;
        emit Transfer(from, to, value);
        return true;
    }
}
