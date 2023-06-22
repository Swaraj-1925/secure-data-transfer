// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Upload {
    address public admin;
    mapping(string => string) fileCIDs;
    mapping(address => bool) allowedAccess;
    mapping(string => address) fileAdmins;
    string[] public fileNames;
    string[] public fileInfo;

    constructor() { 
        admin = msg.sender;
    }

    modifier onlyAdminOrFileAdmin(string memory fileName) {
        require(
            msg.sender == admin || msg.sender == fileAdmins[fileName],
            "Only the admin or the file uploader can perform this action."
        );
        _;
    }

    function addFile(string memory fileName, string memory cid) public {
        fileCIDs[fileName] = cid;
        fileInfo.push(string(abi.encodePacked(fileName, " : ", cid)));
        fileNames.push(fileName);
        fileAdmins[fileName] = msg.sender;
        allowedAccess[msg.sender] = true;
    }

    function grantAccess(address user, string memory fileName) public onlyAdminOrFileAdmin(fileName) {
        allowedAccess[user] = true;
    }

    function revokeAccess(address user, string memory fileName) public onlyAdminOrFileAdmin(fileName) {
        allowedAccess[user] = false;
    }

    function getFileNames() public view returns (string[] memory) {
    // Create a dynamic array to store the file names
    string[] memory userFileNames = new string[](fileNames.length);
    uint256 count = 0;

    // Iterate through all file names and filter the ones uploaded by the caller
    for (uint256 i = 0; i < fileNames.length; i++) {
        if (fileAdmins[fileNames[i]] == msg.sender) {
            userFileNames[count] = fileNames[i];
            count++;
        }
    }

    // Create a new dynamic array with the correct length and copy the filtered file names
    string[] memory result = new string[](count);
    for (uint256 i = 0; i < count; i++) {
        result[i] = userFileNames[i];
    }

    return result;
}

    function getFileCID(string memory fileName) public view returns (string memory) {
        require(allowedAccess[msg.sender], "You do not have access to view this file.");
        return fileCIDs[fileName];
    }

    function getAllFileCIDs() public view returns (string[] memory) {
        return fileInfo;
    }

    function getFileAdmin(string memory fileName) public view returns (address) {
        return fileAdmins[fileName];
    }
}
