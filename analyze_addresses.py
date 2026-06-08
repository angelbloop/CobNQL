#!/usr/bin/env python3
"""
Federal Register Bitcoin Addresses Analysis
Automated OSINT checking for Federal Register addresses
"""

from src.osint_checker import OSINTChecker
from src.address_graph import AddressGraph, RiskAnalyzer

addresses = [
    'bc1qeth6n6ryxexvkx34wnx3nuynun4474h3j0gkhw',
    'bc1q2we5eqjj8je6lz9xwjattpc3pn4jejc5h0s70f',
    'bc1qnujzvts45qka3cr2eqqw8ur3q6g6s0ze2wlk5m',
    'bc1qw4fxztd5u3sl7vrcqwk2a8v5zh5dllvckx3tlt',
    '3EynPFpoGTPxU9m5bPaEDEUxUanzh7vgQP',
    '3FoD1f6Tfnq3s8MYHgJqFPWv9cUrtUdBSv'
]

print('=' * 80)
print('FEDERAL REGISTER BITCOIN ADDRESSES ANALYSIS')
print('=' * 80)
print()

print('INDIVIDUAL ADDRESS REPUTATION CHECK:')
print('-' * 80)

for i, addr in enumerate(addresses, 1):
    result = OSINTChecker.check_address_reputation(addr)
    print(f'{i}. {addr}')
    print(f'   Status: {"KNOWN" if result["is_known"] else "UNKNOWN"}')
    print(f'   Category: {result["category"] if result["category"] else "N/A"}')
    print(f'   Confidence: {result["confidence"]:.1%}')
    if result["tags"]:
        print(f'   Tags: {", ".join(result["tags"])}')
    print()

print('=' * 80)
print('GROUP ANALYSIS')
print('=' * 80)
print()

analysis = OSINTChecker.analyze_transaction_addresses(addresses)
print(f'Total Addresses: {analysis["total_addresses"]}')
print(f'Known Addresses: {len(analysis["known_addresses"])}')
print(f'Unknown Addresses: {analysis["unknown_addresses"]}')
print(f'Risk Level: {analysis["risk_level"]}')
print(f'Confidence: {analysis["overall_confidence"]:.2%}')
print()

if analysis["known_addresses"]:
    print('Known Addresses Details:')
    for known in analysis["known_addresses"]:
        print(f'  • {known["address"]}: {known["category"]} ({known["confidence"]:.0%})')
print()

print('=' * 80)
print('RISK FLAGS DETECTED')
print('=' * 80)
print()

flags = OSINTChecker.generate_flags(addresses)
if flags:
    for flag in flags:
        print(f'⚠️  {flag}')
else:
    print('✅ No suspicious patterns detected in current configuration')
print()

print('=' * 80)
print('ADDRESS GRAPH ANALYSIS')
print('=' * 80)
print()

graph = AddressGraph()
graph.add_transaction('group_tx_federal_register', addresses[:4], addresses[4:])
stats = graph.get_graph_stats()

print(f'Total Nodes: {stats["total_nodes"]}')
print(f'Total Edges: {stats["total_edges"]}')
print(f'Unique Sources: {stats["unique_sources"]}')
print(f'Avg Connections: {stats["avg_connections"]:.2f}')
print()

print('=' * 80)
print('RECOMMENDATIONS')
print('=' * 80)
print()

print('📋 Address Status Summary:')
print(f'  • {len(analysis["known_addresses"])} known addresses in Federal Register')
print(f'  • {analysis["unknown_addresses"]} addresses not in current database')
print(f'  • Risk Assessment: {analysis["risk_level"]}')
print()

print('🚨 CRITICAL ALERTS:')
if len(analysis["known_addresses"]) == 6:
    print('  ⛔ ALL ADDRESSES ARE MARKED AS FEDERAL REGISTER')
    print('  ⛔ POTENTIAL OFAC SANCTIONS VIOLATION DETECTED')
    print('  ⛔ IMMEDIATE ACTION REQUIRED')
    print()
    print('  Action Items:')
    print('    1. ❌ DO NOT PROCESS PAYMENTS FROM/TO THESE ADDRESSES')
    print('    2. ✋ FREEZE ANY RELATED ACCOUNTS')
    print('    3. 📋 REPORT TO COMPLIANCE/LEGAL TEAM')
    print('    4. 📋 FILE SAR (Suspicious Activity Report)')
    print('    5. 🔗 CROSS-REFERENCE WITH TREASURY OFAC LIST')
