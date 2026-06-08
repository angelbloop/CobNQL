"""
Address Graph Analysis Module
Analyzing relationships between blockchain addresses
"""

from typing import Dict, List, Set, Tuple
from collections import defaultdict


class AddressGraph:
    """Address graph and relationship analysis"""
    
    def __init__(self):
        self.nodes: Set[str] = set()
        self.edges: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.address_info: Dict[str, Dict] = {}
        self.transaction_links: Dict[str, List[str]] = {}
    
    def add_transaction(self, tx_hash: str, inputs: List[str], outputs: List[str], 
                       amounts: Dict[str, float] = None):
        """Add transaction to graph"""
        if amounts is None:
            amounts = {}
        
        self.transaction_links[tx_hash] = inputs + outputs
        
        for addr in inputs + outputs:
            if addr and addr != "Unknown":
                self.nodes.add(addr)
        
        for inp in inputs:
            for out in outputs:
                if inp and out and inp != "Unknown" and out != "Unknown":
                    amount = amounts.get(out, 0)
                    self.edges[inp].append((out, amount))
    
    def find_related_addresses(self, address: str, depth: int = 1) -> Set[str]:
        """Find all addresses related to given address at specified depth"""
        related = {address}
        current_level = {address}
        
        for _ in range(depth):
            next_level = set()
            for addr in current_level:
                for src in self.edges:
                    for dst, _ in self.edges[src]:
                        if dst == addr and src not in related:
                            next_level.add(src)
                for dst, _ in self.edges.get(addr, []):
                    if dst not in related:
                        next_level.add(dst)
            
            related.update(next_level)
            current_level = next_level
            
            if not current_level:
                break
        
        return related
    
    def find_address_chains(self, start_address: str, max_length: int = 5) -> List[List[str]]:
        """Find address chains starting from given address"""
        chains = []
        
        def dfs(addr: str, path: List[str], depth: int):
            if depth >= max_length:
                return
            
            for next_addr, _ in self.edges.get(addr, []):
                if next_addr not in path:
                    new_path = path + [next_addr]
                    chains.append(new_path)
                    dfs(next_addr, new_path, depth + 1)
        
        dfs(start_address, [start_address], 0)
        return chains
    
    def find_common_addresses(self, addresses: List[str]) -> Set[str]:
        """Find common addresses for given list"""
        if not addresses:
            return set()
        
        common = self.find_related_addresses(addresses[0], depth=2)
        
        for addr in addresses[1:]:
            related = self.find_related_addresses(addr, depth=2)
            common = common.intersection(related)
        
        return common
    
    def analyze_clustering(self) -> Dict[str, List[str]]:
        """Group addresses into clusters (potential wallets)"""
        clusters = {}
        visited = set()
        cluster_id = 0
        
        def dfs_cluster(addr: str, cluster: List[str]):
            if addr in visited or addr == "Unknown":
                return
            visited.add(addr)
            cluster.append(addr)
            
            for next_addr, _ in self.edges.get(addr, []):
                if next_addr not in visited:
                    dfs_cluster(next_addr, cluster)
            
            for src in self.edges:
                for dst, _ in self.edges[src]:
                    if dst == addr and src not in visited:
                        dfs_cluster(src, cluster)
        
        for node in self.nodes:
            if node not in visited:
                cluster = []
                dfs_cluster(node, cluster)
                if cluster:
                    clusters[f"cluster_{cluster_id}"] = cluster
                    cluster_id += 1
        
        return clusters
    
    def get_graph_stats(self) -> Dict[str, any]:
        """Get graph statistics"""
        total_edges = sum(len(edges) for edges in self.edges.values())
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": total_edges,
            "unique_sources": len(self.edges),
            "avg_connections": total_edges / len(self.edges) if self.edges else 0,
        }


class RiskAnalyzer:
    """Risk analysis and suspicious activity detection"""
    
    KNOWN_MIXERS = {
        "bc1p5cyj3p", "1A1z7aD",
    }
    
    KNOWN_EXCHANGES = {
        "1A1z7aD": "Suspected Exchange",
    }
    
    @staticmethod
    def calculate_privacy_risk(graph: AddressGraph, address: str) -> float:
        """Calculate privacy risk for address (0-1 scale)"""
        related = graph.find_related_addresses(address, depth=2)
        risk = min(1.0, len(related) / 100)
        return risk
    
    @staticmethod
    def detect_suspicious_patterns(graph: AddressGraph, tx_hash: str) -> List[str]:
        """Detect suspicious patterns in transaction"""
        flags = []
        
        if tx_hash in graph.transaction_links:
            addresses = graph.transaction_links[tx_hash]
            
            if len(addresses) > 20:
                flags.append("BULK_OUTPUT: Many addresses in single transaction")
            
            if len(addresses) != len(set(addresses)):
                flags.append("REPEATED_ADDR: Repeated addresses in transaction")
            
            unknown_count = sum(1 for a in addresses if a == "Unknown")
            if unknown_count > len(addresses) * 0.5:
                flags.append("UNKNOWN_ADDR: Many unknown addresses")
        
        return flags