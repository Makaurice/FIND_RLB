// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PropertyNFT {
    struct Property {
        uint256 propertyId;
        address owner;
        string location;
        string metadataURI;
        bool forRent;
        bool forSale;
        uint256 price;
    }
    mapping(uint256 => Property) public properties;
    uint256 public nextPropertyId;

    event PropertyRegistered(uint256 propertyId, address owner);
    event StatusUpdated(uint256 propertyId, bool forRent, bool forSale, uint256 price);
    event OwnershipTransferred(uint256 propertyId, address from, address to);
    event LockedDuringLease(uint256 propertyId);

    function registerProperty(string memory location, string memory metadataURI, bool forRent, bool forSale, uint256 price) public {
        properties[nextPropertyId] = Property(nextPropertyId, msg.sender, location, metadataURI, forRent, forSale, price);
        emit PropertyRegistered(nextPropertyId, msg.sender);
        nextPropertyId++;
    }

    function updateStatus(uint256 propertyId, bool forRent, bool forSale, uint256 price) public {
        require(properties[propertyId].owner == msg.sender, "Not property owner");
        properties[propertyId].forRent = forRent;
        properties[propertyId].forSale = forSale;
        properties[propertyId].price = price;
        emit StatusUpdated(propertyId, forRent, forSale, price);
    }

    function transferOwnership(uint256 propertyId, address newOwner) public {
        require(properties[propertyId].owner == msg.sender, "Not property owner");
        address oldOwner = properties[propertyId].owner;
        properties[propertyId].owner = newOwner;
        emit OwnershipTransferred(propertyId, oldOwner, newOwner);
    }

    mapping(uint256 => bool) public isLocked;
    function lockDuringLease(uint256 propertyId) public {
        require(properties[propertyId].owner == msg.sender, "Not property owner");
        isLocked[propertyId] = true;
        emit LockedDuringLease(propertyId);
    }
}
