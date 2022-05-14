from solcx import compile_standard, install_solc
import json
from web3 import Web3

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

    install_solc("0.6.0")

    # Compile the contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.6.0",
    )

# Save the compiled_sol as a json file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Fetching the bytecode from the compiled_code.json file
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# Fetching the abi code from the compiled_sol dictionary
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

localUrl = 'http://127.0.0.1:7545'
eth_rinkeby='https://rinkeby.infura.io/v3/5c12b3240a2b4bd4ae0881b70f515c61'

w3 = Web3(Web3.HTTPProvider(eth_rinkeby))

# chain_id = 1337 # Using this manually is giving some errors
chain_id = 4 # Official chain id for ETH Rinkeby

# Ganache accounts
# my_address = "0xa9e98925B14E0dCBb263dC599770fdd30f888afC"
# private_key = "b1e08130b9de52a192e76831a2d0e5e6f071019a6b9e119cfceea0fba3867277"

my_address = '0xF732D447FdC60d287B9111cA5D31829B820Eaf70'
private_key = 'a728933e25ff32c28fcf4da1000af5d82db4ff3d3fd719476f6be01f265c9218'

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Parts of transaction
# 1. Build a transaction
# 2. Sign the transaction
# 3. Send the transaction


# Step 1: Building the transaction
transaction = SimpleStorage.constructor().buildTransaction({
    'nonce': nonce,
    'from': my_address,
    'chainId': w3.eth.chain_id,
    'gasPrice': w3.eth.gas_price
})

# Step 2:  Signing the transaction
signed = w3.eth.account.signTransaction(transaction, private_key)

# Step 3: Send the transaction
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# For working with contract you need
# 1. Contract address
# 2. Contract ABI

simple_storage = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

# There are two ways of interacting with a Smart Contract 
# 1. Call or Retrive only interaction - non state changing
# 2. Transact or State changing interaction

# Call state
print(simple_storage.functions.retrieve().call())

# Transact state

# Step 1: Building transaction
store_transaction = simple_storage.functions.store(42).buildTransaction({
    'nonce': w3.eth.getTransactionCount(my_address),
    'from': my_address,
    'chainId': w3.eth.chain_id,
    'gasPrice': w3.eth.gas_price
})

# Step 2: Signing the transaction
signed_store_txn = w3.eth.account.signTransaction(store_transaction, private_key)

# Step 3: Send the transaction
send_store_txn = w3.eth.sendRawTransaction(signed_store_txn.rawTransaction)

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)


# Call state
print(simple_storage.functions.retrieve().call())







