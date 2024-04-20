// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Room {

    event NewCommit(uint id);

    struct Commit {
        address user;
        uint timestamp;
        string model;
    }

    modifier onlyMember(uint _room)
    {
        uint set = 0;
        for(uint i = 0; i < memberToRoom[msg.sender].length; i++)
        {
            if(memberToRoom[msg.sender][i] == _room)
                set = 1;
        }
        require(set == 1);
        _;
    }

    Commit[] private commits;

    mapping (uint => uint) private commitToRoom;
    mapping (uint => uint) private roomCommitCount;
    mapping (address => uint[]) private memberToRoom;

    function create_room (uint _room, address[] memory _users) external {
        for(uint i = 0; i < _users.length; i++)
        {
            memberToRoom[_users[i]].push(_room);
        }
    }

    function push (string memory _model, uint _room) external onlyMember(_room) {
        commits.push(Commit(msg.sender, block.timestamp, _model));
        uint id = commits.length - 1;
        commitToRoom[id] = _room;
        roomCommitCount[_room] ++;
        emit NewCommit(id);
    } 

    function retrieve (uint _room) external view returns (Commit[] memory) {
        Commit[] memory result = new Commit[](roomCommitCount[_room]);
        uint counter = 0;
        for(uint i = 0; i < commits.length; i++)
        {
            if(keccak256(abi.encodePacked(commitToRoom[i])) == keccak256(abi.encodePacked(_room)))
            {
                result[counter] = commits[i];
                counter ++;
            }
        }
        return result;
    }
}