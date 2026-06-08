"""
OSINT Checker Module
Check addresses against known databases and find red flags
"""

from typing import Dict, List, Set, Tuple


class OSINTChecker:
    """Check addresses through OSINT"""
    
    # Known mixers
    KNOWN_MIXERS = {
        "tornado.cash": ["0x12d66f87a04a9e220743712ce6d9bb17b74d6b63"],
        "mixero": ["3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy"],
    }
    
    # Known exchanges
    KNOWN_EXCHANGES = {
        "Binance": ["1A1z7aD", "3J98t"],
        "Kraken": ["1Gkqab", "3CBq"],
        "Coinbase": ["1JV9g", "3R8Er"],
    }
    
    # Known mining pools
    KNOWN_POOLS = {
        "F2Pool": ["1A6jvMJhT"],
        "Antpool": ["1QJV9gf"],
    }
    
    # Federal Register - OFAC/Sanctioned addresses
    FEDERAL_REGISTER = {
        "Federal_Register_BTC": [
            "bc1qeth6n6ryxexvkx34wnx3nuynun4474h3j0gkhw",
            "bc1q2we5eqjj8je6lz9xwjattpc3pn4jejc5h0s70f",
            "bc1qnujzvts45qka3cr2eqqw8ur3q6g6s0ze2wlk5m",
            "bc1qw4fxztd5u3sl7vrcqwk2a8v5zh5dllvckx3tlt",
            "3EynPFpoGTPxU9m5bPaEDEUxUanzh7vgQP",
            "3FoD1f6Tfnq3s8MYHgJqFPWv9cUrtUdBSv",
        ]
    }
    
    @staticmethod
    def check_address_reputation(address: str) -> Dict[str, any]:
        """Check address reputation"""
        result = {
            "address": address,
            "is_known": False,
            "category": None,
            "confidence": 0.0,
            "tags": []
        }
        
        # Check Federal Register (HIGHEST PRIORITY)
        for fr_name, addresses in OSINTChecker.FEDERAL_REGISTER.items():
            for known_addr in addresses:
                if address.lower() == known_addr.lower():
                    result["is_known"] = True
                    result["category"] = "FEDERAL_REGISTER"
                    result["tags"].append("⚠️  OFAC/Sanctions List")
                    result["tags"].append("🚨 CRITICAL")
                    result["confidence"] = 1.0
                    return result
        
        # Check mixers
        for mixer_name, addresses in OSINTChecker.KNOWN_MIXERS.items():
            for known_addr in addresses:
                if address.lower().startswith(known_addr.lower()):
                    result["is_known"] = True
                    result["category"] = "Mixer"
                    result["tags"].append(f"Potentially: {mixer_name}")
                    result["confidence"] = 0.8
                    return result
        
        # Check exchanges
        for exchange_name, addresses in OSINTChecker.KNOWN_EXCHANGES.items():
            for known_addr in addresses:
                if address.lower().startswith(known_addr.lower()):
                    result["is_known"] = True
                    result["category"] = "Exchange"
                    result["tags"].append(exchange_name)
                    result["confidence"] = 0.6
                    return result
        
        # Check pools
        for pool_name, addresses in OSINTChecker.KNOWN_POOLS.items():
            for known_addr in addresses:
                if address.lower().startswith(known_addr.lower()):
                    result["is_known"] = True
                    result["category"] = "Mining Pool"
                    result["tags"].append(pool_name)
                    result["confidence"] = 0.7
                    return result
        
        return result
    
    @staticmethod
    def analyze_transaction_addresses(addresses: List[str]) -> Dict[str, any]:
        """Analyze all addresses in transaction"""
        analysis = {
            "total_addresses": len(addresses),
            "unknown_addresses": 0,
            "known_addresses": [],
            "suspicious_addresses": [],
            "risk_level": "Low",
            "overall_confidence": 0.0
        }
        
        suspicious_count = 0
        confidence_sum = 0.0
        
        for addr in addresses:
            if addr == "Unknown":
                analysis["unknown_addresses"] += 1
                continue
            
            reputation = OSINTChecker.check_address_reputation(addr)
            
            if reputation["is_known"]:
                analysis["known_addresses"].append({
                    "address": addr,
                    "category": reputation["category"],
                    "tags": reputation["tags"],
                    "confidence": reputation["confidence"]
                })
                
                if reputation["category"] == "Mixer":
                    suspicious_count += 1
                
                confidence_sum += reputation["confidence"]
        
        suspicious_ratio = suspicious_count / len(addresses) if addresses else 0
        if suspicious_ratio > 0.5:
            analysis["risk_level"] = "High"
        elif suspicious_ratio > 0.2:
            analysis["risk_level"] = "Medium"
        else:
            analysis["risk_level"] = "Low"
        
        if addresses:
            analysis["overall_confidence"] = confidence_sum / len(addresses)
        
        return analysis
    
    @staticmethod
    def generate_flags(addresses: List[str], amounts: List[float] = None) -> List[str]:
        """Generate suspicion flags based on addresses and amounts"""
        flags = []
        
        for addr in addresses:
            reputation = OSINTChecker.check_address_reputation(addr)
            if reputation["category"] == "Mixer":
                flags.append("🚨 MIXER_USAGE: Mixer detected (possible source obfuscation)")
                break
        
        unique_addrs = len(set(a for a in addresses if a != "Unknown"))
        if unique_addrs > 10:
            flags.append(f"⚠️  MANY_ADDRESSES: Many unique addresses ({unique_addrs})")
        
        unknown_count = sum(1 for a in addresses if a == "Unknown")
        if unknown_count > len(addresses) * 0.5:
            flags.append("⚠️  UNKNOWN_ADDRESSES: More than half addresses unknown")
        
        if amounts:
            dust_count = sum(1 for a in amounts if 0 < a < 0.0001)
            if dust_count > len(amounts) * 0.3:
                flags.append(f"💫 DUST_ATTACKS: Found {dust_count} dust outputs")
        
        return flags