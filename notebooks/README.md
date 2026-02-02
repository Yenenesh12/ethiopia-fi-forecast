# Notebooks Directory

This directory contains Jupyter notebooks for exploratory data analysis, model development, and visualization.

## Recommended Structure

- `01_data_exploration.ipynb` - Initial data exploration and understanding
- `02_data_enrichment.ipynb` - Data enrichment and feature engineering
- `03_trend_analysis.ipynb` - Trend analysis and pattern identification
- `04_forecasting_models.ipynb` - Model development and evaluation
- `05_scenario_analysis.ipynb` - Scenario planning and sensitivity analysis

## Usage

1. Ensure you have activated the virtual environment
2. Install Jupyter: `pip install jupyter`
3. Start Jupyter: `jupyter notebook`
4. Navigate to this directory and open the desired notebook

## Data Access

Notebooks should reference data using relative paths:
- Raw data: `../data/raw/`
- Processed data: `../data/processed/`
- Model outputs: `../models/`