from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseBlockchainFetcher(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return network name (e.g., 'Ethereum')"""
        pass

    @abstractmethod
    def get_transaction_info(self, tx_hash: str) -> Dict[str, Any]:
        """Fetch raw transaction data via API"""
        pass