const { AccountId, PrivateKey, Client, ContractCreateFlow } = require("@hiero-ledger/sdk");
const fs = require("fs");

async function main() {
  const MY_ACCOUNT_ID = AccountId.fromString("0.0.7974203");
  const MY_PRIVATE_KEY = PrivateKey.fromStringECDSA("0x3b980fa28f0c1e58d677ef8ff75e248ac16f37fc5de373a236b39fe04e9a447a");
  const client = Client.forTestnet().setOperator(MY_ACCOUNT_ID, MY_PRIVATE_KEY);
  const bytecode = fs.readFileSync("./artifacts/contracts/SavingsVault.sol/SavingsVault.bin");
  const contractCreate = new ContractCreateFlow().setGas(3000000).setBytecode(bytecode);
  const txResponse = await contractCreate.execute(client);
  const receipt = await txResponse.getReceipt(client);
  const contractId = receipt.contractId;
  console.log("SavingsVault Contract deployed to:", contractId.toString());
  await client.close();
}
main().catch(console.error);
