"""
Configuration settings for the Revenue Calculator application.

This file contains model selection and other configuration settings.
"""
from typing import TypedDict, List, Dict, Any

class PlanConfig(TypedDict):
    name: str
    price: float
    type: str  # 'onetime' or 'recurring'
    display_name: str
    description: str
    color: str
    probability: float

# Web Design Development Business Model
WEB_DESIGN_MODEL = {
    'plans': [
        {
            'name': 'basic',
            'price': 29.95,
            'type': 'recurring',
            'display_name': 'Base Hosting',
            'description': 'Basic hosting package',
            'color': '#1f77b4',
            'probability': 0.85  # 85% chance for basic hosting
        },
        {
            'name': 'premium',
            'price': 119.95,
            'type': 'recurring',
            'display_name': 'Premium Hosting',
            'description': 'Premium hosting package',
            'color': '#ff7f0e',
            'probability': 0.15  # 15% chance for premium
        }
    ],
    'addons': [
        {
            'name': 'web_dev_care',
            'price': 247.00,
            'type': 'recurring',
            'display_name': 'Web Dev Care',
            'description': 'Web development care package',
            'color': '#2ca02c',
            'probability': 0.10
        },
        {
            'name': 'extra_pages',
            'price': 147.00,
            'type': 'onetime',
            'display_name': 'Extra Pages',
            'description': 'Additional web pages',
            'color': '#d62728',
            'probability': 0.25,
            'max_quantity': 3
        },
        {
            'name': 'analytics',
            'price': 47.00,
            'type': 'recurring',
            'display_name': 'Analytics',
            'description': 'Analytics dashboard',
            'color': '#9467bd',
            'probability': 0.20
        },
        {
            'name': 'seo_updates',
            'price': 497.00,
            'type': 'recurring',
            'display_name': 'SEO Updates',
            'description': 'Monthly SEO updates',
            'color': '#8c564b',
            'probability': 0.05
        },
        {
            'name': 'seo_articles',
            'price': 3000.00,
            'type': 'recurring',
            'display_name': 'SEO Articles',
            'description': 'Monthly SEO articles',
            'color': '#e377c2',
            'probability': 0.01
        }
    ]
}

# Buddy Business Model
BUDDY_MODEL = {
    'plans': [
        {
            'name': 'basic',
            'price': 39.00,
            'type': 'recurring',
            'display_name': 'Basic',
            'description': 'Basic package',
            'color': '#1f77b4',
            'probability': 0.70  # 70%
        },
        {
            'name': 'pro',
            'price': 97.00,
            'type': 'recurring',
            'display_name': 'Pro',
            'description': 'Professional package',
            'color': '#ff7f0e',
            'probability': 0.25  # 25%
        },
        {
            'name': 'diamond',
            'price': 177.00,
            'type': 'recurring',
            'display_name': 'Diamond',
            'description': 'Premium package',
            'color': '#b4a7d6',
            'probability': 0.05  # 5%
        }
    ],
    'addons': [
        # Add buddy specific addons here
    ]
}

# =============================================
# MODEL SELECTION
# =============================================
# Choose which business model to use by uncommenting one of the following lines:
# CURRENT_MODEL = WEB_DESIGN_MODEL  # Web Design Development Business Model
CURRENT_MODEL = BUDDY_MODEL        # Buddy Business Model

# Extract hosting plans and addons for the selected model
PLANS = CURRENT_MODEL['plans']
ADDONS = CURRENT_MODEL['addons']

# Verify that the selected model's hosting plan probabilities sum to 1.0
try:
    TOTAL_PROB = sum(plan['probability'] for plan in PLANS)
    if not (0.99 <= TOTAL_PROB <= 1.01):  # Allow for small floating point errors
        raise ValueError(f"Hosting plan probabilities must sum to 1.0, got {TOTAL_PROB}")
except Exception as e:
    print(f"Error in model configuration: {e}")
    raise

# =============================================
# OTHER CONFIGURATION SETTINGS
# =============================================
SETUP_FEE = 2249
MONTHS_TO_CALCULATE = 36
ANNUAL_DOMAIN_COST = 150
MONTHLY_DOMAIN_COST = (ANNUAL_DOMAIN_COST / 12)  # ~$12.50 per month

def get_revenue_streams() -> Dict[str, Dict[str, Any]]:
    """
    Generate revenue streams dictionary from the current model's plans and addons.
    Returns a dictionary with display names as keys and their metadata as values.
    """
    revenue_streams = {}
    
    # Add plans
    for plan in PLANS:
        revenue_streams[plan['display_name']] = {
            'color': plan['color'],
            'display_name': f"{plan['display_name']} (${plan['price']})",
            'type': plan['type'],
            'price': plan['price']
        }
    
    # Add addons
    for addon in ADDONS:
        revenue_streams[addon['display_name']] = {
            'color': addon['color'],
            'display_name': f"{addon['display_name']} (${addon['price']})",
            'type': addon['type'],
            'price': addon['price']
        }
    
    return revenue_streams

# Generate revenue streams for the current model
REVENUE_STREAMS = get_revenue_streams()

# Customer acquisition scenarios
SCENARIOS = {
    "1 customer per month": 1,
    "2 customers per month": 2,
    "3 customers per month": 3,
    "4 customers per month": 4,
    "6 customers per month": 6,
    "10 customers per month": 10,
}

# Export all configuration values
__all__ = [
    'SETUP_FEE',
    'MONTHS_TO_CALCULATE',
    'ANNUAL_DOMAIN_COST',
    'MONTHLY_DOMAIN_COST',
    'PLANS',
    'ADDONS',
    'CURRENT_MODEL',
    'WEB_DESIGN_MODEL',
    'BUDDY_MODEL',
    'REVENUE_STREAMS',
    'SCENARIOS',
    'get_revenue_streams'
]
