// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PropertyNFT {
    enum PropertyStatus { AVAILABLE, OCCUPIED, MAINTENANCE, DELISTED }

    struct Property {
        uint256 propertyId;
        address owner;
        string location;
        string metadataURI;  // IPFS hash
        uint256 price;
        PropertyStatus status;
        uint256 registeredAt;
        uint256 lastUpdated;
        bool isNFT;
    }

    struct PropertyMetadata {
        uint beds;
        uint baths;
        uint sqft;
        string[] amenities;
        uint rating; // 0-5 stars
    }

    mapping(uint256 => Property) public properties;
    mapping(uint256 => PropertyMetadata) public propertyMetadata;
    mapping(uint256 => bool) public isLockedDuringLease;
    mapping(address => uint256[]) public ownerProperties;

    uint256 public nextPropertyId;
    address public owner;

    event PropertyRegistered(uint256 indexed propertyId, address indexed owner, string location);
    event StatusUpdated(uint256 indexed propertyId, string newStatus);
    event OwnershipTransferred(uint256 indexed propertyId, address from, address to);
    event PropertyLocked(uint256 indexed propertyId);
    event PropertyUnlocked(uint256 indexed propertyId);
    event MetadataUpdated(uint256 indexed propertyId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    modifier onlyPropertyOwner(uint256 propertyId) {
        require(properties[propertyId].owner == msg.sender, "Not property owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerProperty(
        string memory location,
        string memory metadataURI,
        uint256 price,
        uint beds,
        uint baths,
        uint sqft,
        string[] memory amenities
    ) external {
        require(bytes(location).length > 0, "Location required");
        require(price > 0, "Price must be positive");

        uint256 propertyId = nextPropertyId++;
        properties[propertyId] = Property(
            propertyId,
            msg.sender,
            location,
            metadataURI,
            price,
            PropertyStatus.AVAILABLE,
            block.timestamp,
            block.timestamp,
            true
        );

        propertyMetadata[propertyId] = PropertyMetadata(beds, baths, sqft, amenities, 0);
        ownerProperties[msg.sender].push(propertyId);

        emit PropertyRegistered(propertyId, msg.sender, location);
    }

    function updateStatus(uint256 propertyId, PropertyStatus newStatus) external onlyPropertyOwner(propertyId) {
        require(!isLockedDuringLease[propertyId], "Locked during lease");
        properties[propertyId].status = newStatus;
        properties[propertyId].lastUpdated = block.timestamp;
        emit StatusUpdated(propertyId, _getStatusString(newStatus));
    }

    function updatePrice(uint256 propertyId, uint256 newPrice) external onlyPropertyOwner(propertyId) {
        require(newPrice > 0, "Price must be positive");
        properties[propertyId].price = newPrice;
        properties[propertyId].lastUpdated = block.timestamp;
    }

    function updateMetadata(uint256 propertyId, uint beds, uint baths, uint sqft, string[] memory amenities, uint rating) external onlyPropertyOwner(propertyId) {
        require(rating <= 5, "Rating must be 0-5");
        propertyMetadata[propertyId] = PropertyMetadata(beds, baths, sqft, amenities, rating);
        emit MetadataUpdated(propertyId);
    }

    function transferOwnership(uint256 propertyId, address newOwner) external onlyPropertyOwner(propertyId) {
        require(newOwner != address(0), "Invalid new owner");
        require(!isLockedDuringLease[propertyId], "Locked during lease");

        address oldOwner = properties[propertyId].owner;
        properties[propertyId].owner = newOwner;
        properties[propertyId].lastUpdated = block.timestamp;

        // Update owner properties lists
        _removeFromArray(ownerProperties[oldOwner], propertyId);
        ownerProperties[newOwner].push(propertyId);

        emit OwnershipTransferred(propertyId, oldOwner, newOwner);
    }

    function lockDuringLease(uint256 propertyId) external onlyPropertyOwner(propertyId) {
        require(!isLockedDuringLease[propertyId], "Already locked");
        isLockedDuringLease[propertyId] = true;
        properties[propertyId].status = PropertyStatus.OCCUPIED;
        emit PropertyLocked(propertyId);
    }

    function unlockAfterLease(uint256 propertyId) external onlyPropertyOwner(propertyId) {
        require(isLockedDuringLease[propertyId], "Not locked");
        isLockedDuringLease[propertyId] = false;
        properties[propertyId].status = PropertyStatus.AVAILABLE;
        emit PropertyUnlocked(propertyId);
    }

    function getProperty(uint256 propertyId) external view returns (Property memory) {
        return properties[propertyId];
    }

    function getPropertyMetadata(uint256 propertyId) external view returns (PropertyMetadata memory) {
        return propertyMetadata[propertyId];
    }

    function getOwnerProperties(address owner_addr) external view returns (uint256[] memory) {
        return ownerProperties[owner_addr];
    }

    function _getStatusString(PropertyStatus status) internal pure returns (string memory) {
        if (status == PropertyStatus.AVAILABLE) return "AVAILABLE";
        if (status == PropertyStatus.OCCUPIED) return "OCCUPIED";
        if (status == PropertyStatus.MAINTENANCE) return "MAINTENANCE";
        return "DELISTED";
    }

    function _removeFromArray(uint256[] storage arr, uint256 value) internal {
        for (uint i = 0; i < arr.length; i++) {
            if (arr[i] == value) {
                arr[i] = arr[arr.length - 1];
                arr.pop();
                break;
            }
        }
    }
}
