require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      chainId: 1337
    },
    hedera: {
      url: "https://testnet.hedera.hashgraph.com:8545",
      accounts: process.env.HEDERA_PRIVATE_KEY ? [`0x${process.env.HEDERA_PRIVATE_KEY.startsWith('0x') ? process.env.HEDERA_PRIVATE_KEY.slice(2) : process.env.HEDERA_PRIVATE_KEY}`] : [],
      chainId: 296
    }
  },
  paths: {
    artifacts: "./artifacts",
    cache: "./cache",
    sources: "./contracts",
    tests: "./test"
  }
};