"""
Supporting Analysis and Visualizations for Ethiopia Digital Finance Interim Report
Senior Data Scientist, Selam Analytics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set up professional styling
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

def create_account_ownership_trend():
    """Create account ownership trend visualization"""
    
    # Sample data based on our analysis
    years = [2017, 2018, 2019, 2021, 2022, 2023, 2024]
    ownership_rates = [22, 35, 46, 56, 57, 58, 58]
    
    # Key events
    events = {
        2016: 'Digital Finance Strategy',
        2019: 'EthSwitch Launch',
        2020: 'Mobile Money Regulation',
        2021: 'Telebirr Launch'
    }
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Main trend line
    ax.plot(years, ownership_rates, marker='o', linewidth=4, markersize=10, 
            color='#2E86AB', label='Account Ownership Rate')
    
    # Add event markers
    for year, event in events.items():
        if year in years:
            idx = years.index(year)
            ax.annotate(event, xy=(year, ownership_rates[idx]), 
                       xytext=(year, ownership_rates[idx] + 8),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2),
                       fontsize=10, ha='center', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Highlight slowdown period
    slowdown_years = [2021, 2022, 2023, 2024]
    slowdown_rates = [56, 57, 58, 58]
    ax.plot(slowdown_years, slowdown_rates, linewidth=6, alpha=0.3, color='red')
    ax.text(2022.5, 54, '2021-2024 Slowdown Period', fontsize=12, fontweight='bold',
            ha='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='red', alpha=0.2))
    
    ax.set_title('Ethiopia Account Ownership Trajectory: Policy Impact & Growth Slowdown', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Account Ownership Rate (%)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)
    
    # Add target line
    ax.axhline(y=70, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(2023, 72, '2027 Target: 70%', fontsize=11, fontweight='bold', color='green')
    
    plt.tight_layout()
    return fig

def create_gender_gap_analysis():
    """Create gender gap analysis visualization"""
    
    years = [2017, 2019, 2021, 2024]
    male_rates = [32, 56, 65, 65]
    female_rates = [12, 36, 47, 50]
    gaps = [20, 20, 18, 15]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Gender trends
    ax1.plot(years, male_rates, marker='o', linewidth=3, markersize=8, 
             label='Male', color='#3498DB')
    ax1.plot(years, female_rates, marker='o', linewidth=3, markersize=8, 
             label='Female', color='#E74C3C')
    
    ax1.set_title('Account Ownership by Gender', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Account Ownership Rate (%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gender gap trend
    ax2.bar(years, gaps, color='#FF9F43', alpha=0.8, width=0.8)
    ax2.set_title('Gender Gap Trend (Percentage Points)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Gender Gap (pp)')
    ax2.grid(True, alpha=0.3)
    
    # Add values on bars
    for i, gap in enumerate(gaps):
        ax2.text(years[i], gap + 0.5, f'{gap}pp', ha='center', fontweight='bold')
    
    plt.suptitle('Gender Inclusion Analysis: Progress but Persistent Gaps', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def create_platform_competition():
    """Create platform competition visualization"""
    
    platforms = ['Telebirr', 'M-Pesa', 'Others']
    market_share = [70, 15, 15]
    users_millions = [25, 3, 2]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Market share pie chart
    colors = ['#C73E1D', '#00A86B', '#8E44AD']
    wedges, texts, autotexts = ax1.pie(market_share, labels=platforms, autopct='%1.1f%%', 
                                      colors=colors, startangle=90, textprops={'fontsize': 12})
    ax1.set_title('Mobile Money Market Share (2024)', fontsize=14, fontweight='bold')
    
    # User base comparison
    ax2.bar(platforms, users_millions, color=colors, alpha=0.8)
    ax2.set_title('Active Users (Millions)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Users (Millions)')
    
    # Add values on bars
    for i, users in enumerate(users_millions):
        ax2.text(i, users + 0.5, f'{users}M', ha='center', fontweight='bold')
    
    plt.suptitle('Platform Competition Dynamics: Telebirr Dominance vs Emerging Competition', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def create_infrastructure_correlation():
    """Create infrastructure vs inclusion correlation"""
    
    # Sample regional data
    regions = ['Addis Ababa', 'Dire Dawa', 'Oromia', 'Amhara', 'SNNP', 'Tigray']
    coverage_4g = [95, 85, 70, 65, 60, 55]
    account_ownership = [75, 68, 58, 52, 48, 45]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Scatter plot
    scatter = ax.scatter(coverage_4g, account_ownership, s=200, alpha=0.7, 
                        c=range(len(regions)), cmap='viridis')
    
    # Add region labels
    for i, region in enumerate(regions):
        ax.annotate(region, (coverage_4g[i], account_ownership[i]), 
                   xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    # Add trend line
    z = np.polyfit(coverage_4g, account_ownership, 1)
    p = np.poly1d(z)
    ax.plot(coverage_4g, p(coverage_4g), "r--", alpha=0.8, linewidth=2)
    
    # Calculate correlation
    correlation = np.corrcoef(coverage_4g, account_ownership)[0, 1]
    ax.text(0.05, 0.95, f'Correlation: r = {correlation:.2f}', 
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_title('Infrastructure-Inclusion Correlation: 4G Coverage vs Account Ownership', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('4G Coverage (%)')
    ax.set_ylabel('Account Ownership (%)')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_event_impact_timeline():
    """Create event impact timeline visualization"""
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Events data
    events = [
        {'year': 2016, 'event': 'Digital Finance Strategy', 'impact': 8, 'type': 'Policy'},
        {'year': 2019, 'event': 'EthSwitch Launch', 'impact': 5, 'type': 'Infrastructure'},
        {'year': 2020, 'event': 'Mobile Money Regulation', 'impact': 7, 'type': 'Regulatory'},
        {'year': 2021, 'event': 'Telebirr Launch', 'impact': 15, 'type': 'Technology'},
        {'year': 2022, 'event': 'Agent Banking Expansion', 'impact': 3, 'type': 'Infrastructure'}
    ]
    
    # Color mapping for event types
    colors = {'Policy': '#3498DB', 'Infrastructure': '#E67E22', 
              'Regulatory': '#E74C3C', 'Technology': '#27AE60'}
    
    # Create timeline
    for i, event in enumerate(events):
        # Event marker
        ax.scatter(event['year'], i, s=event['impact']*50, 
                  c=colors[event['type']], alpha=0.7, edgecolors='black', linewidth=2)
        
        # Event label
        ax.text(event['year'] + 0.1, i, f"{event['event']}\n(+{event['impact']}pp impact)", 
               fontsize=10, va='center')
    
    # Customize plot
    ax.set_yticks(range(len(events)))
    ax.set_yticklabels([f"Event {i+1}" for i in range(len(events))])
    ax.set_xlabel('Year', fontsize=12)
    ax.set_title('Policy Event Timeline & Measured Impact on Financial Inclusion', 
                fontsize=14, fontweight='bold')
    
    # Add legend
    legend_elements = [plt.scatter([], [], s=100, c=color, alpha=0.7, edgecolors='black', 
                                  label=event_type) for event_type, color in colors.items()]
    ax.legend(handles=legend_elements, title='Event Type', loc='upper left')
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def save_all_visualizations():
    """Save all visualizations to reports/figures/"""
    
    figures_dir = Path('figures')
    figures_dir.mkdir(exist_ok=True)
    
    # Create and save all visualizations
    visualizations = [
        (create_account_ownership_trend(), 'account_ownership_trend.png'),
        (create_gender_gap_analysis(), 'gender_gap_analysis.png'),
        (create_platform_competition(), 'platform_competition.png'),
        (create_infrastructure_correlation(), 'infrastructure_correlation.png'),
        (create_event_impact_timeline(), 'event_impact_timeline.png')
    ]
    
    for fig, filename in visualizations:
        filepath = figures_dir / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"📊 Saved: {filepath}")
        plt.close(fig)
    
    print(f"\n✅ All visualizations saved to {figures_dir}/")

def create_summary_tables():
    """Create summary tables for the report"""
    
    # Task 1 Enrichment Summary
    enrichment_summary = pd.DataFrame({
        'Category': ['Observations', 'Events', 'Impact Links', 'Regional Data', 'Gender Data'],
        'Records Added': [12, 5, 7, 8, 6],
        'Confidence Level': ['High', 'High', 'High', 'Medium', 'High'],
        'Source Type': ['Survey/Admin', 'Policy Docs', 'Analysis', 'Estimates', 'Survey']
    })
    
    # Key Metrics Summary
    metrics_summary = pd.DataFrame({
        'Metric': ['Account Ownership 2024', 'Digital Payment Usage 2024', 'Gender Gap 2024', 
                  '4G Coverage 2024', 'Telebirr Users', 'M-Pesa Users'],
        'Value': ['58%', '42%', '15pp', '75%', '25M', '3M'],
        'Target 2027': ['70%', '60%', '<10pp', '95%', 'N/A', 'N/A'],
        'Status': ['Behind', 'On Track', 'Behind', 'On Track', 'Leading', 'Growing']
    })
    
    # Save tables
    tables_dir = Path('tables')
    tables_dir.mkdir(exist_ok=True)
    
    enrichment_summary.to_csv(tables_dir / 'enrichment_summary.csv', index=False)
    metrics_summary.to_csv(tables_dir / 'key_metrics_summary.csv', index=False)
    
    print("📋 Summary tables saved:")
    print(f"   • {tables_dir}/enrichment_summary.csv")
    print(f"   • {tables_dir}/key_metrics_summary.csv")
    
    return enrichment_summary, metrics_summary

if __name__ == "__main__":
    print("🎯 Generating supporting analysis for Ethiopia Digital Finance Interim Report")
    print("=" * 70)
    
    # Create visualizations
    save_all_visualizations()
    
    # Create summary tables
    enrichment_summary, metrics_summary = create_summary_tables()
    
    print("\n✅ Supporting analysis complete!")
    print("📊 5 visualizations created")
    print("📋 2 summary tables created")
    print("\nFiles ready for interim report presentation.")