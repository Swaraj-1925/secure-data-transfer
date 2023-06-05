// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Upload {
    struct Access {
        address user;
        bool authenticity; // To check the authenticity of the address
    }

    mapping(address => string) cid;
    mapping(address => Access[]) accesslist;
    mapping(address => mapping(address => bool)) ownership;
    mapping(address => mapping(address => bool)) prevdata;

    function store_cid(string memory _cid) external {
        cid[msg.sender] = _cid;
    }

    function allow(address user) external {
        ownership[msg.sender][user] = true;
        if (prevdata[msg.sender][user]) {
            for (uint256 i = 0; i < accesslist[msg.sender].length; i++) {
                if (accesslist[msg.sender][i].user == user) {
                    accesslist[msg.sender][i].authenticity = true;
                }
            }
        } else {
            accesslist[msg.sender].push(Access(user, true));
            prevdata[msg.sender][user] = true;
        }
    }

    function disallow(address user) public {
        ownership[msg.sender][user] = false;
        for (uint256 i = 0; i < accesslist[msg.sender].length; i++) {
            if (accesslist[msg.sender][i].user == user) {
                accesslist[msg.sender][i].authenticity = false;
            }
        }
    }

    function get_cid(address _user) external view returns (string memory) {
        require(_user == msg.sender || ownership[_user][msg.sender], "Unauthorized Access");
        return cid[_user];
    }

    function ShareAccess() public view returns (Access[] memory) {
        return accesslist[msg.sender];
    }
}