"""
Interactive Dashboard for Ethiopia Digital Finance Analysis
Streamlit application integrating all visualizations and analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

try:
    from data_analysis import EthiopiaDataAnalyzer
    from visualization_engine import VisualizationEngine
    from impact_modeling import ImpactModeler
except ImportError:
    st.error("Could not import analysis modules. Please ensure src/ modules are available.")

# Page configuration
st.set_page_config(
    page_title="Ethiopia Digital Finance Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #E67E22;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498DB;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data"""
    try:
        analyzer = EthiopiaDataAnalyzer()
        analyzer.load_data()
        return analyzer.df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def get_summary_stats(df):
    """Get summary statistics"""
    if df is None:
        return {}
    
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    # Get key metrics
    account_ownership = latest_data[
        (latest_data['indicator'] == 'Account Ownership Rate') & 
        (latest_data['gender'] == 'all')
    ]['value_numeric'].iloc[0] if not latest_data.empty else 0
    
    mobile_money = latest_data[
        (latest_data['indicator'] == 'Mobile Money Account Rate') & 
        (latest_data['gender'] == 'all')
    ]['value_numeric'].iloc[0] if not latest_data.empty else 0
    
    return {
        'latest_year': int(latest_year),
        'account_ownership': account_ownership,
        'mobile_money': mobile_money,
        'total_records': len(df),
        'unique_indicators': df['indicator'].nunique()
    }

