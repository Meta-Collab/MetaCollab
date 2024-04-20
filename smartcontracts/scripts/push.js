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

main("[ 7.81871229e-02 -4.58515435e-01 -7.39910543e-01 -1.21237881e-01 1.18119540e-02  2.05976233e-01 -7.21554339e-01 -6.48166612e-02 8.36113170e-02  5.00397974e-22 -6.65314180e-22 -8.04441097e-23 -2.41206422e-01  1.55485459e-02 -1.80058792e-01 -5.77486038e-01 2.82645345e-01 -2.47149408e-01 -1.29563004e-01 -5.72289377e-02 -1.34234670e-23  1.42827420e-03  6.42313480e-01 -8.67906958e-02 -6.00320927e-04  2.15270277e-03  4.66955379e-02  3.41252493e-22 3.20650823e-03 -7.62496144e-02 -3.43744314e-21  5.17112970e-21]", 1548133828)
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })