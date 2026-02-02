"""
Ethiopia Financial Inclusion Dashboard

Interactive dashboard for visualizing financial inclusion trends,
forecasts, and scenario analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide"
)

def load_data():
    """Load the financial inclusion dataset"""
    data_path = Path(__file__).parent.parent / "data" / "raw" / "ethiopia_fi_unified_data.csv"
    return pd.read_csv(data_path)

def main():
    st.title("🇪🇹 Ethiopia Financial Inclusion Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("Dashboard Controls")
    
    # Load data
    try:
        df = load_data()
        st.sidebar.success(f"Data loaded: {len(df)} records")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Account Access Trends")
        # Add visualization code here
        
    with col2:
        st.subheader("Digital Payment Usage")
        # Add visualization code here
    
    # Data table
    st.subheader("Raw Data")
    st.dataframe(df)

if __name__ == "__main__":
    main()