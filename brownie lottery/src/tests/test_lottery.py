from web3 import Web3
from brownie import Lottery,accounts,network,config

# To add our local mainnet-fork
# brownie networks delete mainnet-fork
# brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/0YWFI6MbTH7Ob6x19tMnaz2qJGumUGsQ accounts=10 mnemonic=brownie port=8545

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config['networks'][network.show_active()]['eth_usd_price_feed'],{'from':account}) 
    print(lottery.address)
    
    # To check if its in range of 0.020 and 0.025 ETH @ 2000 USD/ETH
    assert lottery.getEntranceFee() > Web3.toWei(0.020, 'ether')
    assert lottery.getEntranceFee() < Web3.toWei(0.025, 'ether')

# def test_price_feed():
#     account  = accounts[0]
#     lottery = Lottery.deploy('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419',{'from':account})
#     print(lottery.address)
    # print(lottery.getPrice())
    # assert lottery.getPrice()>1000


