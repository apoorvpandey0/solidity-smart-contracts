import os
from brownie import accounts,config,SimpleStorage,network

from .read_value import get_account

# Method 1 of loading environment variables
# from dotenv import load_dotenv
# load_dotenv()
# print(os.getenv('TEST_VAR'))

def deploy_simple_storage():

    # Playing with accounts
    # account = accounts[0]
    # print(account,len(accounts))

    # Add new accounts, public address will be automatically generated using private key
    # account = accounts.add(config['wallets']['from_key'])
    # print(account)
    # print(config['wallets']['test_var'])

    account = get_account()

    # Brownie will automatically create a transaction and do all three steps for us
    # By default brownie uses Development network: ├─Ganache-CLI: development
    simple_storage = SimpleStorage.deploy({'from':account})

    # Print the address of the contract
    print("Deployed Smart contract address",simple_storage.address)

    # Print the value of the contract
    print("Initial value of favouriteNumber",simple_storage.retrieve())

    # Set the value of the contract
    txn = simple_storage.store(10,{'from':account})

    # It is recommended to wait for few confirmations after a transaction has occured
    txn.wait(1)

    # Print the updated value of the contract
    print("Updated value of favouriteNumber",simple_storage.retrieve())


def main():
    print("HSIT")
    deploy_simple_storage()