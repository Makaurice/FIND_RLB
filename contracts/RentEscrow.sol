// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RentEscrow {
    enum PaymentStatus { PENDING, PAID, OVERDUE, DELINQUENT }

    struct RentRecord {
        uint leaseId;
        address tenant;
        address landlord;
        uint amount;
        uint dueDate;
        PaymentStatus status;
        uint paidDate;
    }

    struct EscrowAccount {
        uint leaseId;
        address tenant;
        address landlord;
        uint securityDeposit;
        uint totalRentCollected;
        uint totalPenalties;
        uint escrowBalance;
        bool securityDepositReleased;
    }

    uint public nextRentRecordId;
    mapping(uint => RentRecord) public rentRecords;
    mapping(uint => EscrowAccount) public escrowAccounts;
    mapping(uint => uint[]) public leaseRentHistory;

    uint public penaltyAmount = 10;
    uint public penaltyThresholdDays = 5; // Days overdue before penalty

    event RentPaid(uint leaseId, address indexed tenant, uint amount, uint paidDate);
    event LatePenaltyCharged(uint leaseId, address indexed tenant, uint penaltyAmount, uint newTotal);
    event SecurityDepositReceived(uint leaseId, uint amount);
    event SecurityDepositReleased(uint leaseId, address indexed tenant, uint refundAmount);
    event EscrowCreated(uint leaseId, address indexed landlord, address indexed tenant);

    modifier onlyTenant(uint leaseId) {
        require(msg.sender == escrowAccounts[leaseId].tenant, "Only tenant");
        _;
    }

    modifier onlyLandlord(uint leaseId) {
        require(msg.sender == escrowAccounts[leaseId].landlord, "Only landlord");
        _;
    }

    function createEscrow(uint leaseId, address landlord, address tenant, uint securityDeposit, uint monthlyRent) external {
        require(escrowAccounts[leaseId].leaseId == 0, "Escrow already exists");
        escrowAccounts[leaseId] = EscrowAccount(leaseId, tenant, landlord, securityDeposit, 0, 0, 0, false);
        emit EscrowCreated(leaseId, landlord, tenant);
    }

    function depositSecurityDeposit(uint leaseId) external payable {
        EscrowAccount storage escrow = escrowAccounts[leaseId];
        require(msg.sender == escrow.tenant, "Only tenant can deposit");
        require(msg.value > 0, "Deposit must be positive");
        
        escrow.escrowBalance += msg.value;
        emit SecurityDepositReceived(leaseId, msg.value);
    }

    function payRent(uint leaseId, uint amount, uint dueDate) external {
        EscrowAccount storage escrow = escrowAccounts[leaseId];
        require(msg.sender == escrow.tenant, "Only tenant can pay rent");
        require(amount > 0, "Amount must be positive");

        uint rentRecordId = nextRentRecordId++;
        PaymentStatus status = block.timestamp <= dueDate ? PaymentStatus.PAID : PaymentStatus.OVERDUE;
        
        rentRecords[rentRecordId] = RentRecord(leaseId, escrow.tenant, escrow.landlord, amount, dueDate, status, block.timestamp);
        leaseRentHistory[leaseId].push(rentRecordId);

        escrow.totalRentCollected += amount;
        escrow.escrowBalance += amount;

        emit RentPaid(leaseId, msg.sender, amount, block.timestamp);
    }

    function chargeLatePenalty(uint leaseId) external onlyLandlord(leaseId) {
        EscrowAccount storage escrow = escrowAccounts[leaseId];
        uint[] memory history = leaseRentHistory[leaseId];
        
        require(history.length > 0, "No rent records");
        
        RentRecord storage lastRecord = rentRecords[history[history.length - 1]];
        uint daysOverdue = (block.timestamp - lastRecord.dueDate) / 1 days;
        
        require(daysOverdue >= penaltyThresholdDays, "Not overdue enough");
        require(lastRecord.status != PaymentStatus.DELINQUENT, "Already charged");

        lastRecord.status = PaymentStatus.DELINQUENT;
        escrow.totalPenalties += penaltyAmount;
        escrow.escrowBalance -= penaltyAmount; // Deduct from balance

        emit LatePenaltyCharged(leaseId, lastRecord.tenant, penaltyAmount, escrow.totalPenalties);
    }

    function releaseSecurityDeposit(uint leaseId) external onlyLandlord(leaseId) {
        EscrowAccount storage escrow = escrowAccounts[leaseId];
        require(!escrow.securityDepositReleased, "Already released");
        require(escrow.escrowBalance >= escrow.securityDeposit, "Insufficient balance");

        escrow.securityDepositReleased = true;
        uint refundAmount = escrow.securityDeposit;
        escrow.escrowBalance -= refundAmount;

        // In production, transfer to tenant wallet
        emit SecurityDepositReleased(leaseId, escrow.tenant, refundAmount);
    }

    function getEscrowStatus(uint leaseId) external view returns (EscrowAccount memory) {
        return escrowAccounts[leaseId];
    }

    function getRentHistory(uint leaseId) external view returns (uint[] memory) {
        return leaseRentHistory[leaseId];
    }

    function getRentRecord(uint recordId) external view returns (RentRecord memory) {
        return rentRecords[recordId];
    }
}
