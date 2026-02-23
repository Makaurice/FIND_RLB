const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PropertyNFT", function () {
  let PropertyNFT, propertyNFT, owner, addr1;

  beforeEach(async function () {
    PropertyNFT = await ethers.getContractFactory("PropertyNFT");
    [owner, addr1] = await ethers.getSigners();
    propertyNFT = await PropertyNFT.deploy();
    await propertyNFT.deployed();
  });

  it("should register a property", async function () {
    await propertyNFT.registerProperty("NYC", "ipfs://meta", true, false, 1000);
    const prop = await propertyNFT.properties(0);
    expect(prop.owner).to.equal(owner.address);
    expect(prop.location).to.equal("NYC");
    expect(prop.forRent).to.equal(true);
    expect(prop.forSale).to.equal(false);
    expect(prop.price).to.equal(1000);
  });

  it("should update property status", async function () {
    await propertyNFT.registerProperty("NYC", "ipfs://meta", true, false, 1000);
    await propertyNFT.updateStatus(0, false, true, 2000);
    const prop = await propertyNFT.properties(0);
    expect(prop.forRent).to.equal(false);
    expect(prop.forSale).to.equal(true);
    expect(prop.price).to.equal(2000);
  });

  it("should transfer ownership", async function () {
    await propertyNFT.registerProperty("NYC", "ipfs://meta", true, false, 1000);
    await propertyNFT.transferOwnership(0, addr1.address);
    const prop = await propertyNFT.properties(0);
    expect(prop.owner).to.equal(addr1.address);
  });

  it("should lock property during lease", async function () {
    await propertyNFT.registerProperty("NYC", "ipfs://meta", true, true, 1000);
    await propertyNFT.lockDuringLease(0);
    const prop = await propertyNFT.properties(0);
    expect(prop.forRent).to.equal(false);
    expect(prop.forSale).to.equal(false);
  });
});
