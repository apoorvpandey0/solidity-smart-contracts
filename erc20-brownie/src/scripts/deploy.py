from web3 import Web3
from brownie import accounts,config,DoraToken

def deploy_token():
    account = accounts.add(config['wallets']['from_key'])
    # account = accounts[0]
    initial_supply = Web3.toWei(10000, 'ether')
    token = DoraToken.deploy(initial_supply,{'from':account},publish_source=True)
    print(token.name())

def main():
    deploy_token()