"""
Data loading utilities for Ethiopia Financial Inclusion EDA
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Class for loading and basic validation of financial inclusion data"""
    
    def __init__(self, data_path: str = "../data"):
        self.data_path = Path(data_path)
        self.raw_path = self.data_path / "raw"
        self.processed_path = self.data_path / "processed"
        
    def load_main_dataset(self, filename: str = "ethiopia_fi_unified_data.csv") -> Optional[pd.DataFrame]:
        """
        Load the main financial inclusion dataset
        
        Args:
            filename: Name of the dataset file
            
        Returns:
            DataFrame or None if loading fails
        """
        try:
            # Try processed first, then raw
            for path in [self.processed_path, self.raw_path]:
                file_path = path / filename
                if file_path.exists():
                    logger.info(f"Loading dataset from {file_path}")
                    
                    # Try different file formats
                    if filename.endswith('.csv'):
                        df = pd.read_csv(file_path)
                    elif filename.endswith('.xlsx'):
                        df = pd.read_excel(file_path)
                    else:
                        # Try CSV first, then Excel
                        try:
                            df = pd.read_csv(file_path)
                        except:
                            df = pd.read_excel(file_path)
                    
                    logger.info(f"Dataset loaded successfully: {df.shape}")
                    return df
                    
            logger.error(f"Dataset file {filename} not found in {self.data_path}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return None
    
    def load_reference_codes(self, filename: str = "reference_codes.csv") -> Optional[pd.DataFrame]:
        """
        Load reference codes dataset
        
        Args:
            filename: Name of the reference codes file
            
        Returns:
            DataFrame or None if loading fails
        """
        try:
            for path in [self.processed_path, self.raw_path]:
                file_path = path / filename
                if file_path.exists():
                    logger.info(f"Loading reference codes from {file_path}")
                    
                    if filename.endswith('.csv'):
                        df = pd.read_csv(file_path)
                    else:
                        df = pd.read_excel(file_path)
                    
                    # Normalize column names
                    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
                    
                    logger.info(f"Reference codes loaded: {df.shape}")
                    return df
                    
            logger.warning(f"Reference codes file {filename} not found")
            return None
            
        except Exception as e:
            logger.error(f"Error loading reference codes: {e}")
            return None
    
    def validate_dataset(self, df: pd.DataFrame) -> dict:
        """
        Perform basic validation on the dataset
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_rows': df.duplicated().sum(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        # Check for expected columns
        expected_cols = ['record_type', 'indicator_code', 'year', 'value']
        missing_expected = [col for col in expected_cols if col not in df.columns]
        validation_results['missing_expected_columns'] = missing_expected
        
        return validation_results