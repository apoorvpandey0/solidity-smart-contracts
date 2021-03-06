from brownie import (accounts,config,network,Contract,Lottery,MockV3Aggregator,VRFCoordinatorMock,LinkToken)

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork','mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']

def get_account(index=None,id=None):
    if index: return accounts[index]
    if id: return accounts.load(id)

    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

contract_to_mock = {
    'eth_usd_price_feed': MockV3Aggregator,
    'vrf_coordinator': VRFCoordinatorMock,
    'link_token': LinkToken
}

def get_contract(contract_name):
    """
        This function will grab the contract address from the config file
        or it will deploy a mock version of the contract and return mock contract

        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of the contract

    """
    contract_type = contract_to_mock[contract_name]
    
    # If running in local network
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # If contract has no previous deployments yet
        if len(contract_type)<=0:
            deploy_mocks()
        
        # Else return the last deployment
        contract = contract_type[-1]
    
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        # address,abi
        contract = Contract.from_abi(contract_type._name,contract_address,contract_type)
    return contract

DECIMALS = 8
INITIAL_VALUE = 200000000000

def deploy_mocks(decimals=DECIMALS,initial_value=INITIAL_VALUE):
    account = get_account()
    mock_price_feed = MockV3Aggregator.deploy(decimals,initial_value,{'from':account})
    link_token = LinkToken.deploy({'from':account})
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address,{'from':account})
    print("Mocks deployed - price feed: {}, link token: {}, vrf coordinator: {}".format(mock_price_feed.address,link_token.address,vrf_coordinator.address))

                                                                        
def fund_with_link(contract_address,account=None,link_token=None,amount=100000000000000000):
    # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address,amount,{'from':account})
    tx.wait(1)
    return tx
