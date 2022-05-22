from web3 import Web3
import pytest
from brownie import Lottery,accounts,network,config,exceptions

from scripts.deploy import deploy_lottery
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS,get_account

# To add our local mainnet-fork
# brownie networks delete mainnet-fork
# brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/0YWFI6MbTH7Ob6x19tMnaz2qJGumUGsQ accounts=10 mnemonic=brownie port=8545


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("This test is only for local environments")

    lottery = deploy_lottery()

    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        # This will raise brownie.exceptions.VirtualMachineError: revert: Lottery is closed/calculating winner
        # Which will be caught by above pytest.raises() and hence the test will pass
        lottery.enter({'from':get_account(), 'value':lottery.getEntranceFee()})

def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("This test is only for local environments")
    
    # Act
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account})
    tx = lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    tx.wait(1)

    # Assert
    assert lottery.players(0) == account
    


def test_get_entrance_fee():

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("This test is only for local environments")

    # Arrange
    lottery  = deploy_lottery( )
    print(lottery.address)

    # Act
    # 2000eth/usd
    # usdEntryfee = 50 USD
    # 2000/1 == 50/x == 0.025
    # print(lottery.getEthUsdPriceInUsd())
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entrance_fee = lottery.getEntranceFee()

    # Assert
    # This assertion holds only on development environment hence we're skipping on live networks
    assert expected_entrance_fee == entrance_fee


