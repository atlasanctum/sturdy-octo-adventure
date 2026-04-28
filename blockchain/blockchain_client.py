"""Python client for blockchain interaction."""

import os
import json
from typing import Dict, Any, Optional
from web3 import Web3


class BlockchainClient:
    """Client for interacting with Ethereum blockchain."""

    def __init__(self):
        """Initialize blockchain client."""
        self.rpc_url = os.getenv("BLOCKCHAIN_RPC_URL", "http://ganache:8545")
        self.contract_address = os.getenv("AUDIT_LOG_CONTRACT", "0x0000000000000000000000000000000000000000")
        self.private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY", "0x" + "0" * 64)
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contract = None
        self.account = None

    def connect(self) -> bool:
        """Connect to blockchain."""
        try:
            if not self.w3.is_connected():
                print(f"Warning: Unable to connect to blockchain at {self.rpc_url}")
                return False
            
            # Set up account
            self.account = self.w3.eth.account.from_key(self.private_key)
            print(f"Connected to blockchain. Account: {self.account.address}")
            return True
        except Exception as e:
            print(f"Failed to connect to blockchain: {e}")
            return False

    def set_contract(self, contract_address: str, contract_abi: list):
        """Set the contract to interact with."""
        try:
            self.contract_address = contract_address
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=contract_abi
            )
            print(f"Contract loaded at {contract_address}")
        except Exception as e:
            print(f"Failed to load contract: {e}")

    async def log_action(self, action: str, metadata: Dict[str, Any], tx_hash: str = "0x0") -> Optional[str]:
        """
        Log an action to the blockchain.
        
        Args:
            action: Action description
            metadata: Action metadata
            tx_hash: External transaction hash
            
        Returns:
            Blockchain transaction hash
        """
        if not self.contract:
            print("Warning: Contract not loaded, skipping blockchain logging")
            return None
        
        try:
            metadata_json = json.dumps(metadata)
            
            # Build transaction
            tx = self.contract.functions.logAction(
                action,
                metadata_json,
                bytes.fromhex(tx_hash.lstrip("0x") or "0")
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            print(f"Action logged to blockchain: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            print(f"Failed to log action to blockchain: {e}")
            return None

    async def get_log_count(self) -> Optional[int]:
        """Get total count of logged actions."""
        if not self.contract:
            return None
        
        try:
            count = self.contract.functions.getLogCount().call()
            return count
        except Exception as e:
            print(f"Failed to get log count: {e}")
            return None

    async def get_latest_log(self) -> Optional[Dict[str, Any]]:
        """Get the most recent log entry."""
        if not self.contract:
            return None
        
        try:
            log = self.contract.functions.getLatestLog().call()
            return {
                "timestamp": log[0],
                "executor": log[1],
                "action": log[2],
                "metadata": log[3],
            }
        except Exception as e:
            print(f"Failed to get latest log: {e}")
            return None


# Global instance
_blockchain_client: Optional[BlockchainClient] = None


async def get_blockchain_client() -> BlockchainClient:
    """Get or create blockchain client."""
    global _blockchain_client
    if _blockchain_client is None:
        _blockchain_client = BlockchainClient()
        _blockchain_client.connect()
    return _blockchain_client
