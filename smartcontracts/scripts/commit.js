const { ethers, run, network } = require("hardhat")

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS

async function main(room_id) {
  const [signer] = await ethers.getSigners();
    const storageFactory = await ethers.getContractFactory("Room")
    const contract = await storageFactory.attach(CONTRACT_ADDRESS);
    const commits = await contract.retrieve(room_id)
    return commits
}

commit = main(1548133828)
  .then(() => 
  module.exports = commit)
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })

  // Result(1) [
  //   Result(3) [
  //     '0xe2BA10C388ef4A013Db4ff13f56B742893208D05',
  //     1713643308n,
  //     'hdoieh'
  //   ]
  // ]