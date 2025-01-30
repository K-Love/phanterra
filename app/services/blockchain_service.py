# app/services/blockchain_service.py

from web3 import Web3
from eth_account import Account
import json
import os
from typing import List, Dict
from dotenv import load_load_dotenv

load_dotenv()

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URI')))
        self.contract_address = os.getenv('NFT_CONTRACT_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.account = Account.from_key(self.private_key)

        # Load contract ABI
        with open('contracts/artifacts/ColoringBookNFT.json') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']

        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )

    def mint_batch(self, designs: List[Dict]) -> List[Dict]:
        """
        Mint NFTs for a batch of designs
        """
        nft_results = []

        for design in designs:
            try:
                # Upload metadata to IPFS
                metadata_uri = self._upload_to_ipfs(design)

                # Prepare transaction
                nonce = self.w3.eth.get_transaction_count(self.account.address)

                # Mint NFT
                mint_txn = self.contract.functions.mintDesign(
                    self.account.address,
                    metadata_uri
                ).build_transaction({
                    'nonce': nonce,
                    'gas': 500000,
                    'gasPrice': self.w3.eth.gas_price
                })

                # Sign and send transaction
                signed_txn = self.w3.eth.account.sign_transaction(
                    mint_txn,
                    private_key=self.private_key
                )
                tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

                # Wait for transaction receipt
                tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

                # Get token ID from event logs
                token_id = self._get_token_id_from_receipt(tx_receipt)

                nft_results.append({
                    'design_path': design['path'],
                    'token_id': token_id,
                    'transaction_hash': tx_hash.hex(),
                    'metadata_uri': metadata_uri,
                    'status': 'success'
                })

            except Exception as e:
                nft_results.append({
                    'design_path': design['path'],
                    'error': str(e),
                    'status': 'failed'
                })

        return nft_results

    def _upload_to_ipfs(self, design: Dict) -> str:
        """
        Upload design metadata to IPFS
        """
        # Create metadata
        metadata = {
            'name': f"Coloring Book Design #{design.get('id', 'unknown')}",
            'description': f"Original coloring book design from {design.get('niche', 'unknown')} collection",
            'image': design['path'],
            'attributes': [
                {
                    'trait_type': 'Niche',
                    'value': design.get('niche', 'unknown')
                },
                {
                    'trait_type': 'Style',
                    'value': design.get('type', 'unknown')
                }
            ]
        }

        # Implementation for IPFS upload would go here
        # For now, we'll simulate with a placeholder
        return f"ipfs://QmXxxx.../{design['id']}"

    def _get_token_id_from_receipt(self, receipt) -> int:
        """
        Extract token ID from transaction receipt
        """
        transfer_event = self.contract.events.Transfer().process_receipt(receipt)[0]
        return transfer_event['args']['tokenId']