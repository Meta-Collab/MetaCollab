// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Room {
    struct Commit {
        address user;
        uint timestamp;
        string model;
    }
    Commit[] private commits;

    mapping (uint => uint) private commitToRoom;
    mapping (uint => uint) private roomCommitCount;
    mapping (address => uint[]) private memberToRoom;
}