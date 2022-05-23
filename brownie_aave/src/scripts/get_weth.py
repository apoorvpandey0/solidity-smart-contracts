from web3 import Web3
from brownie import config,network,interface
from scripts.utils import get_account

def main():
    get_weth()

def get_weth():
    account = get_account()
    weth = interface.IWeth(config['networks'][network.show_active()]['weth_token'])
    print("WETH deployed at {}".format(weth.address))

    tx = weth.deposit({'from':account, 'value':Web3.toWei(0.1, 'ether')})
    tx.wait(1)

    print("Deposited 0.1 ETH into WETH contract")