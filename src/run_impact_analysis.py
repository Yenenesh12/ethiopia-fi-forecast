"""
Run Event Impact Analysis for Task 3

This script executes the complete event impact modeling workflow:
1. Load and process data
2. Define key events and impacts
3. Build impact matrices
4. Validate against historical data
5. Generate visualizations and reports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent))

from impact_modeling import EventImpactModel, create