const { ethers, run, network } = require("hardhat")

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS

async function main(room_id, members) {
  const [signer] = await ethers.getSigners();
    const storageFactory = await ethers.getContractFactory("Room")
    const contract = await storageFactory.attach(CONTRACT_ADDRESS);
    const tx = await contract.create_room(room_id, members)
    await tx.wait();
    console.log("successfully created room")
}

main(1548133828, ["0xe2BA10C388ef4A013Db4ff13f56B742893208D05"])
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })