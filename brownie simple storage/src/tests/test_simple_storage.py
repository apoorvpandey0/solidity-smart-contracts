from brownie import SimpleStorage,accounts

"""
Some important points
1. The names of these functions should always start with "test_" to get collected by brownie

2. To test a single test case use: brownie test -k test_deploy

3. to also run the debugger if test fails use: brownie test --pdb

4. To get output in short forms use: brownie test -s

5. To run all the tests use: brownie test

All these functionalities are derived from Pytest
"""


def test_deploy():
    # Arrange
    account = accounts[0]
    
    # Act
    simple_storage = SimpleStorage.deploy({'from':account})
    starting_value = simple_storage.retrieve()
    expected = 0
    
    # Assert
    assert simple_storage.address != None
    assert starting_value == expected

def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({'from':account})
    
    # Act
    new_value = 15
    txn = simple_storage.store(new_value,{'from':account})
    txn.wait(1)
    updated_value = simple_storage.retrieve()
    
    # Assert
    assert new_value == updated_value

