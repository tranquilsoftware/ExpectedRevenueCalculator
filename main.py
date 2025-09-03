import pandas as pd
import matplotlib.pyplot as plt
from openpyxl.utils import get_column_letter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

### Constants
# Data stored in env for privacy..
setup_fee = int(os.getenv('SETUP_FEE'))
monthly_hosting_fee = float(os.getenv('MONTHLY_HOSTING_FEE'))
months_to_calculate = int(os.getenv('MONTHS_TO_CALCULATE'))

output_files = {
    "excel": "customer_revenue_breakdown.xlsx",
    "total_revenue_chart": "total_revenue_growth_chart.png",
    "hosting_revenue_chart": "monthly_hosting_revenue_chart.png"
}

# Scenarios: number of customers acquired per month
scenarios = {
    "2 customers per month": 2,
    "3 customers per month": 3, 
    "4 customers per month": 4,
    "6 customers per month": 6,
}

# Function to build revenue data for a given acquisition rate
def build_revenue_data(customers_per_month):
    months = months_to_calculate
    data = []

    total_customers = 0
    cumulative_one_time = 0
    cumulative_hosting = 0

    for month in range(1, months + 1):
        new_customers = customers_per_month
        total_customers += new_customers

        # Revenue calculations
        one_time_revenue = new_customers * setup_fee
        cumulative_one_time += one_time_revenue

        monthly_hosting_revenue = total_customers * monthly_hosting_fee
        cumulative_hosting += monthly_hosting_revenue

        total_revenue = cumulative_one_time + cumulative_hosting

        data.append({
            "Month": month,
            "Total Customers": total_customers,
            "One-Time Revenue (Cumulative)": cumulative_one_time,
            "Monthly Hosting Revenue": round(monthly_hosting_revenue, 2),
            "Hosting Revenue (Cumulative)": round(cumulative_hosting, 2),
            "Total Revenue": round(total_revenue, 2)
        })

    return pd.DataFrame(data)

# Create dataframes for all scenarios
dfs = {label: build_revenue_data(rate) for label, rate in scenarios.items()}

# Plot Total Revenue Growth with Customer Count
plt.figure(figsize=(14, 7))

# Create primary y-axis (left)
ax1 = plt.gca()
ax1.set_xlabel('Month')
ax1.set_ylabel('Total Revenue ($)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Plot all scenarios on primary y-axis
for label, df in dfs.items():
    ax1.plot(df['Month'], df['Total Revenue'], 
             label=f'{label} Revenue', linestyle='-', linewidth=2)

# Create secondary y-axis (right)
ax2 = ax1.twinx()
ax2.set_ylabel('Total Customers', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Plot all scenarios on secondary y-axis
for label, df in dfs.items():
    ax2.plot(df['Month'], df['Total Customers'], 
             label=f'{label} Customers', linestyle='--', linewidth=1.5, alpha=0.7)

# Add title and grid
plt.title('Total Revenue & Customer Growth by Scenario')
ax1.grid(True, alpha=0.3)

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, 
           bbox_to_anchor=(0.5, -0.15), 
           loc='upper center', 
           ncol=4)

plt.tight_layout()
plt.savefig(output_files["total_revenue_chart"], bbox_inches='tight')
print("Saved chart as: " + output_files["total_revenue_chart"])
plt.clf()

# Plot Monthly Hosting Revenue with Customer Count
plt.figure(figsize=(14, 7))

# Create primary y-axis (left)
ax1 = plt.gca()
ax1.set_xlabel('Month')
ax1.set_ylabel('Monthly Hosting Revenue ($)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Plot all scenarios on primary y-axis
for label, df in dfs.items():
    ax1.plot(df['Month'], df['Monthly Hosting Revenue'], 
             label=f'{label} Revenue', linestyle='-', linewidth=2)

# Create secondary y-axis (right)
ax2 = ax1.twinx()
ax2.set_ylabel('Total Customers', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Plot all scenarios on secondary y-axis
for label, df in dfs.items():
    ax2.plot(df['Month'], df['Total Customers'], 
             label=f'{label} Customers', linestyle='--', linewidth=1.5, alpha=0.7)

# Add title and grid
plt.title('Monthly Hosting Revenue & Total Customers by Scenario')
ax1.grid(True, alpha=0.3)

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, 
           bbox_to_anchor=(0.5, -0.15), 
           loc='upper center', 
           ncol=4)

plt.tight_layout()
plt.savefig(output_files["hosting_revenue_chart"], bbox_inches='tight')
print("Saved chart as: " + output_files["hosting_revenue_chart"])
plt.clf()

# Save Excel with auto-adjusted column widths
with pd.ExcelWriter(output_files["excel"], engine="openpyxl") as writer:
    for label, df in dfs.items():
        df.to_excel(writer, sheet_name=label, index=False)

        worksheet = writer.sheets[label]
        for i, column in enumerate(df.columns):
            max_length = max(
                df[column].astype(str).map(len).max(),
                len(column)
            )
            adjusted_width = max_length + 2
            col_letter = get_column_letter(i + 1)
            worksheet.column_dimensions[col_letter].width = adjusted_width

print("Saved Excel file as: " + output_files["excel"])
