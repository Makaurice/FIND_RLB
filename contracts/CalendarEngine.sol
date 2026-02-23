// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CalendarEngine {
    struct Event {
        uint256 id;
        address user;
        string eventType;
        uint256 timestamp;
        string data;
        bool triggered;
    }

    uint256 public nextEventId;
    mapping(uint256 => Event) public events;
    mapping(address => uint256[]) public userEvents;

    event EventScheduled(uint256 indexed id, address indexed user, string eventType, uint256 timestamp, string data);
    event EventTriggered(uint256 indexed id, address indexed user, string eventType);

    function scheduleEvent(address user, string memory eventType, uint256 timestamp, string memory data) public returns (uint256) {
        uint256 id = nextEventId++;
        events[id] = Event(id, user, eventType, timestamp, data, false);
        userEvents[user].push(id);
        emit EventScheduled(id, user, eventType, timestamp, data);
        return id;
    }

    function triggerEvent(uint256 id) public {
        Event storage e = events[id];
        require(!e.triggered, "Already triggered");
        require(block.timestamp >= e.timestamp, "Too early");
        e.triggered = true;
        emit EventTriggered(id, e.user, e.eventType);
        // Add logic for eventType: payment reminder, lease expiry, etc.
    }

    function getUserEvents(address user) public view returns (uint256[] memory) {
        return userEvents[user];
    }
}
