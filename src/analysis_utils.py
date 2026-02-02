"""
Analysis utilities for Ethiopia Financial Inclusion EDA
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class AnalysisUtils:
    """Utility class for data analysis functions"""
    
    @staticmethod
    def extract_year_from_data(df: pd.DataFrame) -> Optional[str]:
        """Extract year information from various date columns"""
        year_col = None
        
        # Check for direct year column
        if 'year' in df.columns:
            return 'year'
        
        # Extract from date columns
        date_columns = ['observation_date', 'period_start', 'period_end', 'collected_by']
        for col in date_columns:
            if col in df.columns and df[col].dtype == 'datetime64[ns]':
                df[f'{col}_year'] = df[col].dt.year
                if year_col is None:
                    year_col = f'{col}_year'
        
        # Extract from fiscal_year if it's a string
        if 'fiscal_year' in df.columns and year_col is None:
            try:
                df['fiscal_year_extracted'] = pd.to_numeric(df['fiscal_year'], errors='coerce')
                year_col = 'fiscal_year_extracted'
            except:
                pass
        
        return year_col
    
    @staticmethod
    def get_value_column(df: pd.DataFrame) -> Optional[str]:
        """Identify the main value column"""
        possible_value_cols = ['value_numeric', 'value', 'amount', 'rate', 'percentage']
        
        for col in possible_value_cols:
            if col in df.columns:
                return col
        
        return None
    
    @staticmethod
    def calculate_growth_rate(df: pd.DataFrame, value_col: str, year_col: str, 
                            group_cols: Optional[List[str]] = None) -> pd.DataFrame:
        """Calculate growth rates over time"""
        
        if group_cols:
            grouped = df.groupby(group_cols + [year_col])[value_col].mean().reset_index()
            grouped = grouped.sort_values(group_cols + [year_col])
            
            growth_rates = []
            for group_vals in grouped[group_cols].drop_duplicates().values:
                group_filter = True
                for i, col in enumerate(group_cols):
                    group_filter &= (grouped[col] == group_vals[i])
                
                group_data = grouped[group_filter].copy()
                group_data['growth_rate'] = group_data[value_col].pct_change() * 100
                growth_rates.append(group_data)
            
            return pd.concat(growth_rates, ignore_index=True)
        else:
            trend_data = df.groupby(year_col)[value_col].mean().reset_index()
            trend_data = trend_data.sort_values(year_col)
            trend_data['growth_rate'] = trend_data[value_col].pct_change() * 100
            return trend_data
    
    @staticmethod
    def identify_outliers(df: pd.DataFrame, col: str, method: str = 'iqr') -> pd.Series:
        """Identify outliers using IQR or Z-score method"""
        
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (df[col] < lower_bound) | (df[col] > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            return z_scores > 3
        
        return pd.Series([False] * len(df))
    
    @staticmethod
    def calculate_summary_stats(df: pd.DataFrame, value_col: str, 
                              group_col: Optional[str] = None) -> Dict[str, Any]:
        """Calculate comprehensive summary statistics"""
        
        if group_col and group_col in df.columns:
            stats = {}
            for group in df[group_col].unique():
                if pd.notna(group):
                    group_data = df[df[group_col] == group][value_col].dropna()
                    stats[str(group)] = {
                        'count': len(group_data),
                        'mean': group_data.mean(),
                        'median': group_data.median(),
                        'std': group_data.std(),
                        'min': group_data.min(),
                        'max': group_data.max(),
                        'q25': group_data.quantile(0.25),
                        'q75': group_data.quantile(0.75)
                    }
            return stats
        else:
            data = df[value_col].dropna()
            return {
                'overall': {
                    'count': len(data),
                    'mean': data.mean(),
                    'median': data.median(),
                    'std': data.std(),
                    'min': data.min(),
                    'max': data.max(),
                    'q25': data.quantile(0.25),
                    'q75': data.quantile(0.75)
                }
            }
    
    @staticmethod
    def analyze_trends(df: pd.DataFrame, value_col: str, year_col: str,
                      indicator_col: str = 'indicator_code') -> Dict[str, Any]:
        """Analyze trends for different indicators"""
        
        trends = {}
        
        for indicator in df[indicator_col].unique():
            if pd.notna(indicator):
                indicator_data = df[df[indicator_col] == indicator]
                trend_data = indicator_data.groupby(year_col)[value_col].mean().reset_index()
                trend_data = trend_data.sort_values(year_col)
                
                if len(trend_data) >= 2:
                    # Calculate trend metrics
                    first_value = trend_data[value_col].iloc[0]
                    last_value = trend_data[value_col].iloc[-1]
                    total_change = last_value - first_value
                    percent_change = (total_change / first_value) * 100 if first_value != 0 else 0
                    
                    # Calculate average annual growth rate
                    years_span = trend_data[year_col].iloc[-1] - trend_data[year_col].iloc[0]
                    cagr = ((last_value / first_value) ** (1/years_span) - 1) * 100 if first_value > 0 and years_span > 0 else 0
                    
                    trends[indicator] = {
                        'first_year': trend_data[year_col].iloc[0],
                        'last_year': trend_data[year_col].iloc[-1],
                        'first_value': first_value,
                        'last_value': last_value,
                        'total_change': total_change,
                        'percent_change': percent_change,
                        'cagr': cagr,
                        'data_points': len(trend_data)
                    }
        
        return trends
    
    @staticmethod
    def calculate_gender_gap(df: pd.DataFrame, value_col: str, 
                           gender_col: str = 'gender') -> Dict[str, float]:
        """Calculate gender gaps in financial inclusion metrics"""
        
        if gender_col not in df.columns:
            return {}
        
        # Get male and female data
        male_data = df[df[gender_col].str.lower() == 'male'][value_col].dropna()
        female_data = df[df[gender_col].str.lower() == 'female'][value_col].dropna()
        
        if male_data.empty or female_data.empty:
            return {}
        
        male_avg = male_data.mean()
        female_avg = female_data.mean()
        
        gap_absolute = male_avg - female_avg
        gap_relative = (gap_absolute / female_avg) * 100 if female_avg != 0 else 0
        
        return {
            'male_average': male_avg,
            'female_average': female_avg,
            'gap_absolute': gap_absolute,
            'gap_relative': gap_relative,
            'higher_gender': 'Male' if male_avg > female_avg else 'Female'
        }
    
    @staticmethod
    def identify_data_gaps(df: pd.DataFrame, year_col: str, 
                          indicator_col: str = 'indicator_code') -> Dict[str, List[int]]:
        """Identify missing years in time series data"""
        
        gaps = {}
        
        for indicator in df[indicator_col].unique():
            if pd.notna(indicator):
                indicator_data = df[df[indicator_col] == indicator]
                years_present = sorted(indicator_data[year_col].dropna().unique())
                
                if len(years_present) >= 2:
                    year_range = range(int(years_present[0]), int(years_present[-1]) + 1)
                    missing_years = [year for year in year_range if year not in years_present]
                    
                    if missing_years:
                        gaps[indicator] = missing_years
        
        return gaps
    
    @staticmethod
    def generate_insights_summary(analysis_results: Dict[str, Any]) -> List[str]:
        """Generate key insights from analysis results"""
        
        insights = []
        
        # Account ownership insights
        if 'ownership_insights' in analysis_results:
            ownership = analysis_results['ownership_insights']
            if ownership and 'latest_rate' in ownership:
                insights.append(f"Current account ownership rate: {ownership['latest_rate']:.1f}%")
                if 'growth' in ownership and ownership['growth']:
                    insights.append(f"Account ownership growth: {ownership['growth']:+.1f} percentage points")
        
        # Gender gap insights
        if 'gender_insights' in analysis_results:
            gender = analysis_results['gender_insights']
            if gender and 'gap' in gender:
                insights.append(f"Gender gap in financial access: {gender['gap']:.1f}pp ({gender['higher_gender']} higher)")
        
        # Digital payment insights
        if 'payment_insights' in analysis_results:
            payment = analysis_results['payment_insights']
            if payment and 'average_usage' in payment:
                insights.append(f"Average digital payment usage: {payment['average_usage']:.2f}")
        
        # Infrastructure insights
        if 'infrastructure_insights' in analysis_results:
            infra = analysis_results['infrastructure_insights']
            if infra and 'mobile_penetration' in infra:
                insights.append(f"Mobile penetration supports digital finance growth")
        
        # Data quality insights
        if 'quality_report' in analysis_results:
            quality = analysis_results['quality_report']
            if quality and 'completeness' in quality:
                missing_cols = len([k for k, v in quality['completeness']['missing_by_column']['counts'].items() if v > 0])
                insights.append(f"Data quality: {missing_cols} columns have missing values")
        
        return insights