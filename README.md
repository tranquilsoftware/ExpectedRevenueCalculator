# Expected Revenue Calculator

A comprehensive Python tool for projecting and visualizing revenue growth based on different customer acquisition scenarios, including various revenue streams and one-time fees. The tool now features a modular design that allows for easy customization of business models and revenue streams.

## 🚀 Features

- **Modular Business Models**: Easily switch between different business models
- **Customizable Revenue Streams**: Define your own hosting plans, add-ons, and pricing
- **Flexible Configuration**: Adjust probabilities, pricing, and service offerings
- **Multiple Scenarios**: Compare different customer acquisition rates (1-6+ customers/month)
- **Detailed Visualizations**: Interactive charts with revenue breakdowns
- **Comprehensive Reports**: Excel exports with detailed financial projections
- **Type Hints**: Full type support for better code maintainability

## 🛠️ Project Structure

- `main.py`: Main entry point for the application
- `config.py`: Central configuration and model selection
- `models.py`: Core business logic and data models
  - `UpsellPackage`: Represents a sellable package with pricing and type
  - `CustomerUpsells`: Tracks customer purchases and calculates revenue
  - `ServiceNames`: Centralized service name definitions
- `revenue_calculator.py`: Handles revenue projections and calculations
- `generate_charts.py`: Visualization and chart generation
- `excel.py`: Excel report generation
- `output/`: Generated reports and charts

## ⚙️ Configuration

### Business Models

Edit `config.py` to define your business model:

```python
# Example Web Design Business Model
WEB_DESIGN_MODEL = {
    'hosting_plans': [
        {
            'name': 'basic',
            'price': 29.95,
            'type': 'recurring',
            'display_name': 'Base Hosting',
            'color': '#1f77b4',
            'probability': 0.85
        },
        # ... more plans
    ],
    'addons': [
        {
            'name': 'web_dev_care',
            'price': 247.00,
            'type': 'recurring',
            'display_name': 'Web Dev Care',
            'color': '#2ca02c',
            'probability': 0.10
        },
        # ... more addons
    ]
}

# Select active model
CURRENT_MODEL = WEB_DESIGN_MODEL
```

### Scenarios

Modify `main.py` to adjust customer acquisition scenarios:

```python
scenarios = {
    "1 customer/month": 1,
    "2 customers/month": 2,
    "3 customers/month": 3,
    "4 customers/month": 4,
    "6 customers/month": 6
}
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ExpectedRevenueCalculator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the calculator**
   ```bash
   python main.py
   ```

## 📊 Output

The tool generates:
- Interactive charts in `output/` directory
- Detailed Excel reports with revenue breakdowns
- Visual comparisons across different scenarios

## 🎨 Customization

### Adding New Business Models

1. Define your model in `config.py` following the existing structure
2. Add it to the model selection in `config.py`
3. The system will automatically handle the rest

### Modifying Revenue Streams

Update the `CURRENT_MODEL` configuration in `config.py` to:
- Add/remove plans
- Adjust pricing and probabilities
- Define new add-ons and services

## 📦 Dependencies

- Python 3.7+
- pandas: Data manipulation and Excel export
- openpyxl: Excel file support
- matplotlib: Chart generation
- numpy: Numerical operations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
- matplotlib: Data visualization
- openpyxl: Excel file handling
- numpy: Numerical operations

## License

This project is for demonstration purposes. Please ensure you have the right to use and modify the code as needed for your specific use case.
