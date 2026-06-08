import requests
from typing import Dict, Any
from .base import BaseBlockchainFetcher

class BitcoinFetcher(BaseBlockchainFetcher):
    @property
    def name(self) -> str:
        return "Bitcoin"
    
    def get_transaction_info(self, tx_hash: str) -> Dict[str, Any]:
        url = f"https://mempool.space/api/tx/{tx_hash}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return {"network": self.name, "data": response.json(), "success": True}
        except Exception as e:
            return {"network": self.name, "error": str(e), "success": False}