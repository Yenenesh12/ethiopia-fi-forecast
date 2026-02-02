"""
Data quality assessment utilities for Ethiopia Financial Inclusion EDA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class DataQualityAssessment:
    """Class for comprehensive data quality assessment"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.quality_report = {}
        
    def assess_completeness(self) -> Dict:
        """Assess data completeness"""
        completeness = {}
        
        # Missing values by column
        missing_counts = self.df.isnull().sum()
        missing_percentages = (missing_counts / len(self.df)) * 100
        
        completeness['missing_by_column'] = {
            'counts': missing_counts.to_dict(),
            'percentages': missing_percentages.to_dict()
        }
        
        # Missing values by record type (if column exists)
        if 'record_type' in self.df.columns:
            missing_by_type = {}
            for record_type in self.df['record_type'].unique():
                subset = self.df[self.df['record_type'] == record_type]
                missing_by_type[record_type] = (subset.isnull().sum() / len(subset) * 100).to_dict()
            completeness['missing_by_record_type'] = missing_by_type
        
        return completeness
    
    def assess_consistency(self) -> Dict:
        """Assess data consistency"""
        consistency = {}
        
        # Check for duplicate records
        consistency['duplicate_records'] = self.df.duplicated().sum()
        
        # Check data type consistency
        consistency['data_types'] = self.df.dtypes.to_dict()
        
        # Check for inconsistent categorical values
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        inconsistent_values = {}
        
        for col in categorical_cols:
            unique_vals = self.df[col].dropna().unique()
            if len(unique_vals) > 50:  # Skip columns with too many unique values
                continue
            
            # Look for potential inconsistencies (case, spacing, etc.)
            normalized_vals = [str(val).strip().lower() for val in unique_vals]
            if len(set(normalized_vals)) < len(unique_vals):
                inconsistent_values[col] = list(unique_vals)
        
        consistency['potential_inconsistencies'] = inconsistent_values
        
        return consistency
    
    def assess_validity(self) -> Dict:
        """Assess data validity"""
        validity = {}
        
        # Check for negative values where they shouldn't exist
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        negative_values = {}
        
        for col in numeric_cols:
            if col in ['value', 'year']:  # Columns that shouldn't have negative values
                neg_count = (self.df[col] < 0).sum()
                if neg_count > 0:
                    negative_values[col] = neg_count
        
        validity['negative_values'] = negative_values
        
        # Check year ranges
        if 'year' in self.df.columns:
            year_stats = {
                'min_year': self.df['year'].min(),
                'max_year': self.df['year'].max(),
                'future_years': (self.df['year'] > 2024).sum(),
                'very_old_years': (self.df['year'] < 1990).sum()
            }
            validity['year_validity'] = year_stats
        
        # Check value ranges for percentages
        if 'value' in self.df.columns and 'unit' in self.df.columns:
            percentage_mask = self.df['unit'] == 'percentage'
            if percentage_mask.any():
                pct_values = self.df.loc[percentage_mask, 'value']
                validity['percentage_validity'] = {
                    'values_over_100': (pct_values > 100).sum(),
                    'negative_percentages': (pct_values < 0).sum()
                }
        
        return validity
    
    def generate_quality_report(self) -> Dict:
        """Generate comprehensive quality report"""
        self.quality_report = {
            'completeness': self.assess_completeness(),
            'consistency': self.assess_consistency(),
            'validity': self.assess_validity(),
            'summary_stats': {
                'total_records': len(self.df),
                'total_columns': len(self.df.columns),
                'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2
            }
        }
        
        return self.quality_report
    
    def visualize_missing_data(self, figsize: Tuple[int, int] = (12, 8)):
        """Visualize missing data patterns"""
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Data Quality Assessment: Missing Values', fontsize=16, fontweight='bold')
        
        # Missing values by column
        missing_counts = self.df.isnull().sum()
        missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=True)
        
        if not missing_counts.empty:
            axes[0, 0].barh(range(len(missing_counts)), missing_counts.values)
            axes[0, 0].set_yticks(range(len(missing_counts)))
            axes[0, 0].set_yticklabels(missing_counts.index)
            axes[0, 0].set_xlabel('Missing Count')
            axes[0, 0].set_title('Missing Values by Column')
        else:
            axes[0, 0].text(0.5, 0.5, 'No missing values found', ha='center', va='center')
            axes[0, 0].set_title('Missing Values by Column')
        
        # Missing values percentage
        missing_pct = (self.df.isnull().sum() / len(self.df) * 100)
        missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=True)
        
        if not missing_pct.empty:
            axes[0, 1].barh(range(len(missing_pct)), missing_pct.values)
            axes[0, 1].set_yticks(range(len(missing_pct)))
            axes[0, 1].set_yticklabels(missing_pct.index)
            axes[0, 1].set_xlabel('Missing Percentage (%)')
            axes[0, 1].set_title('Missing Values Percentage')
        else:
            axes[0, 1].text(0.5, 0.5, 'No missing values found', ha='center', va='center')
            axes[0, 1].set_title('Missing Values Percentage')
        
        # Heatmap of missing values (sample if too large)
        sample_size = min(1000, len(self.df))
        df_sample = self.df.sample(n=sample_size) if len(self.df) > sample_size else self.df
        
        missing_matrix = df_sample.isnull()
        if missing_matrix.any().any():
            sns.heatmap(missing_matrix, cbar=True, ax=axes[1, 0], cmap='viridis')
            axes[1, 0].set_title(f'Missing Values Heatmap (Sample: {sample_size})')
        else:
            axes[1, 0].text(0.5, 0.5, 'No missing values to display', ha='center', va='center')
            axes[1, 0].set_title('Missing Values Heatmap')
        
        # Missing values by record type (if available)
        if 'record_type' in self.df.columns:
            missing_by_type = []
            record_types = []
            
            for record_type in self.df['record_type'].unique():
                subset = self.df[self.df['record_type'] == record_type]
                missing_pct = (subset.isnull().sum().sum() / (len(subset) * len(subset.columns))) * 100
                missing_by_type.append(missing_pct)
                record_types.append(record_type)
            
            axes[1, 1].bar(record_types, missing_by_type)
            axes[1, 1].set_xlabel('Record Type')
            axes[1, 1].set_ylabel('Missing Percentage (%)')
            axes[1, 1].set_title('Missing Values by Record Type')
            axes[1, 1].tick_params(axis='x', rotation=45)
        else:
            axes[1, 1].text(0.5, 0.5, 'No record_type column found', ha='center', va='center')
            axes[1, 1].set_title('Missing Values by Record Type')
        
        plt.tight_layout()
        plt.show()
    
    def print_quality_summary(self):
        """Print a summary of data quality issues"""
        if not self.quality_report:
            self.generate_quality_report()
        
        print("=" * 60)
        print("DATA QUALITY ASSESSMENT SUMMARY")
        print("=" * 60)
        
        # Summary stats
        summary = self.quality_report['summary_stats']
        print(f"📊 Dataset Overview:")
        print(f"   • Total Records: {summary['total_records']:,}")
        print(f"   • Total Columns: {summary['total_columns']}")
        print(f"   • Memory Usage: {summary['memory_usage_mb']:.2f} MB")
        
        # Completeness issues
        completeness = self.quality_report['completeness']
        missing_cols = {k: v for k, v in completeness['missing_by_column']['counts'].items() if v > 0}
        
        print(f"\n🔍 Completeness Issues:")
        if missing_cols:
            print(f"   • Columns with missing values: {len(missing_cols)}")
            for col, count in sorted(missing_cols.items(), key=lambda x: x[1], reverse=True)[:5]:
                pct = completeness['missing_by_column']['percentages'][col]
                print(f"     - {col}: {count:,} ({pct:.1f}%)")
        else:
            print("   • No missing values found ✅")
        
        # Consistency issues
        consistency = self.quality_report['consistency']
        print(f"\n🔄 Consistency Issues:")
        print(f"   • Duplicate records: {consistency['duplicate_records']:,}")
        
        inconsistencies = consistency['potential_inconsistencies']
        if inconsistencies:
            print(f"   • Columns with potential inconsistencies: {len(inconsistencies)}")
            for col in list(inconsistencies.keys())[:3]:
                print(f"     - {col}: {len(inconsistencies[col])} unique values")
        else:
            print("   • No obvious inconsistencies found ✅")
        
        # Validity issues
        validity = self.quality_report['validity']
        print(f"\n✅ Validity Issues:")
        
        if validity['negative_values']:
            print(f"   • Columns with negative values:")
            for col, count in validity['negative_values'].items():
                print(f"     - {col}: {count:,} negative values")
        
        if 'year_validity' in validity:
            year_stats = validity['year_validity']
            print(f"   • Year range: {year_stats['min_year']} - {year_stats['max_year']}")
            if year_stats['future_years'] > 0:
                print(f"     - Future years: {year_stats['future_years']:,}")
            if year_stats['very_old_years'] > 0:
                print(f"     - Very old years (< 1990): {year_stats['very_old_years']:,}")
        
        print("\n" + "=" * 60)