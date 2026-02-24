// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RentEscrow {
    mapping(uint => uint) public nextPaymentDue;
    mapping(uint => uint) public lastPaid;
    mapping(uint => address) public leaseToTenant;
    mapping(uint => address) public leaseToLandlord;
    mapping(uint => uint) public monthlyRent;
    mapping(uint => uint) public latePenalty;

    event RentPaid(uint leaseId, address indexed tenant, uint amount, uint dueDate);
    event ReminderEvent(uint leaseId, address tenant, uint dueDate);
    event ReputationUpdated(address indexed tenant, int scoreChange);

    function payRent(uint leaseId) external payable {
        require(msg.value >= monthlyRent[leaseId], "Insufficient rent");
        require(msg.sender == leaseToTenant[leaseId], "Not tenant");
        lastPaid[leaseId] = block.timestamp;
        nextPaymentDue[leaseId] = block.timestamp + 30 days;
        emit RentPaid(leaseId, msg.sender, msg.value, nextPaymentDue[leaseId]);
    }

    uint public penaltyAmount = 10;
    function chargeLatePenalty(uint leaseId) external {
        require(block.timestamp > nextPaymentDue[leaseId], "Not overdue");
        latePenalty[leaseId] += penaltyAmount;
        emit ReminderEvent(leaseId, leaseToTenant[leaseId], nextPaymentDue[leaseId]);
        emit ReputationUpdated(leaseToTenant[leaseId], -1);
    }
}
