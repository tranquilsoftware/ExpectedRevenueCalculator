import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, ClassVar

# Base Constants
SETUP_FEE = 2249
BASE_MONTHLY_HOSTING_FEE = 29.95
PREMIUM_MONTHLY_HOSTING_FEE = 119.95
MONTHS_TO_CALCULATE = 36

# Domain Costs (negative costs)
ANNUAL_DOMAIN_COST = 100.00
MONTHLY_DOMAIN_COST = (ANNUAL_DOMAIN_COST / 12)  # ~$8.33 per month

# Probabilities (as decimal percentages)
PREMIUM_PROBABILITY = 0.15  # 15% chance for premium hosting
WEB_DEV_CARE_PKG_PROB = 0.10  # 10% chance for web dev care package
EXTRA_PAGE_PROB = 0.25  # 25% chance per customer for extra pages
ANALYTICS_PROB = 0.20  # 20% chance for analytics dashboard
SEO_UPDATE_PROB = 0.05  # 5% chance for SEO update package
SEO_ARTICLES_PROB = 0.01  # 1% chance for article package

# Service Prices
WEB_DEV_CARE_PKG = 247.00
EXTRA_PAGE_PRICE = 147.00

# Analytics
ANALYTICS_DASHBOARD_PRICE = 47.00

# SEO
SEO_UPDATE_PACKAGE_PRICE = 497.00
SEO_ARTICLES_PACKAGE_PRICE = 3000.00

# Revenue stream configuration
REVENUE_STREAMS = {
    'Base Hosting Revenue': {
        'color': '#1f77b4',
        'display_name': 'Base Hosting'
    },
    'Revenue: Premium Hosting': {
        'color': '#ff7f0e',
        'display_name': 'Premium Hosting'
    },
    'Revenue: Web Dev Care': {
        'color': '#2ca02c',
        'display_name': 'Web Dev Care'
    },
    'Revenue: Analytics': {
        'color': '#d62728',
        'display_name': 'Analytics'
    },
    'Revenue: SEO Updates': {
        'color': '#9467bd',
        'display_name': 'SEO Updates'
    },
    'Revenue: SEO Articles': {
        'color': '#8c564b',
        'display_name': 'SEO Articles'
    },
    # 'Monthly One-Time Revenue': {
    #     'color': '#e377c2',
    #     'display_name': 'One-Time'
    # }
}

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

# Define all upsell packages
UPSELL_PACKAGES = {
    'premium_hosting': UpsellPackage(
        name="Premium Hosting",
        monthly_price=PREMIUM_MONTHLY_HOSTING_FEE - BASE_MONTHLY_HOSTING_FEE,
        probability=PREMIUM_PROBABILITY,
        revenue_stream="Revenue: Premium Hosting"
    ),
    'web_dev_care': UpsellPackage(
        name="Web Dev Care Package",
        monthly_price=WEB_DEV_CARE_PKG,
        probability=WEB_DEV_CARE_PKG_PROB,
        revenue_stream="Revenue: Web Dev Care"
    ),
    'extra_pages': UpsellPackage(
        name="Extra Pages",
        one_time_price=EXTRA_PAGE_PRICE,
        probability=EXTRA_PAGE_PROB,
        is_quantity_based=True,
        max_quantity=3,
        revenue_stream="Monthly One-Time Revenue"
    ),
    'analytics': UpsellPackage(
        name="Analytics Dashboard",
        monthly_price=ANALYTICS_DASHBOARD_PRICE,
        probability=ANALYTICS_PROB,
        revenue_stream="Revenue: Analytics"
    ),
    'seo_updates': UpsellPackage(
        name="SEO Update Package",
        monthly_price=SEO_UPDATE_PACKAGE_PRICE,
        probability=SEO_UPDATE_PROB,
        revenue_stream="Revenue: SEO Updates"
    ),
    'seo_articles': UpsellPackage(
        name="SEO Articles Package",
        monthly_price=SEO_ARTICLES_PACKAGE_PRICE,
        probability=SEO_ARTICLES_PROB,
        revenue_stream="Revenue: SEO Articles"
    )
}

# Service Names (for reference)
class ServiceNames:
    PREMIUM_HOSTING = "Premium Hosting"
    WEB_DEV_CARE = "Web Dev Care Package"
    EXTRA_PAGES = "Extra Pages"
    ANALYTICS = "Analytics Dashboard"
    SEO_UPDATES = "SEO Update Package"
    SEO_ARTICLES = "SEO Articles Package"

