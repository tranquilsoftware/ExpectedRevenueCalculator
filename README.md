# Expected Revenue Calculator

A comprehensive Python tool for projecting and visualizing revenue growth based on different customer acquisition scenarios, including various revenue streams and one-time fees.

## Features

- Multiple customer acquisition scenarios (1-6 customers per month)
- Detailed revenue breakdown by stream (Hosting, Premium, Web Dev Care, Analytics, SEO)
- Interactive visualizations with dual-axis charts
- Comprehensive Excel reports with auto-adjusted column widths
- Support for both recurring and one-time revenue streams
- Configurable probabilities for different service up-sells

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

## Project Structure

- `main.py`: Main script to run the revenue calculator
- `revenue_calculator.py`: Core revenue calculation logic
- `generate_charts.py`: Visualization and chart generation
- `excel.py`: Excel report generation
- `hidden_costs.py`: Configuration for pricing, probabilities, and revenue streams
- `output/`: Directory containing generated charts and reports

## Configuration

### Revenue Streams

Modify `hidden_costs.py` to adjust:
- Base and premium hosting fees
- Setup fees
- Service probabilities and pricing
- Revenue stream configurations

### Scenarios

Modify the `scenarios` dictionary in `main.py` to change the customer acquisition rates:

```python
scenarios = {
    "1 customer per month": 1,
    "2 customers per month": 2,
    "3 customers per month": 3,
    "4 customers per month": 4,
    "6 customers per month": 6
}
```

## Usage

Run the calculator:
```bash
python main.py
```

### Output Files

- `output/` directory will contain:
  - `revenue_breakdown_*.png`: Individual revenue breakdown charts for each scenario
  - `revenue_comparison.png`: Comparison of monthly revenue across all scenarios
  - `cumulative_revenue_projection.png`: Cumulative revenue projection by scenario
  - `customer_revenue_breakdown.xlsx`: Excel file with detailed revenue breakdown by scenario

## Customization

### Chart Styling

Modify `generate_charts.py` to adjust:
- Figure sizes and layouts
- Color schemes
- Line styles and markers
- Axis formatting and labels
- Legend position and styling

### Revenue Streams

Update `REVENUE_STREAMS` in `hidden_costs.py` to add or modify revenue streams, including:
- Display names
- Colors
- Associated revenue calculations

## Dependencies

- pandas: Data manipulation and Excel export
- matplotlib: Data visualization
- openpyxl: Excel file handling
- python-dotenv: Environment variable management
- numpy: Numerical operations

## License

This project is for demonstration purposes. Please ensure you have the right to use and modify the code as needed for your specific use case.
