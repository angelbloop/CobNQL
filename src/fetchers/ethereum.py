import requests
from typing import Dict, Any
from .base import BaseBlockchainFetcher

class EthereumFetcher(BaseBlockchainFetcher):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.etherscan.io/api"

    @property
    def name(self) -> str:
        return "Ethereum"

    def get_transaction_info(self, tx_hash: str) -> Dict[str, Any]:
        params = {
            "module": "proxy",
            "action": "eth_getTransactionByHash",
            "txhash": tx_hash,
            "apikey": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data.get("result"), str) and "deprecated" in data.get("result", "").lower():
                return {
                    "network": self.name, 
                    "error": f"Etherscan V1 API is deprecated. Use https://etherscan.io/tx/{tx_hash}",
                    "success": False
                }
            
            if "result" in data and data["result"] is not None:
                return {"network": self.name, "data": data["result"], "success": True}
            
            return {"network": self.name, "error": data.get("message", "Transaction not found"), "success": False}
        except Exception as e:
            return {"network": self.name, "error": str(e), "success": False}