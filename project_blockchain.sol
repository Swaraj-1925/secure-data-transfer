// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Upload{
    struct access{
        //0x1234
        address user;
        bool authenticity;//To check the authenticity of the address
        
    }
    mapping(address=>string[]) value;
    mapping(address=>access[]) accesslist;
    mapping (address=>mapping(address=>bool)) ownership;
    mapping (address=>mapping(address=>bool)) prevdata;

    function get_url(address _user,string memory url) external{
        value[_user].push(url);
    }
    function allow(address user) external{
        ownership[msg.sender][user]=true;
        if(prevdata[msg.sender][user]){
            for(uint256 i=0;i<accesslist[msg.sender].length;i++){
                if(accesslist[msg.sender][i].user==user){
                    accesslist[msg.sender][i].authenticity=true;
                }
            }
        }
        else{
            accesslist[msg.sender].push(access(user,true));
            prevdata[msg.sender][user]=true;
        }
        
    }
    function disallow(address user)public{
        ownership[msg.sender][user]=false;
        for(uint256 i=0;i<accesslist[msg.sender].length;i++){
            if(accesslist[msg.sender][i].user==user){
             accesslist[msg.sender][i].authenticity=false;
            }

        }
    }
    function display(address _user) external view returns(string[] memory){
        require(_user==msg.sender || ownership[_user][msg.sender],"Unauthorized Access");
        return value[_user];
    }
    function ShareAccess() public view returns(access[] memory){
        return accesslist[msg.sender];
    }
    

}