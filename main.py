import pandas as pd
import os
from revenue_calculator import RevenueCalculator
from excel import ExcelGenerator
from generate_charts import ChartGenerator
from hidden_costs import MONTHS_TO_CALCULATE

def main():
    # Scenarios: number of customers acquired per month
    scenarios = {
        "1 customer per month": 1,
        "2 customers per month": 2,
        "3 customers per month": 3, 
        "4 customers per month": 4,
        "6 customers per month": 6,
    }

    # Calculate revenue for all scenarios
    dfs = {}
    for label, rate in scenarios.items():
        calculator = RevenueCalculator(customers_per_month=rate, months=MONTHS_TO_CALCULATE)
        dfs[label] = calculator.calculate_revenue()
    
    # Generate Excel and charts
    excel_generator = ExcelGenerator()
    excel_generator.generate_excel(dfs)
    
    # Generate charts using ChartGenerator
    chart_generator = ChartGenerator()
    chart_generator.generate_revenue_charts(dfs)
    
    print("\nAll reports and charts have been generated successfully!")
    print("Charts saved in the 'output' directory")

if __name__ == "__main__":
    main()
