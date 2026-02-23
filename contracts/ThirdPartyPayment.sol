// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ThirdPartyPayment {
    event PaidOnBehalf(address indexed payer, address indexed tenant, uint leaseId, uint amount);

    function payOnBehalf(address tenant, uint leaseId) external payable {
        require(msg.value > 0, "No payment");
        // Payment logic here
        emit PaidOnBehalf(msg.sender, tenant, leaseId, msg.value);
    }
}
