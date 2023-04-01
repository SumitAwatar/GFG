pragma solidity ^0.8.0;

contract VideoAccess {
    address public owner;
    mapping(address => bool) public allowedDevices;

    constructor() {
        owner = msg.sender;
    }

    function addDevice(address device) public {
        require(msg.sender == owner, "Only the owner can add devices.");
        allowedDevices[device] = true;
    }

    function removeDevice(address device) public {
        require(msg.sender == owner, "Only the owner can remove devices.");
        allowedDevices[device] = false;
    }

    function isDeviceAllowed(address device) public view returns (bool) {
        return allowedDevices[device];
    }
}