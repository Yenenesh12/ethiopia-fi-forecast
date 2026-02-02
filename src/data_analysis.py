"""
Data Analysis & Enrichment Module
Comprehensive data loading, exploration, cleaning, and gap analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class EthiopiaDataAnalyzer:
    """Main class for Ethiopia financial inclusion data analysis"""
    
    def __init__(self, data_path="data/processed/ethiopia_fi_unified_data_enriched.csv"):
        self.data_path = Path(data_path)
        self.df = None
        self.summary_stats = {}
        
    def load_data(self):
        """Load and perform initial data exploration"""
        print("📊 Loading Ethiopia FI unified data...")
        
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Data loaded successfully: {len(self.df)} records")
            
            # Basic info
            print(f"📋 Dataset shape: {self.df.shape}")
            print(f"📅 Date range: {self.df['year'].min()} - {self.df['year'].max()}")
            
            return self.df
            
        except FileNotFoundError:
            print(f"❌ File not found: {self.data_path}")
            return None
            
    def explore_data_structure(self):
        """Comprehensive data structure exploration"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return
            
        print("\n🔍 DATA STRUCTURE EXPLORATION")
        print("=" * 50)
        
        # Column info
        print(f"📊 Total columns: {len(self.df.columns)}")
        print(f"📊 Data types:\n{self.df.dtypes.value_counts()}")
        
        # Missing data analysis
        missing_data = self.df.isnull().sum()
        missing_pct = (missing_data / len(self.df)) * 100
        
        missing_summary = pd.DataFrame({
            'Missing_Count': missing_data,
            'Missing_Percentage': missing_pct
        }).sort_values('Missing_Percentage', ascending=False)
        
        print(f"\n📉 Missing Data Summary (Top 10):")
        print(missing_summary.head(10))
        
        # Record types
        if 'record_type' in self.df.columns:
            print(f"\n📋 Record Types:")
            print(self.df['record_type'].value_counts())
            
        # Categories and pillars
        if 'category' in self.df.columns:
            print(f"\n🏛️ Categories:")
            print(self.df['category'].value_counts())
            
        if 'pillar' in self.df.columns:
            print(f"\n🏛️ Pillars:")
            print(self.df['pillar'].value_counts())
            
        return missing_summary
        
    def analyze_indicators(self):
        """Analyze unique indicators and their characteristics"""
        if self.df is None:
            return
            
        print("\n🎯 INDICATOR ANALYSIS")
        print("=" * 50)
        
        # Unique indicators
        unique_indicators = self.df['indicator'].nunique()
        print(f"📊 Total unique indicators: {unique_indicators}")
        
        # Indicator frequency
        indicator_counts = self.df['indicator'].value_counts()
        print(f"\n📈 Top 10 Most Frequent Indicators:")
        print(indicator_counts.head(10))
        
        # Indicator codes
        if 'indicator_code' in self.df.columns:
            unique_codes = self.df['indicator_code'].nunique()
            print(f"\n🔢 Unique indicator codes: {unique_codes}")
            
        # Value types
        if 'value_type' in self.df.columns:
            print(f"\n📊 Value Types:")
            print(self.df['value_type'].value_counts())
            
        # Numeric vs text values
        numeric_values = self.df['value_numeric'].notna().sum()
        text_values = self.df['value_text'].notna().sum()
        
        print(f"\n📊 Value Distribution:")
        print(f"   Numeric values: {numeric_values}")
        print(f"   Text values: {text_values}")
        
        return indicator_counts
        
    def identify_data_gaps(self):
        """Identify gaps in data coverage"""
        if self.df is None:
            return
            
        print("\n🕳️ DATA GAP ANALYSIS")
        print("=" * 50)
        
        # Time coverage gaps
        years_available = sorted(self.df['year'].dropna().unique())
        year_range = range(int(min(years_available)), int(max(years_available)) + 1)
        missing_years = [year for year in year_range if year not in years_available]
        
        print(f"📅 Available years: {years_available}")
        if missing_years:
            print(f"❌ Missing years: {missing_years}")
        else:
            print("✅ No missing years in range")
            
        # Gender coverage
        if 'gender' in self.df.columns:
            gender_coverage = self.df['gender'].value_counts()
            print(f"\n👥 Gender Coverage:")
            print(gender_coverage)
            
            # Gender gaps by indicator
            gender_gaps = []
            for indicator in self.df['indicator'].unique():
                indicator_data = self.df[self.df['indicator'] == indicator]
                genders = indicator_data['gender'].unique()
                if len(genders) < 3:  # Should have 'all', 'male', 'female'
                    gender_gaps.append(indicator)
                    
            if gender_gaps:
                print(f"\n❌ Indicators missing gender disaggregation ({len(gender_gaps)}):")
                for gap in gender_gaps[:5]:  # Show first 5
                    print(f"   • {gap}")
                    
        # Regional coverage
        if 'region' in self.df.columns:
            region_coverage = self.df['region'].value_counts()
            print(f"\n🗺️ Regional Coverage:")
            print(region_coverage)
            
        # Source diversity
        if 'source_name' in self.df.columns:
            source_coverage = self.df['source_name'].value_counts()
            print(f"\n📚 Data Sources:")
            print(source_coverage)
            
        return {
            'missing_years': missing_years,
            'gender_gaps': gender_gaps if 'gender' in self.df.columns else [],
            'available_years': years_available
        }
        
    def clean_data(self):
        """Perform data cleaning operations"""
        if self.df is None:
            return
            
        print("\n🧹 DATA CLEANING")
        print("=" * 50)
        
        initial_records = len(self.df)
        
        # Remove completely empty rows
        self.df = self.df.dropna(how='all')
        print(f"🗑️ Removed {initial_records - len(self.df)} completely empty rows")
        
        # Standardize year column
        if 'year' in self.df.columns:
            # Convert year to integer where possible
            self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')
            
        # Standardize numeric values
        if 'value_numeric' in self.df.columns:
            self.df['value_numeric'] = pd.to_numeric(self.df['value_numeric'], errors='coerce')
            
        # Clean gender values
        if 'gender' in self.df.columns:
            gender_mapping = {
                'All': 'all',
                'ALL': 'all',
                'Male': 'male',
                'MALE': 'male',
                'Female': 'female',
                'FEMALE': 'female'
            }
            self.df['gender'] = self.df['gender'].replace(gender_mapping)
            
        # Clean indicator codes
        if 'indicator_code' in self.df.columns:
            self.df['indicator_code'] = self.df['indicator_code'].str.upper().str.strip()
            
        print(f"✅ Data cleaning complete. Final records: {len(self.df)}")
        
        return self.df
        
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        if self.df is None:
            return
            
        print("\n📋 SUMMARY REPORT")
        print("=" * 50)
        
        # Basic statistics
        total_records = len(self.df)
        unique_indicators = self.df['indicator'].nunique()
        year_span = self.df['year'].max() - self.df['year'].min()
        
        # Access vs Usage indicators
        access_indicators = self.df[self.df['pillar'] == 'ACCESS']['indicator'].nunique()
        usage_indicators = self.df[self.df['pillar'] == 'USAGE']['indicator'].nunique()
        
        # Data quality metrics
        completeness = (1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        
        summary = {
            'total_records': total_records,
            'unique_indicators': unique_indicators,
            'year_span': year_span,
            'access_indicators': access_indicators,
            'usage_indicators': usage_indicators,
            'data_completeness': round(completeness, 2),
            'latest_year': int(self.df['year'].max()),
            'earliest_year': int(self.df['year'].min())
        }
        
        print(f"📊 Total Records: {summary['total_records']:,}")
        print(f"🎯 Unique Indicators: {summary['unique_indicators']}")
        print(f"📅 Time Span: {summary['year_span']} years ({summary['earliest_year']}-{summary['latest_year']})")
        print(f"🏛️ Access Indicators: {summary['access_indicators']}")
        print(f"🏛️ Usage Indicators: {summary['usage_indicators']}")
        print(f"✅ Data Completeness: {summary['data_completeness']}%")
        
        self.summary_stats = summary
        return summary
        
    def export_cleaned_data(self, output_path="data/processed/ethiopia_fi_cleaned.csv"):
        """Export cleaned data"""
        if self.df is None:
            return
            
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        print(f"💾 Cleaned data exported to: {output_path}")
        
        return output_path
        
    def run_full_analysis(self):
        """Run complete data analysis pipeline"""
        print("🚀 STARTING COMPREHENSIVE DATA ANALYSIS")
        print("=" * 60)
        
        # Load data
        self.load_data()
        if self.df is None:
            return
            
        # Explore structure
        self.explore_data_structure()
        
        # Analyze indicators
        self.analyze_indicators()
        
        # Identify gaps
        gaps = self.identify_data_gaps()
        
        # Clean data
        self.clean_data()
        
        # Generate summary
        summary = self.generate_summary_report()
        
        # Export cleaned data
        self.export_cleaned_data()
        
        print("\n✅ ANALYSIS COMPLETE!")
        print("=" * 60)
        
        return {
            'data': self.df,
            'summary': summary,
            'gaps': gaps
        }

def main():
    """Main execution function"""
    analyzer = EthiopiaDataAnalyzer()
    results = analyzer.run_full_analysis()
    return results

if __name__ == "__main__":
    main()