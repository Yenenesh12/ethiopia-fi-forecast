"""
Insights generator for Ethiopia Financial Inclusion EDA
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class InsightsGenerator:
    """Generate key insights from financial inclusion data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.insights = {}
        
    def extract_year_from_data(self) -> Optional[str]:
        """Extract year information from various date columns"""
        year_col = None
        
        # Check for direct year column
        if 'year' in self.df.columns:
            return 'year'
        
        # Extract from date columns
        date_columns = ['observation_date', 'period_start', 'period_end', 'collected_by']
        for col in date_columns:
            if col in self.df.columns and self.df[col].dtype == 'datetime64[ns]':
                self.df[f'{col}_year'] = self.df[col].dt.year
                if year_col is None:
                    year_col = f'{col}_year'
        
        # Extract from fiscal_year if it's a string
        if 'fiscal_year' in self.df.columns and year_col is None:
            try:
                self.df['fiscal_year_extracted'] = pd.to_numeric(self.df['fiscal_year'], errors='coerce')
                year_col = 'fiscal_year_extracted'
            except:
                pass
        
        return year_col
    
    def get_value_column(self) -> str:
        """Get the appropriate value column"""
        return 'value_numeric' if 'value_numeric' in self.df.columns else 'value'
    
    def insight_1_account_ownership_trends(self) -> Dict:
        """Generate insights on account ownership trends"""
        
        year_col = self.extract_year_from_data()
        value_col = self.get_value_column()
        
        if year_col is None or value_col not in self.df.columns:
            return {"error": "Missing required columns for trend analysis"}
        
        # Filter for account ownership indicators
        access_indicators = ['ACC_OWNERSHIP', 'FI_ACCESS_ACCOUNT', 'ACC_FAYDA']
        access_data = self.df[
            (self.df['indicator_code'].isin(access_indicators)) & 
            (self.df['record_type'] == 'observation')
        ].copy() if 'record_type' in self.df.columns else self.df[self.df['indicator_code'].isin(access_indicators)].copy()
        
        if access_data.empty:
            return {"error": "No account ownership data found"}
        
        # Calculate key metrics
        latest_year = access_data[year_col].max()
        earliest_year = access_data[year_col].min()
        latest_rate = access_data[access_data[year_col] == latest_year][value_col].mean()
        earliest_rate = access_data[access_data[year_col] == earliest_year][value_col].mean()
        
        growth = latest_rate - earliest_rate if not pd.isna(earliest_rate) else None
        
        # Trend analysis
        yearly_trend = access_data.groupby(year_col)[value_col].mean()
        trend_direction = "increasing" if yearly_trend.iloc[-1] > yearly_trend.iloc[0] else "decreasing"
        
        insight = {
            "title": "Account Ownership Trends",
            "latest_year": int(latest_year),
            "latest_rate": round(latest_rate, 1),
            "earliest_year": int(earliest_year),
            "earliest_rate": round(earliest_rate, 1) if not pd.isna(earliest_rate) else None,
            "growth": round(growth, 1) if growth is not None else None,
            "trend_direction": trend_direction,
            "data_points": len(access_data),
            "summary": f"Account ownership reached {latest_rate:.1f}% in {latest_year}, showing {trend_direction} trend"
        }
        
        self.insights["account_ownership"] = insight
        return insight
    
    def insight_2_digital_payment_patterns(self) -> Dict:
        """Generate insights on digital payment usage patterns"""
        
        value_col = self.get_value_column()
        
        # Filter for usage indicators
        usage_indicators = ['USG_P2P_COUNT', 'USG_P2P_VALUE', 'USG_TELEBIRR_USERS', 
                           'USG_TELEBIRR_VALUE', 'USG_MPESA_ACTIVE', 'USG_ACTIVE_RATE']
        
        usage_data = self.df[self.df['indicator_code'].isin(usage_indicators)].copy()
        
        if usage_data.empty:
            return {"error": "No digital payment usage data found"}
        
        # Platform analysis
        telebirr_data = usage_data[usage_data['indicator_code'].str.contains('TELEBIRR', na=False)]
        mpesa_data = usage_data[usage_data['indicator_code'].str.contains('MPESA', na=False)]
        
        telebirr_avg = telebirr_data[value_col].mean() if not telebirr_data.empty else 0
        mpesa_avg = mpesa_data[value_col].mean() if not mpesa_data.empty else 0
        
        dominant_platform = "Telebirr" if telebirr_avg > mpesa_avg else "M-Pesa"
        
        # Usage statistics
        total_indicators = len(usage_data['indicator_code'].unique())
        avg_usage = usage_data[value_col].mean()
        most_active_indicator = usage_data.groupby('indicator_code')[value_col].mean().idxmax()
        
        insight = {
            "title": "Digital Payment Usage Patterns",
            "total_indicators": total_indicators,
            "average_usage": round(avg_usage, 2),
            "most_active_indicator": most_active_indicator,
            "dominant_platform": dominant_platform,
            "telebirr_avg": round(telebirr_avg, 2),
            "mpesa_avg": round(mpesa_avg, 2),
            "summary": f"Digital payments show {total_indicators} tracked indicators with {dominant_platform} leading"
        }
        
        self.insights["digital_payments"] = insight
        return insight
    
    def insight_3_gender_gap_analysis(self) -> Dict:
        """Generate insights on gender gaps"""
        
        if 'gender' not in self.df.columns:
            return {"error": "No gender data available"}
        
        value_col = self.get_value_column()
        
        # Filter for gender-specific data
        gender_data = self.df[self.df['gender'].isin(['male', 'female', 'Male', 'Female'])].copy()
        
        if gender_data.empty:
            return {"error": "No gender-disaggregated data found"}
        
        # Focus on access indicators
        access_indicators = ['ACC_OWNERSHIP', 'GEN_GAP_ACC', 'ACC_FAYDA']
        gender_access = gender_data[gender_data['indicator_code'].isin(access_indicators)]
        
        if gender_access.empty:
            return {"error": "No gender access data found"}
        
        # Calculate gender averages
        male_avg = gender_access[gender_access['gender'].str.lower() == 'male'][value_col].mean()
        female_avg = gender_access[gender_access['gender'].str.lower() == 'female'][value_col].mean()
        
        if pd.isna(male_avg) or pd.isna(female_avg):
            return {"error": "Insufficient gender data for analysis"}
        
        gap = abs(male_avg - female_avg)
        higher_gender = 'Male' if male_avg > female_avg else 'Female'
        gap_percentage = (gap / max(male_avg, female_avg)) * 100
        
        insight = {
            "title": "Gender Gap Analysis",
            "male_avg": round(male_avg, 1),
            "female_avg": round(female_avg, 1),
            "gap": round(gap, 1),
            "gap_percentage": round(gap_percentage, 1),
            "higher_gender": higher_gender,
            "summary": f"Gender gap of {gap:.1f}pp with {higher_gender} having higher access rates"
        }
        
        self.insights["gender_gap"] = insight
        return insight
    
    def insight_4_infrastructure_impact(self) -> Dict:
        """Generate insights on infrastructure indicators"""
        
        value_col = self.get_value_column()
        
        # Infrastructure indicators
        infra_indicators = ['ACC_4G_COV', 'ACC_MOBILE_PEN', 'USG_ATM_COUNT', 'USG_ATM_VALUE']
        infra_data = self.df[self.df['indicator_code'].isin(infra_indicators)].copy()
        
        if infra_data.empty:
            return {"error": "No infrastructure data found"}
        
        # Infrastructure statistics
        coverage_indicators = infra_data[infra_data['indicator_code'].str.contains('COV|PEN', na=False)]
        usage_indicators = infra_data[infra_data['indicator_code'].str.contains('ATM|COUNT', na=False)]
        
        avg_coverage = coverage_indicators[value_col].mean() if not coverage_indicators.empty else 0
        avg_usage = usage_indicators[value_col].mean() if not usage_indicators.empty else 0
        
        total_infra_indicators = len(infra_data['indicator_code'].unique())
        
        insight = {
            "title": "Infrastructure Impact Analysis",
            "total_indicators": total_infra_indicators,
            "avg_coverage": round(avg_coverage, 1),
            "avg_usage": round(avg_usage, 1),
            "coverage_indicators": len(coverage_indicators),
            "usage_indicators": len(usage_indicators),
            "summary": f"Infrastructure shows {total_infra_indicators} indicators with {avg_coverage:.1f}% average coverage"
        }
        
        self.insights["infrastructure"] = insight
        return insight
    
    def insight_5_regional_disparities(self) -> Dict:
        """Generate insights on regional disparities"""
        
        if 'region' not in self.df.columns and 'location' not in self.df.columns:
            return {"error": "No regional data available"}
        
        value_col = self.get_value_column()
        region_col = 'region' if 'region' in self.df.columns else 'location'
        
        # Filter for regional data
        regional_data = self.df[self.df[region_col].notna()].copy()
        
        if regional_data.empty:
            return {"error": "No regional data found"}
        
        # Regional statistics
        regional_avg = regional_data.groupby(region_col)[value_col].mean()
        highest_region = regional_avg.idxmax()
        lowest_region = regional_avg.idxmin()
        
        regional_disparity = regional_avg.max() - regional_avg.min()
        
        insight = {
            "title": "Regional Disparities Analysis",
            "total_regions": len(regional_avg),
            "highest_region": highest_region,
            "highest_value": round(regional_avg.max(), 1),
            "lowest_region": lowest_region,
            "lowest_value": round(regional_avg.min(), 1),
            "disparity": round(regional_disparity, 1),
            "summary": f"Regional disparity of {regional_disparity:.1f}pp between {highest_region} and {lowest_region}"
        }
        
        self.insights["regional_disparities"] = insight
        return insight
    
    def generate_all_insights(self) -> Dict:
        """Generate all insights"""
        
        print("🔍 Generating comprehensive insights...")
        
        insights = {
            "insight_1": self.insight_1_account_ownership_trends(),
            "insight_2": self.insight_2_digital_payment_patterns(),
            "insight_3": self.insight_3_gender_gap_analysis(),
            "insight_4": self.insight_4_infrastructure_impact(),
            "insight_5": self.insight_5_regional_disparities()
        }
        
        # Filter out error insights
        valid_insights = {k: v for k, v in insights.items() if "error" not in v}
        
        print(f"✅ Generated {len(valid_insights)} valid insights")
        
        return valid_insights
    
    def print_insights_summary(self):
        """Print a formatted summary of all insights"""
        
        if not self.insights:
            self.generate_all_insights()
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE INSIGHTS SUMMARY")
        print("=" * 80)
        
        for i, (key, insight) in enumerate(self.insights.items(), 1):
            if "error" not in insight:
                print(f"\n{i}. {insight['title'].upper()}")
                print(f"   {insight['summary']}")
                
                # Print key metrics
                for metric_key, metric_value in insight.items():
                    if metric_key not in ['title', 'summary', 'error']:
                        print(f"   • {metric_key.replace('_', ' ').title()}: {metric_value}")
        
        print("\n" + "=" * 80)