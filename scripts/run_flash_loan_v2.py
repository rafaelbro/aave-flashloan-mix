from brownie import FlashloanV2, accounts, config, network, interface

MINIMUM_FLASHLOAN_WETH_BALANCE = 500000000000000000 #0.5WETH
ETHERSCAN_TX_URL = "https://kovan.etherscan.io/tx/{}"


def main():
    """
    Executes the funcitonality of the flash loan.
    """
    acct = accounts.add(config["wallets"]["from_key"])
    print("Getting Flashloan contract...")
    flashloan = FlashloanV2[len(FlashloanV2) - 1]
    weth = interface.WethInterface(config["networks"][network.show_active()]["weth"])
    # We need to fund it if it doesn't have any token to fund!
    print("current balance of contract: ", weth.balanceOf(flashloan))
    if weth.balanceOf(flashloan) < MINIMUM_FLASHLOAN_WETH_BALANCE:
        print("Funding Flashloan contract with WETH...")
        weth.transfer(flashloan, "1 ether", {"from": acct})
    print("Executing Flashloan...")
    tx = flashloan.flashloan(weth, {"from": acct})
    print("You did it! View your tx here: " + ETHERSCAN_TX_URL.format(tx.txid))
    return flashloan
