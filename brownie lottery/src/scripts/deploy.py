import time
from brownie import (accounts,config,network,Contract,Lottery,MockV3Aggregator,VRFCoordinatorMock,LinkToken)
from scripts.utils import (get_account,LOCAL_BLOCKCHAIN_ENVIRONMENTS,FORKED_LOCAL_ENVIRONMENTS,fund_with_link,get_contract)

def deploy_lottery():
    # account  = accounts.add('c71e90ee2bd937d7db8f9646e14cc62f80e0acf664e023cf184acfeec0129dff')
    # account = get_account(id='metamask')
    account = get_account()
    lottery = Lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][network.show_active()]['fee'],
        config['networks'][network.show_active()]['keyhash'],
        {'from':account},
        publish_source = config['networks'][network.show_active()].get('publish_source',False)
    )
    print(lottery.address)
    return lottery

def start_lottery():
    # account = get_account(id='metamask')
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({'from':account})
    tx.wait(1)
    print("Lottery is started!")

def enter_lottery():
    # account = get_account(id='metamask')
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee()+1000000000
    tx = lottery.enter({'from':account,"value":value})
    tx.wait(1)
    print("You entered the lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transation = lottery.endLottery({'from':account})
    ending_transation.wait(1)
    time.sleep(5)
    print("Lottery is Ended!")
    print("Winner",lottery.recentWinner())


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
