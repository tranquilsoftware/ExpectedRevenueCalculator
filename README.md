# Expected Revenue Calculator

A Python tool for projecting and visualizing revenue growth based on different customer acquisition scenarios.

## Features

- Multiple customer acquisition scenarios (2, 3, 4, or 6 customers per month)
- Dual-axis visualizations showing both revenue and customer growth
- Detailed Excel reports with auto-adjusted column widths
- Environment variable configuration for sensitive data

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ExpectedRevenueCalculator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a new `.env` file with:
   ```
   SETUP_FEE=2249
   MONTHLY_HOSTING_FEE=29.95
   MONTHS_TO_CALCULATE=36
   ```

2. Modify the values in `.env` as needed for your scenario.

## Usage

Run the calculator:
```bash
python main.py
```

### Output Files

- `total_revenue_growth_chart.png`: Chart showing total revenue growth over time
- `monthly_hosting_revenue_chart.png`: Chart showing monthly hosting revenue and customer growth
- `customer_revenue_breakdown.xlsx`: Excel file with detailed revenue breakdown by scenario

## Customization

### Scenarios
Modify the `scenarios` dictionary in `main.py` to change the customer acquisition rates:

```python
scenarios = {
    "2 customers per month": 2,
    "3 customers per month": 3,
    "6 customers per month": 6,
    # Add or modify scenarios as needed
}
```

### Chart Styling
Adjust the chart appearance by modifying the plotting code in `main.py`:
- Figure size
- Colors
- Line styles
- Grid opacity
- Legend position

## Dependencies

- pandas: Data manipulation and Excel export
- matplotlib: Data visualization
- openpyxl: Excel file handling
- python-dotenv: Environment variable management

## License

This project is for demonstration purposes. Please ensure you have the right to use and modify the code as needed for your specific use case.
