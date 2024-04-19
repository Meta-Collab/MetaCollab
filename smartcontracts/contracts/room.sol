// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Room {

    event NewCommit(uint id);

    struct Commit {
        address user;
        uint timestamp;
        string model;
    }

    Commit[] private commits;

    mapping (uint => uint) private commitToRoom;
    mapping (uint => uint) private roomCommitCount;

    function push (string memory _model, uint _room) external {
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