// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LeaseAgreement {
    enum LeaseStatus { PENDING, ACTIVE, TERMINATED, DISPUTED }

    struct Lease {
        uint leaseId;
        uint propertyId;
        address landlord;
        address tenant;
        uint monthlyRent;
        uint securityDeposit;
        uint startDate;
        uint endDate;
        LeaseStatus status;
        uint createdAt;
    }

    struct Dispute {
        uint leaseId;
        address initiator;
        string reason;
        uint createdAt;
        bool resolved;
    }

    uint public nextLeaseId;
    uint public nextDisputeId;
    mapping(uint => Lease) public leases;
    mapping(uint => Dispute) public disputes;
    mapping(uint => uint[]) public leaseDisputes;

    address public arbitrator;

    event LeaseCreated(uint leaseId, uint propertyId, address indexed landlord, address indexed tenant, uint monthlyRent);
    event LeaseActivated(uint leaseId);
    event LeaseTerminated(uint leaseId, string reason);
    event LeaseRenewed(uint leaseId, uint newEndDate);
    event LeaseAmended(uint leaseId, uint newRent);
    event DisputeInitiated(uint leaseId, uint disputeId, address initiator, string reason);
    event DisputeResolved(uint disputeId, bool favorLandlord);

    modifier onlyLeasePart(uint leaseId) {
        Lease storage lease = leases[leaseId];
        require(msg.sender == lease.landlord || msg.sender == lease.tenant, "Not a lease party");
        _;
    }

    modifier onlyArbitrator() {
        require(msg.sender == arbitrator, "Only arbitrator");
        _;
    }

    constructor(address _arbitrator) {
        arbitrator = _arbitrator;
    }

    function createLease(uint propertyId, address tenant, uint monthlyRent, uint securityDeposit, uint startDate, uint endDate) external {
        require(tenant != address(0), "Invalid tenant");
        require(monthlyRent > 0, "Rent must be positive");
        require(endDate > startDate, "Invalid dates");

        uint leaseId = nextLeaseId++;
        leases[leaseId] = Lease(leaseId, propertyId, msg.sender, tenant, monthlyRent, securityDeposit, startDate, endDate, LeaseStatus.PENDING, block.timestamp);
        emit LeaseCreated(leaseId, propertyId, msg.sender, tenant, monthlyRent);
    }

    function activateLease(uint leaseId) external {
        Lease storage lease = leases[leaseId];
        require(msg.sender == lease.landlord, "Only landlord can activate");
        require(lease.status == LeaseStatus.PENDING, "Can only activate pending leases");
        lease.status = LeaseStatus.ACTIVE;
        emit LeaseActivated(leaseId);
    }

    function terminateLease(uint leaseId, string calldata reason) external onlyLeasePart(leaseId) {
        Lease storage lease = leases[leaseId];
        require(lease.status == LeaseStatus.ACTIVE, "Lease not active");
        lease.status = LeaseStatus.TERMINATED;
        emit LeaseTerminated(leaseId, reason);
    }

    function renewLease(uint leaseId, uint newEndDate) external {
        Lease storage lease = leases[leaseId];
        require(msg.sender == lease.landlord, "Only landlord can renew");
        require(newEndDate > lease.endDate, "New end date must be after current");
        lease.endDate = newEndDate;
        emit LeaseRenewed(leaseId, newEndDate);
    }

    function amendLease(uint leaseId, uint newMonthlyRent) external {
        Lease storage lease = leases[leaseId];
        require(msg.sender == lease.landlord, "Only landlord can amend");
        require(newMonthlyRent > 0, "Rent must be positive");
        require(lease.status == LeaseStatus.ACTIVE, "Can only amend active leases");
        lease.monthlyRent = newMonthlyRent;
        emit LeaseAmended(leaseId, newMonthlyRent);
    }

    function initiateDispute(uint leaseId, string calldata reason) external onlyLeasePart(leaseId) {
        Lease storage lease = leases[leaseId];
        require(lease.status == LeaseStatus.ACTIVE, "Can only dispute active leases");

        uint disputeId = nextDisputeId++;
        disputes[disputeId] = Dispute(leaseId, msg.sender, reason, block.timestamp, false);
        leaseDisputes[leaseId].push(disputeId);
        
        lease.status = LeaseStatus.DISPUTED;
        emit DisputeInitiated(leaseId, disputeId, msg.sender, reason);
    }

    function resolveDispute(uint disputeId, bool favorLandlord) external onlyArbitrator {
        Dispute storage dispute = disputes[disputeId];
        require(!dispute.resolved, "Dispute already resolved");
        dispute.resolved = true;
        
        Lease storage lease = leases[dispute.leaseId];
        if (favorLandlord) {
            lease.status = LeaseStatus.ACTIVE;
        } else {
            lease.status = LeaseStatus.TERMINATED;
        }
        
        emit DisputeResolved(disputeId, favorLandlord);
    }

    function getLease(uint leaseId) external view returns (Lease memory) {
        return leases[leaseId];
    }

    function getLeaseStatus(uint leaseId) external view returns (string memory) {
        LeaseStatus status = leases[leaseId].status;
        if (status == LeaseStatus.PENDING) return "PENDING";
        if (status == LeaseStatus.ACTIVE) return "ACTIVE";
        if (status == LeaseStatus.TERMINATED) return "TERMINATED";
        return "DISPUTED";
    }
}