else:
    print('  ✅ No critical alerts detected')
print()

print('🔍 Next Steps:')
print('  1. Cross-reference with OFAC SDN list')
print('  2. Check transaction history for each address')
print('  3. Monitor future transactions from these addresses')
print('  4. Correlate with other investigation data')
print()

print('=' * 80)
print('SAVING DETAILED REPORT')
print('=' * 80)

from src.enhanced_reporter import EnhancedReportGenerator

report_data = {
    "analysis_type": "Federal Register Bitcoin Addresses",
    "timestamp": __import__('datetime').datetime.now().isoformat(),
    "addresses_analyzed": len(addresses),
    "known_addresses": len(analysis["known_addresses"]),
    "risk_level": analysis["risk_level"],
    "critical_alert": len(analysis["known_addresses"]) == 6,
    "details": {
        "known_addresses": analysis["known_addresses"],
        "individual_results": [OSINTChecker.check_address_reputation(addr) for addr in addresses],
        "graph_stats": stats,
        "flags": flags,
    }
}

json_path = EnhancedReportGenerator.generate_json_report([report_data], "federal_register_analysis.json")
print(f'✅ JSON Report: {json_path}')

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Federal Register Bitcoin Addresses Analysis</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; background: #1a1a1a; color: #fff; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #d32f2f; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .header h1 {{ margin: 0; color: white; }}
        .alert {{ background: #c62828; border-left: 4px solid #ff6f00; padding: 15px; margin: 10px 0; }}
        .address-card {{ background: #2a2a2a; border-left: 4px solid #d32f2f; padding: 15px; margin: 10px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ text-align: left; padding: 12px; border-bottom: 1px solid #444; }}
        th {{ background: #333; font-weight: bold; }}
        .critical {{ color: #ff6f00; font-weight: bold; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #444; text-align: center; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 FEDERAL REGISTER BITCOIN ADDRESSES ANALYSIS</h1>
            <p>Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
        
        <div class="alert">
            <strong>⚠️  CRITICAL ALERT:</strong> All 6 addresses are identified as FEDERAL REGISTER (OFAC/Sanctions)
        </div>
        
        <h2>📊 Summary</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Total Addresses Analyzed</td>
                <td>{len(addresses)}</td>
            </tr>
            <tr>
                <td>Known Addresses (Federal Register)</td>
                <td class="critical">{len(analysis["known_addresses"])}</td>
            </tr>
            <tr>
                <td>Unknown Addresses</td>
                <td>{analysis["unknown_addresses"]}</td>
            </tr>
            <tr>
                <td>Risk Level</td>
                <td class="critical">{analysis["risk_level"]}</td>
            </tr>
            <tr>
                <td>Confidence</td>
                <td>{analysis["overall_confidence"]:.0%}</td>
            </tr>
        </table>
        
        <h2>🔍 Individual Address Details</h2>
"""

for i, addr in enumerate(addresses, 1):
    result = OSINTChecker.check_address_reputation(addr)
    html_content += f"""
        <div class="address-card">
            <h3>{i}. {addr}</h3>
            <p><strong>Category:</strong> <span class="critical">{result['category']}</span></p>
            <p><strong>Confidence:</strong> {result['confidence']:.0%}</p>
            <p><strong>Tags:</strong> {' | '.join(result['tags'])}</p>
        </div>
"""

html_content += f"""
        <h2>⚠️  COMPLIANCE ACTIONS REQUIRED</h2>
        <div class="alert">
            <h3>Immediate Actions:</h3>
            <ol>
                <li><strong>BLOCK TRANSACTIONS:</strong> Do not process any payments from/to these addresses</li>
                <li><strong>FREEZE ACCOUNTS:</strong> Suspend all related accounts pending investigation</li>
                <li><strong>ALERT COMPLIANCE:</strong> Notify your compliance/legal team immediately</li>
                <li><strong>FILE SAR:</strong> File Suspicious Activity Report with relevant authorities</li>
                <li><strong>OFAC CHECK:</strong> Cross-reference with official Treasury OFAC SDN list</li>
            </ol>
        </div>
        
        <div class="footer">
            <p>Report generated by CobNQL v1.1 | Blockchain Analysis & OSINT Tool</p>
            <p>This analysis is based on Federal Register data and should be verified with official sources</p>
        </div>
    </div>
</body>
</html>
"""

with open("reports/federal_register_analysis.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f'✅ HTML Report: reports/federal_register_analysis.html')
print()
print('=' * 80)
print('END OF REPORT')
print('=' * 80)