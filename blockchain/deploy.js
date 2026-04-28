/**
 * Deployment script for ActionAuditLog contract
 */

const hre = require("hardhat");

async function main() {
  console.log("Deploying ActionAuditLog contract...");

  const ActionAuditLog = await hre.ethers.getContractFactory("ActionAuditLog");
  const contract = await ActionAuditLog.deploy();

  await contract.deployed();

  console.log("ActionAuditLog deployed to:", contract.address);
  console.log("Contract ABI saved to: artifacts/contracts/ActionAuditLog.sol/ActionAuditLog.json");

  // Save contract details for client
  const fs = require("fs");
  const contractInfo = {
    address: contract.address,
    network: hre.network.name,
    chainId: (await hre.ethers.provider.getNetwork()).chainId,
  };

  fs.writeFileSync(
    "contract-info.json",
    JSON.stringify(contractInfo, null, 2)
  );
  console.log("Contract info saved to: contract-info.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
