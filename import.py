from flask import Flask, jsonify, request
from web3 import Web3

app = Flask(__name__)

# Connect to the local blockchain node
w3 = Web3(Web3.HTTPProvider('http://localhost:5777'))

# Set the account address that will interact with the smart contract
w3.eth.default_account = "0x9C1944df65CA7496bABDFB0452D8a26A75C41E40"

# Compile the smart contract with Solidity compiler
with open('LandRegistration.sol', 'r') as f:
    contract_source_code = f.read()

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:LandRegistration']

# Instantiate the smart contract
contract = w3.eth.contract(
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin']
)

# Deploy the smart contract to the blockchain
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Get the contract address
contract_address = tx_receipt.contractAddress

# Instantiate the deployed contract
deployed_contract = w3.eth.contract(
    address=contract_address,
    abi=contract_interface['abi']
)

@app.route('/add-land', methods=['POST'])
def add_land():
    data = request.json
    name = data['name']
    location = data['location']
    on_sale = data['on_sale']
    pincode = data['pincode']

    tx_hash = deployed_contract.functions.addLand(name, location, on_sale, pincode).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({'status': 'success', 'message': f'Land {name} added'})

@app.route('/edit-land', methods=['PUT'])
def edit_land():
    data = request.json
    name = data['name']
    location = data['location']
    on_sale = data['on_sale']
    pincode = data['pincode']

    tx_hash = deployed_contract.functions.editLand(name, location, on_sale, pincode).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({'status': 'success', 'message': f'Land {name} edited'})

@app.route('/get-land-by-location', methods=['GET'])
def get_land_by_location():
    location = request.args.get('location')

    try:
        land_name = deployed_contract.functions.getLandUsingLocation(location).call()
        return jsonify({'status': 'success', 'name': land_name})
    except:
        return jsonify({'status': 'error', 'message': 'No land found at the given location'})

@app.route('/get-land', methods=['GET'])
def get_land():
    name = request.args.get('name')

    try:
        land = deployed_contract.functions.getLand(name).call()
        return jsonify({'status': 'success', 'name': land[0], 'location': land[1], 'on_sale': land[2], 'owner': land[3], 'pincode': land[4]})
    except:
        return jsonify({'status': 'error', 'message': 'Land not found'})

if __name__ == '__main__':
    app.run(debug=True)