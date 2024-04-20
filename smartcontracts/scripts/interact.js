// imports
const { ethers, run, network } = require("hardhat")

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS

async function new_room(room_id, members)
{
  const storageFactory = await ethers.getContractFactory("Room")
  const contract = await storageFactory.attach(CONTRACT_ADDRESS);
  await contract.create_room(room_id, members)
}

async function push(commit, room_id)
{
  const storageFactory = await ethers.getContractFactory("Room")
  const contract = await storageFactory.attach(CONTRACT_ADDRESS);
  await contract.push(commit, room_id)
  console.log("successfully updated contract")
}

async function get_commits(room_id)
{
  const storageFactory = await ethers.getContractFactory("Room")
  const contract = await storageFactory.attach(CONTRACT_ADDRESS);
  commits = [].slice.call(await contract.retrieve(room_id))
  return commits
}

