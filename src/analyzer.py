from typing import Dict, Any, List, Set, Tuple
from collections import defaultdict

class BlockchainAnalyzer:
    @staticmethod
    def analyze_ethereum(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        if not raw_data.get("success"):
            return {"status": "Error", "details": raw_data.get("error")}

        tx = raw_data["data"]
        
        if isinstance(tx, str):
            return {"status": "Error", "details": "Invalid API response format"}
        
        value_eth = int(tx.get("value", "0x0"), 16) / 1e18
        
        analysis = {
            "Network": "Ethereum",
            "Hash": tx.get("hash"),
            "From": tx.get("from"),
            "To": tx.get("to"),
            "Value (ETH)": f"{value_eth:.6f}",
            "Analysis Notes": []
        }

        if value_eth > 10.0:
            analysis["Analysis Notes"].append("⚠️  LARGE TRANSACTION (> 10 ETH)")
        
        if tx.get("input") != "0x":
            analysis["Analysis Notes"].append("📝 Smart contract interaction")
        else:
            analysis["Analysis Notes"].append("💸 Regular coin transfer")

        return analysis

    @staticmethod
    def analyze_bitcoin(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        if not raw_data.get("success"):
            return {"status": "Error", "details": raw_data.get("error")}

        tx = raw_data["data"]
        
        inputs = tx.get("vin", [])
        outputs = tx.get("vout", [])
        
        analysis = {
            "Network": "Bitcoin",
            "Hash": tx.get("txid"),
            "Status": "Confirmed" if tx.get("status", {}).get("confirmed") else "Unconfirmed",
            "Size": f"{tx.get('size')} bytes",
            "Fee": f"{tx.get('fee', 0)} BTC" if tx.get('fee') else "N/A",
            "Block Height": tx.get("status", {}).get("block_height", "Unconfirmed"),
            "Inputs": len(inputs),
            "Outputs": len(outputs),
            "Analysis Notes": []
        }

        input_addresses: List[str] = []
        for i, inp in enumerate(inputs):
            if "prevout" in inp and inp["prevout"]:
                addr = inp["prevout"].get("scriptpubkey_address", "Unknown")
                if addr and addr not in input_addresses:
                    input_addresses.append(addr)

        output_addresses: List[str] = []
        output_values: List[float] = []
        for out in outputs:
            addr = out.get("scriptpubkey_address", "Unknown")
            value = out.get("value", 0) / 1e8
            if addr:
                output_addresses.append(addr)
                output_values.append(value)

        analysis["Input Addresses"] = input_addresses if input_addresses else ["Unknown"]
        analysis["Output Addresses"] = output_addresses if output_addresses else []
        
        links = BlockchainAnalyzer._find_address_links(input_addresses, output_addresses)
        if links:
            analysis["Address Links"] = links

        if len(outputs) > 100:
            analysis["Analysis Notes"].append("🔴 Bulk output (> 100 outputs) - possible fund distribution")
        
        if len(input_addresses) > len(output_addresses):
            analysis["Analysis Notes"].append("🔵 Consolidation: more inputs than outputs")
        elif len(output_addresses) > len(input_addresses):
            analysis["Analysis Notes"].append("🟢 Distribution: more outputs than inputs")

        dust_outputs = [v for v in output_values if v < 0.0001 and v > 0]
        if dust_outputs:
            analysis["Analysis Notes"].append(f"💫 Found {len(dust_outputs)} dust output(s)")

        if len(input_addresses) == 1 and len(output_addresses) == 2:
            analysis["Analysis Notes"].append("💸 Regular transaction (output + change)")
        elif len(input_addresses) > 1:
            analysis["Analysis Notes"].append("📋 Multisig or aggregation transaction")

        return analysis

    @staticmethod
    def _find_address_links(inputs: List[str], outputs: List[str]) -> Dict[str, List[str]]:
        """Find links between input and output addresses"""
        links = {}
        for inp in inputs:
            matching_outputs = [out for out in outputs if out and inp and inp.lower() == out.lower()]
            if matching_outputs:
                links[inp] = matching_outputs
        return links