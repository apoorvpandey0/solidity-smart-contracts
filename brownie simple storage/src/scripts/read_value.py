from brownie import accounts,config,SimpleStorage,network

# from .read_value import get_account

def read_contract():
    # SimpleStorage is a list of deployed contracts
    # Use -1 to get the latest deployments
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())

def main():
    read_contract()