import pandas as pd
from openpyxl.utils import get_column_letter
from typing import Dict, Any, List
import os

class ExcelGenerator:
    def __init__(self, output_file: str = "customer_revenue_breakdown.xlsx"):
        self.output_file = output_file

    def generate_excel(self, data_frames: Dict[str, pd.DataFrame]) -> None:
        """Generate Excel file with multiple sheets for different scenarios"""
        with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
            for scenario_name, df in data_frames.items():
                sheet_name = scenario_name[:31]  # Excel sheet name limit
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets[sheet_name]
                for i, col in enumerate(df.columns, 1):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(str(col))
                    ) + 2
                    worksheet.column_dimensions[get_column_letter(i)].width = min(max_length, 30)
        
        print(f"\nExcel file generated: {self.output_file}")