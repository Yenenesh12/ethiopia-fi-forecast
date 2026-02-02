"""
Unit Tests for Visualization Engine Module
Task 5: Testing & Quality Assurance
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pathlib import Path
import tempfile
import sys
import os

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from visualization_engine import VisualizationEngine

class TestVisualizationEngine:
    """Test suite for VisualizationEngine class"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample test data for visualization"""
        data = {
            'record_id': ['REC_001', 'REC_002', 'REC_003', 'REC_004', 'REC_005'],
            'indicator': ['Account Ownership Rate', 'Account Ownership Rate', 'Mobile Money Account Rate', 'Account Ownership Rate', 'Account Ownership Rate'],
            'value_numeric': [22.0, 35.0, 4.7, 56.0, 36.0],
            'year': [2017, 2018, 2021, 2021, 2021],
            'gender': ['all', 'all', 'all', 'male', 'female'],
            'pillar': ['ACCESS', 'ACCESS', 'ACCESS', 'ACCESS', 'ACCESS'],
            'region': [np.nan, np.nan, np.nan, 'Addis Ababa', 'Addis Ababa']
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def temp_csv_file(self, sample_data):
        """Create temporary CSV file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_data.to_csv(f.name, index=False)
            yield f.name
        os.unlink(f.name)
    
    @pytest.fixture
    def viz_engine(self, temp_csv_file):
        """Create VisualizationEngine instance with test data"""
        return VisualizationEngine(temp_csv_file)
    
    def test_engine_initialization(self, temp_csv_file):
        """Test visualization engine initialization"""
        engine = VisualizationEngine(temp_csv_file)
        
        assert engine.data_path == Path(temp_csv_file)
        assert engine.df is not None
        assert len(engine.df) > 0
        assert engine.events_data is not None
       