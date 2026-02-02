# Ethiopia Financial Inclusion - Notebooks

This directory contains comprehensive Jupyter notebooks for exploratory data analysis and financial inclusion research.

## 📓 Available Notebooks

### 1. `comprehensive_eda.ipynb` - **Main EDA Notebook (Task 2)**
**Senior Data Scientist Level Analysis**

A comprehensive exploratory data analysis focusing on Ethiopia's financial inclusion dataset with:

#### 🎯 Key Features:
- **Dataset Breakdown**: Analysis by record_type, pillar, and sourcetype
- **5+ Key Insights**: Data-driven insights with visual evidence
- **Data Quality Assessment**: Comprehensive quality evaluation with documentation
- **Access Analysis**: In-depth account ownership trajectory analysis
- **Modular Code**: Reusable utilities with robust error handling

#### 📊 Generated Insights:
1. **Account Ownership Trends** - Growth patterns and demographic analysis
2. **Digital Payment Usage** - Platform adoption and usage patterns  
3. **Gender Gap Analysis** - Financial inclusion disparities by gender
4. **Infrastructure Impact** - Mobile/4G coverage correlation with access
5. **Event Timeline Analysis** - Policy interventions and their measurable impact

#### 🛠️ Technical Approach:
- Modular utilities in `../src/` for data loading, quality assessment, and visualization
- Robust error handling for missing columns and data inconsistencies
- Automated year extraction from multiple date formats
- Comprehensive statistical analysis with trend calculations
- Professional visualizations with consistent styling

### 2. `01_data_exploration_and_enrichment.ipynb` - **Task 1 Notebook**
Initial data exploration and enrichment work including:
- Schema explanation and record type analysis
- Data loading and basic exploration
- Enrichment with synthetic contextual events
- Impact link creation between events and indicators

## 🔧 Supporting Modules

### `../src/data_loader.py`
- Robust data loading with multiple format support
- Basic validation and error handling
- Flexible path management

### `../src/data_quality.py`
- Comprehensive data quality assessment
- Missing value analysis and visualization
- Consistency and validity checks
- Quality reporting with actionable insights

### `../src/visualization_utils.py`
- Standardized visualization utilities
- Consistent styling and color schemes
- Multiple chart types (trends, comparisons, distributions)
- Professional figure export capabilities

### `../src/analysis_utils.py`
- Statistical analysis functions
- Trend calculation and growth rate analysis
- Gender gap calculations
- Data gap identification
- Insight generation utilities

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Prepare Data**:
   - Place `ethiopia_fi_unified_data.xlsx` in `../data/raw/`
   - Place `reference_codes.xlsx` in `../data/raw/`

3. **Run Analysis**:
   - Start with `comprehensive_eda.ipynb` for complete analysis
   - All notebooks include error handling for missing data

## 📋 Analysis Outputs

### Visualizations
- Trend analysis charts
- Gender gap comparisons  
- Infrastructure impact correlations
- Event timeline visualizations
- Data quality heatmaps

### Documentation
- `../reports/eda_documentation.json` - Structured findings
- `../reports/figures/` - Exported visualizations
- Comprehensive insights and recommendations

### Key Metrics Tracked
- Account ownership rates by demographics
- Digital payment usage patterns
- Gender gaps in financial access
- Infrastructure coverage impact
- Policy intervention effectiveness

## 🎯 Business Value

This EDA provides:
- **Strategic Insights** for policy makers
- **Data-Driven Recommendations** for financial inclusion programs
- **Quality Assessment** for data governance
- **Trend Analysis** for forecasting models
- **Gap Identification** for targeted interventions

## 📊 Data Quality Standards

- Comprehensive missing value analysis
- Outlier detection and handling
- Consistency validation across record types
- Temporal data integrity checks
- Demographic breakdown completeness assessment

## Recommended Development Structure

- `01_data_exploration_and_enrichment.ipynb` - Initial exploration and enrichment
- `comprehensive_eda.ipynb` - **Main comprehensive analysis**
- `02_trend_analysis.ipynb` - Advanced trend analysis (future)
- `03_forecasting_models.ipynb` - Model development (future)
- `04_scenario_analysis.ipynb` - Scenario planning (future)

## Usage

1. Ensure you have activated the virtual environment
2. Install Jupyter: `pip install jupyter`
3. Start Jupyter: `jupyter notebook`
4. Navigate to this directory and open the desired notebook

## Data Access

Notebooks reference data using relative paths:
- Raw data: `../data/raw/`
- Processed data: `../data/processed/`
- Model outputs: `../models/`
- Reports: `../reports/`

---

**Note**: All notebooks are designed with robust error handling to work with varying data structures and missing columns, ensuring reliable analysis regardless of data completeness.