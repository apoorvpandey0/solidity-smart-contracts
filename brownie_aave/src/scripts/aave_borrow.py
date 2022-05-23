from brownie import (accounts,config,network,interface)
from scripts.utils import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.get_weth import get_weth

def main():
    account = get_account()
    erc20_address = config['networks'][network.show_active()]['weth_token']

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS+FORKED_LOCAL_ENVIRONMENTS:
        # if we are in local blockchain, then first get some weth
        get_weth()
    lending_pool = get_lending_pool()
    print(lending_pool)


def get_lending_pool():
    # ABI,Address    
    account = get_account()
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(config['networks'][network.show_active()]['lending_pool_addresses_provider'])
    lending_pool_address = lending_pool_address_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
    
    

    
