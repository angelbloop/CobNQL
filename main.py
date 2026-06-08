import typer
import json
import os
from rich.console import Console
from rich.panel import Panel
from src.fetchers.ethereum import EthereumFetcher
from src.fetchers.bitcoin import BitcoinFetcher
from src.analyzer import BlockchainAnalyzer
from src.reporter import ReportGenerator
from src.address_graph import AddressGraph, RiskAnalyzer

app = typer.Typer()
console = Console()

def load_config():
    if not os.path.exists("config.json"):
        with open("config.json", "w") as f:
            json.dump({"etherscan_api_key": "YOUR_KEY_HERE"}, f, indent=4)
    with open("config.json", "r") as f:
        return json.load(f)

@app.command()
def scan(tx_hash: str, depth: int = 1):
    """Scan a blockchain transaction"""
    config = load_config()
    console.print(f"[bold blue]Analyzing transaction:[/bold blue] {tx_hash}")
    
    graph = AddressGraph()
    
    if tx_hash.startswith("0x"):
        fetcher = EthereumFetcher(config.get("etherscan_api_key"))
        raw_data = fetcher.get_transaction_info(tx_hash)
        analysis = BlockchainAnalyzer.analyze_ethereum(raw_data)
    else:
        fetcher = BitcoinFetcher()
        raw_data = fetcher.get_transaction_info(tx_hash)
        analysis = BlockchainAnalyzer.analyze_bitcoin(raw_data)
        
        if raw_data.get("success"):
            inputs = analysis.get("Input Addresses", [])
            outputs = analysis.get("Output Addresses", [])
            graph.add_transaction(tx_hash, inputs, outputs)
            
            if inputs and outputs:
                stats = graph.get_graph_stats()
                analysis["Graph Stats"] = stats
                
                flags = RiskAnalyzer.detect_suspicious_patterns(graph, tx_hash)
                if flags:
                    analysis["Risk Flags"] = flags

    console.print(analysis)
    
    path = ReportGenerator.generate_txt_report([analysis], "latest.txt")
    console.print(f"[green]Report saved:[/green] {path}")

@app.command()
def osint(tx_hash: str):
    """OSINT analysis of addresses in transaction"""
    from src.osint_checker import OSINTChecker
    from src.enhanced_reporter import EnhancedReportGenerator
    
    config = load_config()
    console.print(f"[bold cyan]OSINT Analysis:[/bold cyan] {tx_hash}\n")
    
    if tx_hash.startswith("0x"):
        fetcher = EthereumFetcher(config.get("etherscan_api_key"))
        raw_data = fetcher.get_transaction_info(tx_hash)
    else:
        fetcher = BitcoinFetcher()
        raw_data = fetcher.get_transaction_info(tx_hash)
    
    if not raw_data.get("success"):
        console.print(f"[red]Error:[/red] {raw_data.get('error')}")
        return
    
    analysis = BlockchainAnalyzer.analyze_bitcoin(raw_data) if not tx_hash.startswith("0x") else BlockchainAnalyzer.analyze_ethereum(raw_data)
    
    addresses = []
    if "Input Addresses" in analysis:
        addresses.extend(analysis["Input Addresses"])
    if "Output Addresses" in analysis:
        addresses.extend(analysis["Output Addresses"])
    
    osint_result = OSINTChecker.analyze_transaction_addresses(addresses)
    flags = OSINTChecker.generate_flags(addresses)
    
    console.print("[bold]📊 OSINT Analysis Results:[/bold]\n")
    console.print(f"Total Addresses: {osint_result['total_addresses']}")
    console.print(f"Known Addresses: {len(osint_result['known_addresses'])}")
    console.print(f"Risk Level: {osint_result['risk_level']}")
    console.print(f"Confidence: {osint_result['overall_confidence']:.2%}\n")
    
    if osint_result["known_addresses"]:
        console.print("[bold cyan]Known Addresses:[/bold cyan]")
        for known in osint_result["known_addresses"]:
            console.print(f"  {known['address'][:20]}... → {known['category']}")
    
    if flags:
        console.print("\n[bold yellow]⚠️  Suspicious Patterns:[/bold yellow]")
        for flag in flags:
            console.print(f"  {flag}")
    
    path = EnhancedReportGenerator.generate_osint_report(osint_result, "osint_analysis.txt")
    console.print(f"\n[green]OSINT report:[/green] {path}")

if __name__ == "__main__":
    app()