const { ethers, run, network } = require("hardhat")

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS

async function main(commit, room_id) {
  const [signer] = await ethers.getSigners();
    const storageFactory = await ethers.getContractFactory("Room")
  const contract = await storageFactory.attach(CONTRACT_ADDRESS);
  const tx = await contract.push(commit, room_id)
  await tx.wait();
  console.log("successfully updated contract")
}

main("hdoieh", 1)
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })