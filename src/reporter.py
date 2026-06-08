import os
from datetime import datetime
from typing import List, Dict, Any

class ReportGenerator:
    @staticmethod
    def generate_txt_report(analyses: List[Dict[str, Any]], filename: str):
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"COBNQL REPORT | Date: {datetime.now()}\n")
            f.write("="*40 + "\n")
            for res in analyses:
                for key, val in res.items():
                    f.write(f"{key}: {val}\n")
                f.write("-" * 20 + "\n")
        
        return filepath