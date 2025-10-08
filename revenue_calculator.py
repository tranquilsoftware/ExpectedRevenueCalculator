import random
import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np

# Import from config and hidden_costs
from config import (
    SETUP_FEE,
    MONTHS_TO_CALCULATE,
    PLANS,
    ADDONS,
    CURRENT_MODEL,
    REVENUE_STREAMS
)

from models import (
    BASE_MONTHLY_HOSTING_FEE,
    generate_customer_upsells,
    CustomerUpsells,
    UPSELL_PACKAGES
)

@dataclass
class RevenueMetrics:
    """Class to store revenue metrics for a given month"""
    month: int
    total_customers: int
    new_customers: int
    one_time_revenue: float
    cumulative_one_time: float
    base_hosting_revenue: float
    monthly_upsell_revenue: float
    total_monthly_revenue: float
    cumulative_hosting: float
    active_upsells: Dict[str, int]
    package_revenue: Dict[str, float]

class RevenueCalculator:
    """Handles all revenue calculation logic"""
    
    def __init__(self, customers_per_month: int, months: int = MONTHS_TO_CALCULATE):
        self.customers_per_month = customers_per_month
        self.months = months
        self.customer_cohorts = []
        self.cumulative_one_time = 0
        self.cumulative_hosting = 0
        self.data = []

    def calculate_revenue(self) -> pd.DataFrame:
        """Calculate revenue metrics for all months"""
        for month in range(1, self.months + 1):
            self._process_month(month)
        return pd.DataFrame(self.data)

    def _process_month(self, month: int) -> None:
        """Process a single month's revenue calculations"""
        # Generate new customers and their upsells
        new_customers = []
        for _ in range(self.customers_per_month):
            # Select a random plan for the customer
            plan = random.choices(
                PLANS,
                weights=[p.get('probability', 1.0) for p in PLANS],
                k=1
            )[0]
            
            # Generate upsells for the customer
            upsells = generate_customer_upsells()
            
            # Calculate plan-specific revenue
            plan_monthly_revenue = {}
            plan_one_time_revenue = {}
            
            # Add the plan's monthly fee
            plan_monthly_revenue[plan['name']] = plan['price']
            
            # Get all revenue from upsells
            monthly_revenue = upsells.get_monthly_revenue()
            one_time_revenue = upsells.get_one_time_revenue()
            
            # Add the customer with plan information
            new_customers.append({
                'month_joined': month,
                'plan': plan['name'],
                'upsells': upsells,
                'one_time_fee': upsells.calculate_one_time_fees(),
                'monthly_upsell': upsells.calculate_monthly_upsell_total(),
                'monthly_revenue': {**plan_monthly_revenue, **monthly_revenue},
                'one_time_revenue': one_time_revenue
            })
        
        # Add new customers to cohorts
        self.customer_cohorts.extend(new_customers)
        total_customers = len(self.customer_cohorts)
        
        # Calculate one-time revenue (setup fees + extra pages for new customers)
        new_one_time_revenue = sum(c['one_time_fee'] for c in new_customers)
        self.cumulative_one_time += new_one_time_revenue
        
        # Calculate monthly recurring revenue (base hosting + monthly upsells)
        base_hosting_revenue = total_customers * BASE_MONTHLY_HOSTING_FEE
        monthly_upsell_revenue = sum(c['monthly_upsell'] for c in self.customer_cohorts)
        
        total_monthly_revenue = base_hosting_revenue + monthly_upsell_revenue
        self.cumulative_hosting += total_monthly_revenue
        
        # Initialize revenue tracking
        revenue_by_stream = {stream: 0.0 for stream in REVENUE_STREAMS}
        plan_revenues = {plan['name']: 0.0 for plan in PLANS}
        
        # Track customers by plan
        customers_by_plan = {plan['name']: 0 for plan in PLANS}
        
        # Aggregate revenue across all customers
        for customer in self.customer_cohorts:
            # Count customers by plan
            customer_plan = customer.get('plan', PLANS[0]['name'])
            customers_by_plan[customer_plan] = customers_by_plan.get(customer_plan, 0) + 1
            
            # Add monthly revenue by stream
            for stream, amount in customer['monthly_revenue'].items():
                if stream in revenue_by_stream:
                    revenue_by_stream[stream] += amount
                
                # If this is a plan's monthly fee, add it to the plan's revenue
                if stream in plan_revenues:
                    plan_revenues[stream] += amount
            
            # Add one-time revenue for new customers
            if customer['month_joined'] == month:
                for stream, amount in customer['one_time_revenue'].items():
                    if stream in revenue_by_stream:
                        revenue_by_stream[stream] += amount
        
        # Count active packages across all customers
        package_counts = {}
        for name in UPSELL_PACKAGES:
            count = sum(c['upsells'].get_quantity(name) for c in self.customer_cohorts)
            package_counts[f"Upsell: {UPSELL_PACKAGES[name].name}"] = count
        
        # Store monthly data
        month_data = {
            "Month": month,
            "Total Customers": total_customers,
            "New Customers": len(new_customers),
            "One-Time Revenue (Cumulative)": round(self.cumulative_one_time, 2),
            "Base Hosting Revenue": round(base_hosting_revenue, 2),
            "Upsell Revenue": round(monthly_upsell_revenue, 2),
            "Total Monthly Revenue": round(total_monthly_revenue, 2),
            "Total Revenue (Cumulative)": round(self.cumulative_one_time + self.cumulative_hosting, 2),
        }
        
        # Add package counts
        month_data.update(package_counts)
        
        # Add revenue by stream (including plan-specific revenues)
        for stream, amount in revenue_by_stream.items():
            month_data[stream] = round(amount, 2)
            
        # Add plan-specific revenues (capitalized to match the expected column names)
        for plan_name, amount in plan_revenues.items():
            month_data[plan_name.capitalize()] = round(amount, 2)
                
        # Ensure all plan columns exist in the output, even if zero
        for plan in PLANS:
            if plan['name'] not in month_data:
                month_data[plan['name']] = 0.0
        
        self.data.append(month_data)
