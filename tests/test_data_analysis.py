"""
Unit Tests for Data Analysis Module
Task 5: Testing & Quality Assurance
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import sys
import os

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_analysis import EthiopiaDataAnalyzer

class TestEthiopiaDataAnalyzer:
    """Test suite for EthiopiaDataAnalyzer class"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample test data"""
        data = {
            'record_id': ['REC_001', 'REC_002', 'REC_003', 'REC_004'],
            'record_type': ['observation', 'observation', 'event', 'observation'],
            'indicator': ['Account Ownership Rate', 'Account Ownership Rate', 'Policy Event', 'Mobile Money Account Rate'],
            'indicator_code': ['ACC_OWNERSHIP', 'ACC_OWNERSHIP', 'POLICY_EVENT', 'ACC_MM_ACCOUNT'],
            'value_numeric': [22.0, 35.0, np.nan, 4.7],
            'year': [2017, 2018, 2019, 2021],
            'gender': ['all', 'all', 'all', 'all'],
            'pillar': ['ACCESS', 'ACCESS', 'POLICY', 'ACCESS'],
            'source_name': ['Global Findex', 'Global Findex', 'NBE', 'Global Findex']
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def temp_csv_file(self, sample_data):
        """Create temporary CSV file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_data.to_csv(f.name, index=False)
            yield f.name
        os.unlink(f.name)
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = EthiopiaDataAnalyzer("dummy_path.csv")
        assert analyzer.data_path == Path("dummy_path.csv")
        assert analyzer.df is None
        assert analyzer.summary_stats == {}
    
    def test_load_data_success(self, temp_csv_file):
        """Test successful data loading"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        df = analyzer.load_data()
        
        assert df is not None
        assert len(df) == 4
        assert 'indicator' in df.columns
        assert 'value_numeric' in df.columns
    
    def test_load_data_file_not_found(self):
        """Test data loading with non-existent file"""
        analyzer = EthiopiaDataAnalyzer("non_existent_file.csv")
        df = analyzer.load_data()
        assert df is None
    
    def test_explore_data_structure(self, temp_csv_file):
        """Test data structure exploration"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        analyzer.load_data()
        
        missing_summary = analyzer.explore_data_structure()
        
        assert isinstance(missing_summary, pd.DataFrame)
        assert 'Missing_Count' in missing_summary.columns
        assert 'Missing_Percentage' in missing_summary.columns
    
    def test_analyze_indicators(self, temp_csv_file):
        """Test indicator analysis"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        analyzer.load_data()
        
        indicator_counts = analyzer.analyze_indicators()
        
        assert isinstance(indicator_counts, pd.Series)
        assert 'Account Ownership Rate' in indicator_counts.index
    
    def test_identify_data_gaps(self, temp_csv_file):
        """Test data gap identification"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        analyzer.load_data()
        
        gaps = analyzer.identify_data_gaps()
        
        assert isinstance(gaps, dict)
        assert 'missing_years' in gaps
        assert 'available_years' in gaps
        assert isinstance(gaps['available_years'], list)
    
    def test_clean_data(self, temp_csv_file):
        """Test data cleaning functionality"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        analyzer.load_data()
        
        initial_length = len(analyzer.df)
        cleaned_df = analyzer.clean_data()
        
        assert cleaned_df is not None
        assert len(cleaned_df) <= initial_length  # Should not increase records
        assert cleaned_df['year'].dtype in [np.int64, np.float64]  # Should be numeric
    
    def test_generate_summary_report(self, temp_csv_file):
        """Test summary report generation"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        analyzer.load_data()
        
        summary = analyzer.generate_summary_report()
        
        assert isinstance(summary, dict)
        required_keys = ['total_records', 'unique_indicators', 'year_span', 'data_completeness']
        for key in required_keys:
            assert key in summary
        
        assert summary['total_records'] > 0
        assert summary['unique_indicators'] > 0
        assert 0 <= summary['data_completeness'] <= 100
    
    def test_export_cleaned_data(self, temp_csv_file):
        """Test data export functionality"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        analyzer.load_data()
        analyzer.clean_data()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_output.csv"
            result_path = analyzer.export_cleaned_data(str(output_path))
            
            assert result_path.exists()
            
            # Verify exported data can be read back
            exported_df = pd.read_csv(result_path)
            assert len(exported_df) > 0
    
    def test_run_full_analysis(self, temp_csv_file):
        """Test complete analysis pipeline"""
        analyzer = EthiopiaDataAnalyzer(temp_csv_file)
        
        results = analyzer.run_full_analysis()
        
        assert results is not None
        assert 'data' in results
        assert 'summary' in results
        assert 'gaps' in results
        
        assert isinstance(results['data'], pd.DataFrame)
        assert isinstance(results['summary'], dict)
        assert isinstance(results['gaps'], dict)

class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty dataframes"""
        analyzer = EthiopiaDataAnalyzer()
        analyzer.df = pd.DataFrame()  # Empty dataframe
        
        # Should handle empty data gracefully
        missing_summary = analyzer.explore_data_structure()
        # Should not crash, may return None or empty results
    
    def test_missing_columns_handling(self):
        """Test handling of missing expected columns"""
        analyzer = EthiopiaDataAnalyzer()
        # Create dataframe with minimal columns
        analyzer.df = pd.DataFrame({
            'indicator': ['Test Indicator'],
            'year': [2020]
        })
        
        # Should handle missing columns gracefully
        try:
            analyzer.analyze_indicators()
            analyzer.identify_data_gaps()
        except KeyError:
            pytest.fail("Should handle missing columns gracefully")
    
    def test_invalid_data_types(self):
        """Test handling of invalid data types"""
        analyzer = EthiopiaDataAnalyzer()
        analyzer.df = pd.DataFrame({
            'indicator': ['Test'],
            'year': ['invalid_year'],  # String instead of number
            'value_numeric': ['invalid_number']  # String instead of number
        })
        
        # Should handle invalid data types in cleaning
        cleaned_df = analyzer.clean_data()
        assert cleaned_df is not None

if __name__ == "__main__":
    pytest.main([__file__])