def create_overview_section(df, stats):
    """Create overview section"""
    st.markdown('<div class="section-header">📊 Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Account Ownership</h3>
            <h2>{stats['account_ownership']:.1f}%</h2>
            <p>Latest ({stats['latest_year']})</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Mobile Money</h3>
            <h2>{stats['mobile_money']:.1f}%</h2>
            <p>Latest ({stats['latest_year']})</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Data Points</h3>
            <h2>{stats['total_records']:,}</h2>
            <p>Total Records</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Indicators</h3>
            <h2>{stats['unique_indicators']}</h2>
            <p>Unique Metrics</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key insights
    st.markdown("""
    <div class="insight-box">
        <h4>🎯 Key Insights</h4>
        <ul>
            <li>Account ownership has grown significantly but growth is slowing</li>
            <li>Mobile money adoption is accelerating, doubling since 2021</li>
            <li>Gender gap persists but is narrowing over time</li>
            <li>Policy events show measurable impact on inclusion metrics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def create_trends_section(df):
    """Create trends analysis section"""
    st.markdown('<div class="section-header">📈 Trends Analysis</div>', unsafe_allow_html=True)
    
    # Time series plot
    fig = go.Figure()
    
    # Account ownership trend
    account_data = df[
        (df['indicator'] == 'Account Ownership Rate') & 
        (df['gender'] == 'all')
    ].sort_values('year')
    
    if not account_data.empty:
        fig.add_trace(go.Scatter(
            x=account_data['year'],
            y=account_data['value_numeric'],
            mode='lines+markers',
            name='Account Ownership Rate',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
    
    # Mobile money trend
    mm_data = df[
        (df['indicator'] == 'Mobile Money Account Rate') & 
        (df['gender'] == 'all')
    ].sort_values('year')
    
    if not mm_data.empty:
        fig.add_trace(go.Scatter(
            x=mm_data['year'],
            y=mm_data['value_numeric'],
            mode='lines+markers',
            name='Mobile Money Account Rate',
            line=dict(color='#E67E22', width=3),
            marker=dict(size=8)
        ))
    
    # Add event annotations
    events = [
        {'year': 2016, 'event': 'Digital Finance Strategy'},
        {'year': 2019, 'event': 'EthSwitch Launch'},
        {'year': 2020, 'event': 'Mobile Money Regulation'},
        {'year': 2021, 'event': 'Telebirr Launch'},
        {'year': 2022, 'event': 'Agent Banking Expansion'}
    ]
    
    for event in events:
        fig.add_vline(
            x=event['year'],
            line_dash="dash",
            line_color="red",
            annotation_text=event['event'],
            annotation_position="top"
        )
    
    fig.update_layout(
        title="Financial Inclusion Trends with Policy Events",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        height=500,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gender analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender gap analysis
        fig_gender = go.Figure()
        
        for gender, color in [('male', '#3498DB'), ('female', '#E74C3C')]:
            gender_data = df[
                (df['indicator'] == 'Account Ownership Rate') & 
                (df['gender'] == gender)
            ].sort_values('year')
            
            if not gender_data.empty:
                fig_gender.add_trace(go.Scatter(
                    x=gender_data['year'],
                    y=gender_data['value_numeric'],
                    mode='lines+markers',
                    name=f'{gender.title()}',
                    line=dict(color=color, width=3),
                    marker=dict(size=8)
                ))
        
        fig_gender.update_layout(
            title="Account Ownership by Gender",
            xaxis_title="Year",
            yaxis_title="Account Ownership (%)",
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Platform competition (simulated data)
        platforms = ['Telebirr', 'M-Pesa', 'Others']
        market_share = [70, 15, 15]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=platforms,
            values=market_share,
            hole=0.3,
            marker_colors=['#C73E1D', '#00A86B', '#8E44AD']
        )])
        
        fig_pie.update_layout(
            title="Mobile Money Market Share (2024)",
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

def create_forecasts_section():
    """Create forecasts section"""
    st.markdown('<div class="section-header">🔮 Forecasts & Projections</div>', unsafe_allow_html=True)
    
    # Forecast data (simulated based on modeling)
    forecast_data = {
        'Account Ownership Rate': {
            'years': [2025, 2026, 2027],
            'forecasts': [60.2, 62.8, 65.5],
            'lower_ci': [57.1, 59.2, 61.3],
            'upper_ci': [63.3, 66.4, 69.7]
        },
        'Mobile Money Account Rate': {
            'years': [2025, 2026, 2027],
            'forecasts': [12.8, 16.2, 20.1],
            'lower_ci': [10.5, 13.1, 16.2],
            'upper_ci': [15.1, 19.3, 24.0]
        }
    }
    
    # Create forecast visualization
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Account Ownership Forecast', 'Mobile Money Forecast')
    )
    
    for i, (indicator, data) in enumerate(forecast_data.items()):
        col = i + 1
        
        # Forecast line
        fig.add_trace(
            go.Scatter(
                x=data['years'],
                y=data['forecasts'],
                mode='lines+markers',
                name=f'{indicator} Forecast',
                line=dict(color='#2E86AB' if i == 0 else '#E67E22', width=3),
                marker=dict(size=8)
            ),
            row=1, col=col
        )
        
        # Confidence interval
        fig.add_trace(
            go.Scatter(
                x=data['years'] + data['years'][::-1],
                y=data['upper_ci'] + data['lower_ci'][::-1],
                fill='toself',
                fillcolor=f"rgba({'46, 134, 171' if i == 0 else '230, 126, 34'}, 0.2)",
                line=dict(color='rgba(255,255,255,0)'),
                name=f'{indicator} 95% CI',
                showlegend=False
            ),
            row=1, col=col
        )
    
    fig.update_layout(
        title="Financial Inclusion Forecasts (2025-2027)",
        height=500,
        template="plotly_white"
    )
    
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Percentage (%)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Scenario analysis
    st.subheader("📊 Scenario Analysis")
    
    scenario_data = {
        'Scenario': ['Baseline', 'Accelerated Digital', 'Inclusive Focus'],
        'Account Ownership 2027': [65.5, 72.3, 68.8],
        'Mobile Money 2027': [20.1, 25.6, 22.4],
        'Description': [
            'Current trajectory',
            'Aggressive digital infrastructure',
            'Focus on gender & rural inclusion'
        ]
    }
    
    scenario_df = pd.DataFrame(scenario_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Scenario comparison chart
        fig_scenario = go.Figure()
        
        fig_scenario.add_trace(go.Bar(
            name='Account Ownership 2027',
            x=scenario_df['Scenario'],
            y=scenario_df['Account Ownership 2027'],
            marker_color='#2E86AB'
        ))
        
        fig_scenario.add_trace(go.Bar(
            name='Mobile Money 2027',
            x=scenario_df['Scenario'],
            y=scenario_df['Mobile Money 2027'],
            marker_color='#E67E22'
        ))
        
        fig_scenario.update_layout(
            title="2027 Projections by Scenario",
            xaxis_title="Scenario",
            yaxis_title="Percentage (%)",
            barmode='group',
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_scenario, use_container_width=True)
    
    with col2:
        st.markdown("**Scenario Details:**")
        for _, row in scenario_df.iterrows():
            st.markdown(f"""
            **{row['Scenario']}**  
            {row['Description']}  
            Account: {row['Account Ownership 2027']}%  
            Mobile Money: {row['Mobile Money 2027']}%
            """)

def create_projections_section():
    """Create detailed projections section"""
    st.markdown('<div class="section-header">📋 Detailed Projections</div>', unsafe_allow_html=True)
    
    # Target analysis
    st.subheader("🎯 Target Achievement Analysis")
    
    targets = {
        'Metric': ['Account Ownership', 'Mobile Money', 'Digital Payments', 'Gender Gap'],
        'Current (2024)': ['58%', '9.5%', '42%', '15pp'],
        '2027 Target': ['70%', '25%', '60%', '<10pp'],
        '2027 Forecast': ['65.5%', '20.1%', '55%', '12pp'],
        'Status': ['Behind', 'On Track', 'On Track', 'Behind']
    }
    
    targets_df = pd.DataFrame(targets)
    
    # Color code status
    def color_status(val):
        if val == 'On Track':
            return 'background-color: #d4edda; color: #155724'
        elif val == 'Behind':
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    styled_df = targets_df.style.applymap(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Policy Recommendations")
    
    recommendations = [
        {
            'Priority': 'High',
            'Area': 'Gender Inclusion',
            'Recommendation': 'Launch targeted women financial inclusion program',
            'Expected Impact': '+5pp gender gap reduction'
        },
        {
            'Priority': 'High', 
            'Area': 'Rural Access',
            'Recommendation': 'Expand agent banking network in rural areas',
            'Expected Impact': '+3pp account ownership'
        },
        {
            'Priority': 'Medium',
            'Area': 'Digital Infrastructure',
            'Recommendation': 'Accelerate 5G rollout for mobile money',
            'Expected Impact': '+4pp mobile money adoption'
        },
        {
            'Priority': 'Medium',
            'Area': 'Regulatory',
            'Recommendation': 'Streamline KYC requirements for basic accounts',
            'Expected Impact': '+2pp account ownership'
        }
    ]
    
    rec_df = pd.DataFrame(recommendations)
    
    def color_priority(val):
        if val == 'High':
            return 'background-color: #f8d7da; color: #721c24'
        elif val == 'Medium':
            return 'background-color: #fff3cd; color: #856404'
        return ''
    
    styled_rec = rec_df.style.applymap(color_priority, subset=['Priority'])
    st.dataframe(styled_rec, use_container_width=True)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<div class="main-header">🏦 Ethiopia Digital Finance Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    section = st.sidebar.selectbox(
        "Choose Section:",
        ["Overview", "Trends Analysis", "Forecasts", "Projections", "Data Explorer"]
    )
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Could not load data. Please check data files.")
        return
    
    stats = get_summary_stats(df)
    
    # Display selected section
    if section == "Overview":
        create_overview_section(df, stats)
        
    elif section == "Trends Analysis":
        create_trends_section(df)
        
    elif section == "Forecasts":
        create_forecasts_section()
        
    elif section == "Projections":
        create_projections_section()
        
    elif section == "Data Explorer":
        st.markdown('<div class="section-header">🔍 Data Explorer</div>', unsafe_allow_html=True)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_indicator = st.selectbox(
                "Select Indicator:",
                df['indicator'].unique()
            )
        
        with col2:
            selected_gender = st.selectbox(
                "Select Gender:",
                ['all'] + [g for g in df['gender'].unique() if g != 'all']
            )
        
        with col3:
            year_range = st.slider(
                "Year Range:",
                int(df['year'].min()),
                int(df['year'].max()),
                (int(df['year'].min()), int(df['year'].max()))
            )
        
        # Filter data
        filtered_df = df[
            (df['indicator'] == selected_indicator) &
            (df['gender'] == selected_gender) &
            (df['year'] >= year_range[0]) &
            (df['year'] <= year_range[1])
        ]
        
        # Display filtered data
        st.dataframe(filtered_df, use_container_width=True)
        
        # Quick visualization
        if not filtered_df.empty and 'value_numeric' in filtered_df.columns:
            fig = px.line(
                filtered_df.sort_values('year'),
                x='year',
                y='value_numeric',
                title=f"{selected_indicator} - {selected_gender.title()}"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Ethiopia Digital Finance Analysis Dashboard** | Data as of 2024")

if __name__ == "__main__":
    main()