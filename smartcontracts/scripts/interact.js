// imports
const { ethers, run, network } = require("hardhat")
const { exec } = require('child_process');

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS

async function new_room(room_id, members)
{
  const command = 'yarn hardhat run scripts/create_room.js --network sepolia';

  // Execute the command
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing command: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
}

async function push(commit, room_id)
{
  const command = 'yarn hardhat run scripts/push.js --network sepolia';

  // Execute the command
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing command: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
}

async function get_commits(room_id)
{
  const command = 'yarn hardhat run scripts/commit.js --network sepolia';

  // Execute the command
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing command: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
}

module.exports = { new_room, push, get_commits }