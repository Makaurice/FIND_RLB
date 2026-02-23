// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LeaseAgreement {
    struct Lease {
        uint leaseId;
        uint propertyId;
        address landlord;
        address tenant;
        uint monthlyRent;
        uint startDate;
        uint endDate;
        bool active;
    }

    uint public nextLeaseId;
    mapping(uint => Lease) public leases;

    event LeaseCreated(uint leaseId, uint propertyId, address indexed landlord, address indexed tenant);
    event LeaseActivated(uint leaseId);
    event LeaseTerminated(uint leaseId);
    event LeaseRenewed(uint leaseId, uint newEndDate);

    function createLease(uint propertyId, address tenant, uint monthlyRent, uint startDate, uint endDate) external {
        uint leaseId = nextLeaseId++;
        leases[leaseId] = Lease(leaseId, propertyId, msg.sender, tenant, monthlyRent, startDate, endDate, false);
        emit LeaseCreated(leaseId, propertyId, msg.sender, tenant);
    }

    function activateLease(uint leaseId) external {
        Lease storage lease = leases[leaseId];
        require(msg.sender == lease.landlord, "Only landlord can activate");
        lease.active = true;
        emit LeaseActivated(leaseId);
    }

    function terminateLease(uint leaseId) external {
        Lease storage lease = leases[leaseId];
        require(msg.sender == lease.landlord || msg.sender == lease.tenant, "Not authorized");
        lease.active = false;
        emit LeaseTerminated(leaseId);
    }

    function renewLease(uint leaseId, uint newEndDate) external {
        Lease storage lease = leases[leaseId];
        require(msg.sender == lease.landlord, "Only landlord can renew");
        lease.endDate = newEndDate;
        emit LeaseRenewed(leaseId, newEndDate);
    }
}
