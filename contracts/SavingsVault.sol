// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SavingsVault {
    enum PlanStatus { ACTIVE, COMPLETED, WITHDRAWN, CANCELLED }

    struct SavingsPlan {
        uint planId;
        address saver;
        uint targetAmount;
        uint savedAmount;
        uint interestEarned;
        uint propertyId;
        PlanStatus status;
        uint createdAt;
        uint completedAt;
    }

    struct Deposit {
        uint planId;
        uint amount;
        uint timestamp;
    }

    uint public nextPlanId;
    uint public interestRate = 5; // 5% annual interest
    
    mapping(uint => SavingsPlan) public plans;
    mapping(uint => Deposit[]) public depositHistory;
    mapping(address => uint[]) public saverPlans;

    address public owner;

    event SavingsPlanCreated(uint indexed planId, address indexed saver, uint targetAmount);
    event SavingsDeposited(uint indexed planId, address indexed saver, uint amount, uint totalSaved);
    event InterestAccrued(uint indexed planId, uint interestAmount);
    event PlanCompleted(uint indexed planId, address indexed saver);
    event FundsWithdrawn(uint indexed planId, address indexed saver, uint amount);
    event PlanCancelled(uint indexed planId, address indexed saver);
    event OwnershipConverted(uint indexed planId, address indexed saver, uint propertyId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    modifier onlySaver(uint planId) {
        require(msg.sender == plans[planId].saver, "Not saver");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function createSavingsPlan(uint targetAmount, uint propertyId) external {
        require(targetAmount > 0, "Target must be positive");
        
        uint planId = nextPlanId++;
        plans[planId] = SavingsPlan(planId, msg.sender, targetAmount, 0, 0, propertyId, PlanStatus.ACTIVE, block.timestamp, 0);
        saverPlans[msg.sender].push(planId);
        
        emit SavingsPlanCreated(planId, msg.sender, targetAmount);
    }

    function depositSavings(uint planId) external payable {
        SavingsPlan storage plan = plans[planId];
        require(plan.status == PlanStatus.ACTIVE, "Plan not active");
        require(msg.value > 0, "Deposit must be positive");

        plan.savedAmount += msg.value;
        depositHistory[planId].push(Deposit(planId, msg.value, block.timestamp));

        emit SavingsDeposited(planId, msg.sender, msg.value, plan.savedAmount);

        if (plan.savedAmount >= plan.targetAmount) {
            plan.status = PlanStatus.COMPLETED;
            plan.completedAt = block.timestamp;
            emit PlanCompleted(planId, msg.sender);
        }
    }

    function accrueInterest(uint planId) external onlyOwner {
        SavingsPlan storage plan = plans[planId];
        require(plan.status == PlanStatus.ACTIVE || plan.status == PlanStatus.COMPLETED, "Plan inactive");

        uint interestAmount = (plan.savedAmount * interestRate) / 100 / 12; // Monthly interest
        plan.interestEarned += interestAmount;

        emit InterestAccrued(planId, interestAmount);
    }

    function withdrawFunds(uint planId, uint amount) external onlySaver(planId) {
        SavingsPlan storage plan = plans[planId];
        require(plan.status == PlanStatus.ACTIVE || plan.status == PlanStatus.COMPLETED, "Cannot withdraw");
        require(amount > 0, "Amount must be positive");
        require(plan.savedAmount + plan.interestEarned >= amount, "Insufficient funds");

        plan.savedAmount -= amount;
        plan.status = PlanStatus.WITHDRAWN;

        // In production, transfer to tenant wallet
        emit FundsWithdrawn(planId, msg.sender, amount);
    }

    function cancelPlan(uint planId) external onlySaver(planId) {
        SavingsPlan storage plan = plans[planId];
        require(plan.status == PlanStatus.ACTIVE, "Cannot cancel");
        
        plan.status = PlanStatus.CANCELLED;
        emit PlanCancelled(planId, msg.sender);
    }

    function setPropertyMatch(uint planId, uint propertyId) external onlySaver(planId) {
        SavingsPlan storage plan = plans[planId];
        require(plan.status == PlanStatus.COMPLETED || plan.status == PlanStatus.ACTIVE, "Plan not eligible");
        plan.propertyId = propertyId;
    }

    function convertToOwnership(uint planId) external onlySaver(planId) {
        SavingsPlan storage plan = plans[planId];
        require(plan.status == PlanStatus.COMPLETED, "Plan not completed");
        require(plan.propertyId != 0, "No property matched");
        
        // In production, trigger property ownership transfer
        emit OwnershipConverted(planId, msg.sender, plan.propertyId);
    }

    function getSavingsPlan(uint planId) external view returns (SavingsPlan memory) {
        return plans[planId];
    }

    function getSaverPlans(address saver) external view returns (uint[] memory) {
        return saverPlans[saver];
    }

    function getDepositHistory(uint planId) external view returns (Deposit[] memory) {
        return depositHistory[planId];
    }

    function getProgress(uint planId) external view returns (uint) {
        SavingsPlan storage plan = plans[planId];
        return (plan.savedAmount * 100) / plan.targetAmount;
    }
}