@dataclass
class CustomerUpsells:
    """Tracks all potential upsells for a single customer"""
    _packages: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        # Initialize all packages with 0 quantity
        self._packages = {name: 0 for name in UPSELL_PACKAGES}
    
    def add_upsell(self, package_name: str, quantity: int = 1) -> None:
        """Add an upsell package"""
        if package_name in self._packages:
            if UPSELL_PACKAGES[package_name].is_quantity_based:
                self._packages[package_name] = min(
                    self._packages[package_name] + quantity,
                    UPSELL_PACKAGES[package_name].max_quantity
                )
            else:
                self._packages[package_name] = 1
    
    def get_quantity(self, package_name: str) -> int:
        """Get quantity of a specific package"""
        return self._packages.get(package_name, 0)
    
    def get_monthly_revenue(self) -> Dict[str, float]:
        """Calculate monthly revenue by package"""
        revenue = {}
        for name, pkg in UPSELL_PACKAGES.items():
            if self._packages[name] > 0 and pkg.monthly_price > 0:
                revenue[pkg.revenue_stream] = pkg.monthly_price * self._packages[name]
        return revenue
    
    def get_one_time_revenue(self) -> Dict[str, float]:
        """Calculate one-time revenue by package"""
        revenue = {}
        for name, pkg in UPSELL_PACKAGES.items():
            if self._packages[name] > 0 and pkg.one_time_price > 0:
                revenue[pkg.revenue_stream] = pkg.one_time_price * self._packages[name]
        return revenue
    
    def calculate_monthly_upsell_total(self) -> float:
        """Calculate total monthly cost of all active upsells"""
        total = sum(
            pkg.monthly_price * self._packages[name]
            for name, pkg in UPSELL_PACKAGES.items()
        )
        # Add domain cost (negative cost)
        total -= MONTHLY_DOMAIN_COST
        return total
        
    def calculate_one_time_fees(self) -> float:
        """Calculate one-time fees (setup fee + extra pages)"""
        one_time_total = sum(
            pkg.one_time_price * self._packages[name]
            for name, pkg in UPSELL_PACKAGES.items()
        )
        return SETUP_FEE + one_time_total - ANNUAL_DOMAIN_COST

def generate_customer_upsells() -> CustomerUpsells:
    """
    Generate a random set of upsells for a new customer based on probabilities.
    Returns a CustomerUpsells object with the selected services.
    """
    upsells = CustomerUpsells()
    
    # Generate upsells based on package probabilities
    for name, pkg in UPSELL_PACKAGES.items():
        if pkg.is_quantity_based:
            # For quantity-based packages (like extra pages)
            for _ in range(pkg.max_quantity):
                if random.random() < pkg.probability:
                    upsells.add_upsell(name, 1)
        else:
            # For simple yes/no packages
            if random.random() < pkg.probability:
                upsells.add_upsell(name)
    
    # SEO services are mutually exclusive - if both were selected, keep only one
    if (upsells.get_quantity('seo_updates') > 0 and 
        upsells.get_quantity('seo_articles') > 0):
        # Keep only one SEO service (50/50 chance for each)
        if random.random() < 0.5:
            upsells._packages['seo_articles'] = 0
        else:
            upsells._packages['seo_updates'] = 0
    
    return upsells

def get_upsell_description(upsells: CustomerUpsells) -> str:
    """Generate a human-readable description of the customer's upsells"""
    descriptions = []
    
    if upsells.premium_hosting:
        descriptions.append(f"{ServiceNames.PREMIUM_HOSTING} (${PREMIUM_MONTHLY_HOSTING_FASE_MONTHLY_HOSTING_FEE - BASE_MONTHLY_HOSTING_FEE} upgrade)")
    if upsells.web_dev_care:
        descriptions.append(f"{ServiceNames.WEB_DEV_CARE} (${WEB_DEV_CARE_PKG}/mo)")
    if upsells.extra_pages > 0:
        descriptions.append(f"{upsells.extra_pages} {ServiceNames.EXTRA_PAGES} (${upsells.extra_pages * EXTRA_PAGE_PRICE}/mo)")
    if upsells.analytics:
        descriptions.append(f"{ServiceNames.ANALYTICS} (${ANALYTICS_DASHBOARD_PRICE}/mo)")
    if upsells.seo_updates:
        descriptions.append(f"{ServiceNames.SEO_UPDATES} (${SEO_UPDATE_PACKAGE_PRICE}/mo)")
    if upsells.seo_articles:
        descriptions.append(f"{ServiceNames.SEO_ARTICLES} (${SEO_ARTICLES_PACKAGE_PRICE}/mo)")
    
    return ", ".join(descriptions) if descriptions else "No additional services"

# For backward compatibility
def get_monthly_hosting_fee(probability: float = PREMIUM_PROBABILITY) -> float:
    """Legacy function - returns either base or premium hosting fee"""
    return (PREMIUM_MONTHLY_HOSTING_FEE 
            if random.random() < probability 
            else BASE_MONTHLY_HOSTING_FEE)
