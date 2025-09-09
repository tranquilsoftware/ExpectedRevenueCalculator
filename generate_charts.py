import matplotlib.pyplot as plt
import os
from typing import Dict, List
import pandas as pd
from hidden_costs import REVENUE_STREAMS

class ChartGenerator:
    @staticmethod
    def generate_revenue_charts(data_frames: Dict[str, pd.DataFrame]) -> None:
        """Generate and save revenue charts for each scenario"""
        os.makedirs('output', exist_ok=True)
        
        # Individual scenario charts
        for label, df in data_frames.items():
            filename = f'output/revenue_breakdown_{label.lower().replace(" ", "_")}.png'
            ChartGenerator._plot_revenue_breakdown(
                df, 
                f'Monthly Revenue Breakdown - {label}',
                filename
            )
        
        # Combined monthly revenue comparison chart
        plt.figure(figsize=(14, 7))
        for label, df in data_frames.items():
            plt.plot(df['Month'], df['Total Monthly Revenue'], 
                    label=f'{label} Revenue', linewidth=2)
        
        plt.xlabel('Month')
        plt.ylabel('Total Monthly Revenue ($)')
        plt.title('Monthly Revenue Comparison by Scenario')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('output/revenue_comparison.png', bbox_inches='tight', dpi=300)
        plt.close()
        print("Saved comparison chart: output/revenue_comparison.png")
        
        # Generate cumulative revenue projection chart
        ChartGenerator._generate_cumulative_revenue_graph(data_frames)
    
    @staticmethod
    def _generate_cumulative_revenue_graph(data_frames: Dict[str, pd.DataFrame]) -> None:
        """Generate a detailed cumulative revenue projection graph"""
        plt.figure(figsize=(14, 8))
        
        # Plot each scenario with final total in the legend
        for label, df in data_frames.items():
            plt.plot(df['Month'], 
                    df['Total Revenue (Cumulative)'], 
                    label=f'{label} (${df["Total Revenue (Cumulative)"].iloc[-1]:,.0f} total)',
                    linewidth=2.5)
        
        # Format the plot
        plt.title('Cumulative Revenue Projection by Customer Acquisition Rate', 
                fontsize=16, pad=20)
        plt.xlabel('Month', fontsize=12, labelpad=10)
        plt.ylabel('Cumulative Revenue ($)', fontsize=12, labelpad=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10, framealpha=1, shadow=True)
        
        # Format y-axis to show dollar values with comma separators
        ax = plt.gca()
        ax.yaxis.set_major_formatter('${x:,.0f}')
        
        # Add some padding around the plot
        plt.tight_layout()
        
        # Save the figure
        output_path = os.path.join('output', 'cumulative_revenue_projection.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved cumulative revenue projection: {output_path}")

    @staticmethod
    def _plot_revenue_breakdown(df: pd.DataFrame, title: str, filename: str) -> None:
        """Helper method to plot revenue breakdown for a single scenario"""
        plt.figure(figsize=(14, 7))
        
        # Calculate one-time revenue per month (difference between cumulative values)
        df['Monthly One-Time Revenue'] = df['One-Time Revenue (Cumulative)'].diff().fillna(df['One-Time Revenue (Cumulative)'].iloc[0])
        
        # Get revenue columns and their colors from REVENUE_STREAMS
        revenue_columns = list(REVENUE_STREAMS.keys())
        colors = [REVENUE_STREAMS[col]['color'] for col in revenue_columns]
        
        # Plot each revenue stream
        ax = plt.gca()
        ax.stackplot(
            df['Month'],
            [df[col] for col in revenue_columns],
            labels=[REVENUE_STREAMS[col]['display_name'] for col in revenue_columns],
            colors=colors,
            alpha=0.7
        )
        
        # Add customer count on secondary y-axis
        ax2 = ax.twinx()
        ax2.plot(df['Month'], df['Total Customers'], 'k--', label='Total Customers', alpha=0.7)
        
        # Formatting
        plt.title(title, fontsize=14, pad=20)
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Monthly Revenue ($)', fontsize=12)
        ax2.set_ylabel('Total Customers', fontsize=12)
        
        # Add legend
        ax.legend(loc='upper left', bbox_to_anchor=(0.01, 1.15), ncol=4)
        ax2.legend(loc='upper right', bbox_to_anchor=(0.99, 1.15))
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        print(f"Saved chart as: {filename}")
        plt.close()
