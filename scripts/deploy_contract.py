# scripts/deploy_contract.py

from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv

load_dotenv()

def deploy_contract():
    w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URI')))
    account = Account.from_key(os.getenv('PRIVATE_KEY'))

    # Load contract bytecode and abi
    with open('contracts/artifacts/ColoringBookNFT.json') as f:
        contract_json = json.load(f)
        bytecode = contract_json['bytecode']
        abi = contract_json['abi']

    # Create contract deployment transaction
    ColoringBookNFT = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(account.address)

    # Build deployment transaction
    transaction = ColoringBookNFT.constructor().build_transaction({
        'nonce': nonce,
        'gas': 4000000,
        'gasPrice': w3.eth.gas_price
    })

    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(
        transaction,
        private_key=os.getenv('PRIVATE_KEY')
    )

    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contract deployed at: {tx_receipt.contractAddress}")

    # Save contract address to .env
    with open('.env', 'a') as f:
        f.write(f"\nNFT_CONTRACT_ADDRESS={tx_receipt.contractAddress}")

    return tx_receipt.contractAddress

if __name__ == "__main__":
    deploy_contract()