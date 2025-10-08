"""
Business models and related data structures for the Revenue Calculator.
"""
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, ClassVar, TypedDict, Any

# Import configuration from config.py
from config import (
    SETUP_FEE,
    MONTHS_TO_CALCULATE,
    ANNUAL_DOMAIN_COST,
    MONTHLY_DOMAIN_COST,
    PLANS,
    ADDONS,
    CURRENT_MODEL,
    get_revenue_streams,
    REVENUE_STREAMS
)

# Calculate base hosting fee from the first plan
BASE_MONTHLY_HOSTING_FEE = PLANS[0]['price'] if PLANS else 0.0

# Export BASE_MONTHLY_HOSTING_FEE
__all__ = [
    'BASE_MONTHLY_HOSTING_FEE',
    'PlanConfig',
    'upsellPackage',
    'UPSELL_PACKAGES',
    'ServiceNames',
    'CustomerUpsells',
    'generate_customer_upsells',
    'get_upsell_description',
    'select_random_plan'
]

# Premium plan fee (if available)
premium_plans = [p for p in PLANS if p.get('name') == 'premium' or p.get('name') == 'pro']
PREMIUM_MONTHLY_HOSTING_FEE = premium_plans[0]['price'] if premium_plans else 0

# Get REVENUE_STREAMS from config
REVENUE_STREAMS = get_revenue_streams()

@dataclass
class UpsellPackage:
    """Represents an upsell package with its pricing and type."""
    name: str
    monthly_price: float = 0.0
    one_time_price: float = 0.0
    probability: float = 0.0
    is_quantity_based: bool = False
    max_quantity: int = 1
    revenue_stream: str = ""
    
    def calculate_revenue(self, quantity: int = 1) -> Tuple[float, float]:
        """Calculate monthly and one-time revenue for the given quantity."""
        qty = min(quantity, self.max_quantity) if self.max_quantity > 1 else quantity
        return (self.monthly_price * qty, self.one_time_price * qty)

# Create upsell packages from the current model
UPSELL_PACKAGES = {}
for addon in ADDONS:
    UPSELL_PACKAGES[addon['name']] = UpsellPackage(
        name=addon['display_name'],
        monthly_price=addon['price'] if addon['type'] == 'recurring' else 0,
        one_time_price=addon['price'] if addon['type'] == 'onetime' else 0,
        probability=addon['probability'],
        is_quantity_based=addon.get('max_quantity', 1) > 1,
        max_quantity=addon.get('max_quantity', 1),
        revenue_stream=addon['display_name']
    )

# Service Names (for reference)
class ServiceNames:
    # These will be populated based on the current model
    pass

# Dynamically add service names based on the current model
for plan in PLANS + ADDONS:
    name = plan['name'].upper()
    display_name = plan['display_name']
    setattr(ServiceNames, name, display_name)

@dataclass
class CustomerUpsells:
    """Tracks all potential upsells for a single customer"""
    _packages: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        # Initialize all addons with 0 quantity
        self._packages = {addon['name']: 0 for addon in ADDONS}
    
    def add_upsell(self, package_name: str, quantity: int = 1) -> None:
        """Add an upsell package"""
        if package_name in self._packages:
            addon = next((a for a in ADDONS if a['name'] == package_name), None)
            if addon:
                if addon.get('max_quantity', 1) > 1:  # Quantity-based addon
                    self._packages[package_name] = min(
                        self._packages[package_name] + quantity,
                        addon.get('max_quantity', 1)
                    )
                else:
                    self._packages[package_name] = 1
    
    def get_quantity(self, package_name: str) -> int:
        """Get quantity of a specific package"""
        return self._packages.get(package_name, 0)
    
    def get_monthly_revenue(self) -> Dict[str, float]:
        """Calculate monthly revenue by package"""
        revenue = {}
        for addon in ADDONS:
            name = addon['name']
            if self._packages.get(name, 0) > 0 and addon['type'] == 'recurring':
                revenue[addon['display_name']] = addon['price'] * self._packages[name]
        return revenue
    
    def get_one_time_revenue(self) -> Dict[str, float]:
        """Calculate one-time revenue by package"""
        revenue = {}
        for addon in ADDONS:
            name = addon['name']
            if self._packages.get(name, 0) > 0 and addon['type'] == 'onetime':
                revenue[addon['display_name']] = addon['price'] * self._packages[name]
        return revenue
    
    def calculate_monthly_upsell_total(self) -> float:
        """Calculate total monthly cost of all active upsells"""
        total = 0.0
        for addon in ADDONS:
            name = addon['name']
            if addon['type'] == 'recurring':
                total += addon['price'] * self._packages.get(name, 0)
        # Add domain cost (negative cost)
        total -= MONTHLY_DOMAIN_COST
        return total
        
    def calculate_one_time_fees(self) -> float:
        """Calculate one-time fees (setup fee + one-time addons)"""
        one_time_total = 0.0
        for addon in ADDONS:
            name = addon['name']
            if addon['type'] == 'onetime':
                one_time_total += addon['price'] * self._packages.get(name, 0)
        return SETUP_FEE + one_time_total - ANNUAL_DOMAIN_COST

def generate_customer_upsells() -> CustomerUpsells:
    """
    Generate a random set of upsells for a new customer based on probabilities.
    Returns a CustomerUpsells object with the selected services.
    """
    upsells = CustomerUpsells()
    
    # Generate upsells based on addon probabilities
    for addon in ADDONS:
        if addon.get('max_quantity', 1) > 1:
            # For quantity-based addons (like extra pages)
            max_qty = addon.get('max_quantity', 1)
            for _ in range(max_qty):
                if random.random() < addon['probability']:
                    upsells.add_upsell(addon['name'], 1)
        else:
            # For simple yes/no addons
            if random.random() < addon['probability']:
                upsells.add_upsell(addon['name'])
    
    # Handle mutually exclusive addons (e.g., SEO services)
    seo_services = [a for a in ADDONS if a['name'].startswith('seo_')]
    if len(seo_services) > 1 and sum(upsells.get_quantity(s['name']) for s in seo_services) > 1:
        # If multiple SEO services are selected, keep only one (randomly chosen)
        selected_seo = random.choice(seo_services)
        for seo in seo_services:
            if seo['name'] != selected_seo['name']:
                upsells._packages[seo['name']] = 0
    
    return upsells

def get_upsell_description(upsells: CustomerUpsells) -> str:
    """Generate a human-readable description of the customer's upsells"""
    descriptions = []
    
    # Add hosting plan if needed (if you track it in upsells)
    
    # Add active addons
    for addon in ADDONS:
        name = addon['name']
        qty = upsells.get_quantity(name)
        if qty > 0:
            price_desc = f"${addon['price'] * qty:.2f}"
            if addon['type'] == 'recurring':
                price_desc += "/mo"
            descriptions.append(f"{addon['display_name']} x{qty} ({price_desc})")
    
    return ", ".join(descriptions) if descriptions else "No additional services"

# For backward compatibility
def select_random_plan() -> Tuple[float, str]:
    """
    Randomly select a plan based on probabilities.
    Returns a tuple of (monthly_price, plan_name)
    """
    rand = random.random()
    cumulative_prob = 0.0
    
    for plan in PLANS:
        cumulative_prob += plan['probability']
        if rand < cumulative_prob:
            return plan['price'], plan['name'].capitalize()
    
    # Fallback to first plan if no plan was selected (shouldn't happen if probabilities sum to 1.0)
    return PLANS[0]['price'], PLANS[0]['name'].capitalize()