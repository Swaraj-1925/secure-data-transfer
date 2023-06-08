// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Upload {
    struct Access {
        address user;
        bool hasAccess;
    }

    struct CIDRecord {
        string cid;
        uint256 accessCode;
        mapping(address => bool) accessControl;
    }

    mapping(address => CIDRecord) private cidRecords;

    function storeCID(string memory _cid, uint256 _accessCode) public {
        require(_accessCode >= 100000 && _accessCode <= 999999, "Access code should be a 6-digit number");

        cidRecords[msg.sender].cid = _cid;
        cidRecords[msg.sender].accessCode = _accessCode;
        cidRecords[msg.sender].accessControl[msg.sender] = true; // Grant access to the sender by default
    }

    function grantAccess(address user, uint256 _accessCode) public {
        require(_accessCode == cidRecords[msg.sender].accessCode, "Invalid access code");
        cidRecords[msg.sender].accessControl[user] = true;
    }

    function revokeAccess(address user, uint256 _accessCode) public {
        require(_accessCode == cidRecords[msg.sender].accessCode, "Invalid access code");
        cidRecords[msg.sender].accessControl[user] = false;
    }

    function getCID(uint256 _accessCode) external view returns (string memory) {
        require(_accessCode == cidRecords[msg.sender].accessCode, "Invalid access code");
        require(
            cidRecords[msg.sender].accessControl[msg.sender],
            "Unauthorized Access"
        );
        return cidRecords[msg.sender].cid;
    }
}
