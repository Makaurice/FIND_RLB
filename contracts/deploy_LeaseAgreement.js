const { AccountId, PrivateKey, Client, ContractCreateFlow } = require("@hiero-ledger/sdk");
const fs = require("fs");
require('dotenv').config({ path: '../.env' });
require('dotenv').config({ path: '.env.local' });

async function main() {
  const accountId = process.env.HEDERA_ACCOUNT_ID || "0.0.7974203";
  const privateKeyStr = process.env.HEDERA_PRIVATE_KEY_ECDSA || process.env.HEDERA_PRIVATE_KEY || "3b980fa28f0c1e58d677ef8ff75e248ac16f37fc5de373a236b39fe04e9a447a";
  
  console.log(`🔐 Deploying LeaseAgreement with account: ${accountId}`);
  
  const MY_ACCOUNT_ID = AccountId.fromString(accountId);
  const MY_PRIVATE_KEY = PrivateKey.fromStringECDSA("0x" + (privateKeyStr.startsWith('0x') ? privateKeyStr.slice(2) : privateKeyStr));
  const client = Client.forTestnet().setOperator(MY_ACCOUNT_ID, MY_PRIVATE_KEY);
  
  const bytecodeFile = "./artifacts/contracts/LeaseAgreement.sol/LeaseAgreement.bin";
  if (!fs.existsSync(bytecodeFile)) {
    console.error(`❌ Bytecode file not found: ${bytecodeFile}`);
    process.exit(1);
  }
  
  const bytecode = fs.readFileSync(bytecodeFile);
  const contractCreate = new ContractCreateFlow().setGas(3000000).setBytecode(bytecode);
  
  console.log("⏳ Deploying contract...");
  const txResponse = await contractCreate.execute(client);
  const receipt = await txResponse.getReceipt(client);
  const contractId = receipt.contractId;
  
  console.log(`✅ LeaseAgreement Contract deployed to: ${contractId.toString()}`);
  
  const deploymentInfo = {
    contract: "LeaseAgreement",
    contractId: contractId.toString(),
    deployedAt: new Date().toISOString(),
    accountId: accountId,
    network: "testnet"
  };
  
  fs.writeFileSync("./deployment_lease_output.json", JSON.stringify(deploymentInfo, null, 2));
  
  await client.close();
}

main().catch(err => {
  console.error(`❌ Deployment failed: ${err.message}`);
  process.exit(1);
});
