"""
Enhanced Report Generator
Generate reports in various formats (TXT, JSON, CSV, HTML)
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


class EnhancedReportGenerator:
    """Extended report generator with JSON and ASCII support"""
    
    @staticmethod
    def generate_json_report(analyses: List[Dict[str, Any]], filename: str) -> str:
        """Generate JSON report"""
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "report_count": len(analyses),
            "transactions": analyses
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @staticmethod
    def generate_csv_report(analyses: List[Dict[str, Any]], filename: str) -> str:
        """Generate CSV report"""
        import csv
        
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        if not analyses:
            return filepath
        
        fieldnames = list(analyses[0].keys())
        
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for analysis in analyses:
                row = {}
                for key, value in analysis.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        row[key] = value
                writer.writerow(row)
        
        return filepath
    
    @staticmethod
    def generate_graph_report(addresses: Dict[str, List[str]], filename: str = "graph.txt") -> str:
        """Generate ASCII address graph"""
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("ADDRESS GRAPH ANALYSIS\n")
            f.write("=" * 50 + "\n\n")
            
            for cluster_name, addrs in addresses.items():
                f.write(f"📍 {cluster_name}\n")
                f.write(f"   └─ Addresses: {len(addrs)}\n")
                
                for i, addr in enumerate(addrs[:5]):
                    prefix = "   ├─" if i < 4 else "   └─"
                    display_addr = addr[:20] + "..." if len(addr) > 20 else addr
                    f.write(f"{prefix} {display_addr}\n")
                
                if len(addrs) > 5:
                    f.write(f"   └─ ... and {len(addrs) - 5} more addresses\n")
                
                f.write("\n")
        
        return filepath
    
    @staticmethod
    def generate_osint_report(osint_data: Dict[str, Any], filename: str = "osint.txt") -> str:
        """Generate OSINT report"""
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("OSINT ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            
            if "known_addresses" in osint_data:
                known_addrs = osint_data["known_addresses"]
                if isinstance(known_addrs, list):
                    f.write("🚨 KNOWN ADDRESSES\n")
                    f.write("-" * 50 + "\n")
                    for addr_info in known_addrs:
                        f.write(f"  {addr_info['address']}: {addr_info['category']}\n")
                    f.write("\n")
            
            if "risk_flags" in osint_data:
                f.write("⚠️  RISK FLAGS\n")
                f.write("-" * 50 + "\n")
                for flag in osint_data["risk_flags"]:
                    f.write(f"  • {flag}\n")
                f.write("\n")
            
            if "risk_level" in osint_data:
                f.write("📊 RISK ASSESSMENT\n")
                f.write("-" * 50 + "\n")
                f.write(f"Overall Risk Level: {osint_data.get('risk_level', 'Unknown')}\n")
                f.write(f"Confidence: {osint_data.get('overall_confidence', 0):.2%}\n\n")
            
            if "recommendations" in osint_data:
                f.write("💡 RECOMMENDATIONS\n")
                f.write("-" * 50 + "\n")
                for rec in osint_data["recommendations"]:
                    f.write(f"  • {rec}\n")
        
        return filepath
    
    @staticmethod
    def generate_html_report(analyses: List[Dict[str, Any]], filename: str = "report.html") -> str:
        """Generate HTML report"""
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CobNQL Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .transaction {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        td, th {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
        .risk-high {{ color: #dc3545; font-weight: bold; }}
        .footer {{ margin-top: 40px; text-align: center; color: #666; border-top: 1px solid #ddd; padding-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 CobNQL Analysis Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
        
        for i, analysis in enumerate(analyses, 1):
            html_content += f"""
            <div class="transaction">
                <h3>📊 Transaction {i}</h3>
                <table>
            """
            
            for key, value in analysis.items():
                if key == "Analysis Notes" and isinstance(value, list):
                    html_content += "<tr><td><b>Analysis Notes</b></td><td>"
                    for note in value:
                        html_content += f"<div>{note}</div>"
                    html_content += "</td></tr>"
                elif isinstance(value, (list, dict)):
                    html_content += f"<tr><td><b>{key}</b></td><td><pre>{json.dumps(value, ensure_ascii=False, indent=2)}</pre></td></tr>"
                else:
                    html_content += f"<tr><td><b>{key}</b></td><td>{value}</td></tr>"
            
            html_content += """
                </table>
            </div>
            """
        
        html_content += """
                <div class="footer">
                    <p>Report generated by CobNQL v1.1</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return filepath