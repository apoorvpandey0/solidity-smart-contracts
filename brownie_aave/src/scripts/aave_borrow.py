from web3 import Web3
from brownie import (accounts,config,network,interface)
from scripts.utils import FORKED_LOCAL_ENVIRONMENTS, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.get_weth import get_weth

# All the lending pool functions are given over here@ AAVE Docs V2
# https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#repay

amount = Web3.toWei(0.1, 'ether')

def main():
    # Setup and deposit

    account = get_account()
    erc20_address = config['networks'][network.show_active()]['weth_token']

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS+FORKED_LOCAL_ENVIRONMENTS:
        # if we are in local blockchain, then first get some weth
        get_weth()
    lending_pool = get_lending_pool()
    # print(lending_pool)

    # Approve sending ERC20 Tokens
    approve_erc20(amount,lending_pool.address,erc20_address,account)

    print("Depositing 0.1 ETH into Lending Pool")
    tx = lending_pool.deposit(erc20_address,amount,account.address,0,{'from':account})
    tx.wait(1)
    print("Deposited!")

    (available_borrow_eth,total_collateral_eth,total_debt_eth,current_liquidation_threshold,ltv,health_factor) = get_user_account_data(lending_pool,account)
    

    # Borrowing
    print('Borrowing...')
    dai_eth_price = get_asset_price_feed(config['networks'][network.show_active()]['dai_eth_price_feed'])

    amount_dai_to_borrow = (1/dai_eth_price)*(available_borrow_eth*0.95)
    # amount_dai_to_borrow /=8
    print("Amount of DAI to borrow: {}".format(amount_dai_to_borrow))

    dai_address = config['networks'][network.show_active()]['dai_token_address']

    # function borrow(address asset, uint256 amount, uint256 interestRateMode, uint16 referralCode, address onBehalfOf)
    borrow_tx = lending_pool.borrow(dai_address,Web3.toWei(amount_dai_to_borrow,'ether'),1,0,account.address,{'from':account}) 
    borrow_tx.wait(1)
    print("Borrowed some DAI!")
    get_user_account_data(lending_pool,account)

    # Repay all debt

    # repay_all(amount,lending_pool,account)
    # print('Repaid all debt!')
    # get_user_account_data(lending_pool,account)

def repay_all(amount,lending_pool,account):
    approve_erc20(Web3.toWei(amount,'ether'),lending_pool,config['networks'][network.show_active()]['dai_token_address'],account)

    # function repay(address asset, uint256 amount, uint256 rateMode, address onBehalfOf)
    repay_tx = lending_pool.repay(
        config['networks'][network.show_active()]['dai_token_address'],
        amount,
        1,
        account.address,{'from':account}
    )
    repay_tx.wait(1)


def get_asset_price_feed(asset_address):
    # ABI,Address
    asset_price_feed = interface.IAggregatorV3(asset_address)
    price = asset_price_feed.latestRoundData()[1]
    print("Price feed ",price) # 489430000000000
    # Acc to https://docs.chain.link/docs/ethereum-addresses/
    # the price has 18 decimal places so the actual number is, 1 DAI = 0.000489430000000000 ETH
    converted_latest_price = Web3.fromWei(price,'ether')
    print('Converted price',converted_latest_price)
    return float(converted_latest_price)



def get_user_account_data(lending_pool,account):
    # ABI,Address
    (total_collateral_eth,total_debt_eth,available_borrow_eth,current_liquidation_threshold,ltv,health_factor) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, 'ether')
    total_collateral_eth = Web3.fromWei(total_collateral_eth, 'ether')
    total_debt_eth = Web3.fromWei(total_debt_eth, 'ether')
    print("Total Collateral: {} ETH".format(total_collateral_eth))
    print("Total Debt: {} ETH".format(total_debt_eth))
    print("Available Borrow: {} ETH".format(available_borrow_eth))
    print("Current Liquidation Threshold: {}".format(current_liquidation_threshold))
    print("LTV: {}".format(ltv))
    print("Health Factor: {}".format(health_factor))
    return (float(available_borrow_eth),float(total_collateral_eth),float(total_debt_eth),current_liquidation_threshold,ltv,health_factor)

def approve_erc20(amount,spender,erc20_address,account):
    print("Approving ERC20 Token transaction")
    # ABI, Address
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {'from':account})
    tx.wait(1)
    print("Approved!")
    return tx

def get_lending_pool():
    # ABI,Address    
    account = get_account()
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(config['networks'][network.show_active()]['lending_pool_addresses_provider'])
    lending_pool_address = lending_pool_address_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
    
    

    
