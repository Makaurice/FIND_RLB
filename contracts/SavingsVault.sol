// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SavingsVault {
    struct SavingsPlan {
        address saver;
        uint targetAmount;
        uint savedAmount;
        uint propertyId;
        bool completed;
    }

    uint public nextPlanId;
    mapping(uint => SavingsPlan) public plans;

    event SavingsDeposited(uint planId, address indexed saver, uint amount, uint totalSaved);
    event PlanCompleted(uint planId, address indexed saver);
    event OwnershipConverted(uint planId, address indexed saver, uint propertyId);

    function depositSavings(uint planId) external payable {
        SavingsPlan storage plan = plans[planId];
        require(!plan.completed, "Plan completed");
        plan.savedAmount += msg.value;
        emit SavingsDeposited(planId, msg.sender, msg.value, plan.savedAmount);
        if (plan.savedAmount >= plan.targetAmount) {
            plan.completed = true;
            emit PlanCompleted(planId, msg.sender);
        }
    }

    function autoMatchProperty(uint planId, uint propertyId) external {
        SavingsPlan storage plan = plans[planId];
        require(msg.sender == plan.saver, "Not saver");
        plan.propertyId = propertyId;
    }

    function convertToOwnership(uint planId) external {
        SavingsPlan storage plan = plans[planId];
        require(plan.completed, "Plan not completed");
        // Ownership transfer logic here
        emit OwnershipConverted(planId, plan.saver, plan.propertyId);
    }
}
