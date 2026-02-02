# Ethiopia Financial Inclusion Forecasting

A comprehensive data science project for analyzing and forecasting financial inclusion indicators in Ethiopia using Global Findex data and contextual policy/infrastructure events.

## 📊 Current Status: Task 2 Completed

### ✅ Task 2: Senior Data Scientist EDA - **COMPLETED**

**Comprehensive exploratory data analysis with professional-grade insights and visualizations:**

#### 🎯 Deliverables Completed:
- **Dataset Breakdown**: Complete analysis by record_type, pillar, and sourcetype
- **5+ Key Insights**: Data-driven insights with visual evidence:
  1. Account Ownership Trends - Growth patterns and demographic analysis
  2. Digital Payment Usage - Platform adoption and usage patterns  
  3. Gender Gap Analysis - Financial inclusion disparities by gender
  4. Infrastructure Impact - Mobile/4G coverage correlation with access
  5. Event Timeline Analysis - Policy interventions and measurable impact
- **Data Quality Assessment**: Comprehensive evaluation with documentation
- **Access Analysis**: In-depth account ownership trajectory with charts
- **Modular Code**: Reusable utilities with robust error handling

#### 🛠️ Technical Implementation:
- **Modular Architecture**: Separate utilities for data loading, quality assessment, and visualization
- **Robust Error Handling**: Works with varying data structures and missing columns
- **Professional Visualizations**: Consistent styling with publication-ready charts
- **Comprehensive Documentation**: Structured findings and recommendations
- **Repository Best Practices**: Proper folder structure, README files, and code organization

#### 📁 Key Files Created:
- `notebooks/comprehensive_eda.ipynb` - Main EDA notebook with all analyses
- `src/data_loader.py` - Robust data loading utilities
- `src/data_quality.py` - Comprehensive quality assessment tools
- `src/visualization_utils.py` - Professional visualization utilities
- `src/analysis_utils.py` - Statistical analysis and insight generation
- Updated documentation and README files

---

## Project Overview

This project focuses on Ethiopia's digital financial transformation using two key Global Findex indicators:
- **Account Ownership (Access)**: Percentage of adults with accounts at financial institutions or mobile money providers
- **Digital Payment Usage (Usage)**: Percentage of adults who made or received digital payments

## Project Structure

```
ethiopia-fi-forecast/
├── .github/workflows/          # CI/CD workflows
│   └── unittests.yml
├── data/
│   ├── raw/                    # Original datasets
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/              # Analysis-ready data
├── notebooks/                  # Jupyter notebooks for analysis
├── src/                        # Source code modules
├── dashboard/                  # Interactive dashboard
│   └── app.py
├── tests/                      # Unit and integration tests
├── models/                     # Trained models and artifacts
├── reports/                    # Analysis reports and figures
│   └── figures/
├── requirements.txt
├── README.md
└── .gitignore
```

## Data Schema

The project uses a unified schema with four record types:

### Record Types
1. **observation**: Actual measured data points from surveys/official sources
2. **event**: Policy changes, infrastructure developments, or program launches
3. **impact_link**: Connects events to indicators showing causal relationships
4. **target**: Forecasted or target values for planning purposes

### Key Fields
- `record_id`: Unique identifier for each record
- `record_type`: One of the four types above
- `parent_id`: Links impact_link records to event records
- `indicator_code`: FI_ACCESS_ACCOUNT or FI_USAGE_DIGITAL_PAY
- `year`: Time dimension
- `value`: Numeric value (percentage, count, etc.)
- `confidence`: High/Medium/Low data quality indicator

## Getting Started

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <https://github.com/Yenenesh12/ethiopia-fi-forecast.git>
cd ethiopia-fi-forecast
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

1. **Data Exploration**: Start with notebooks in the `notebooks/` directory
2. **Dashboard**: Run the interactive dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
3. **Analysis**: Use the modules in `src/` for custom analysis
4. **Testing**: Run tests with `pytest tests/`

## Key Features

- **Unified Data Schema**: Combines observations, events, and causal links
- **Multi-dimensional Analysis**: Gender, age, region, income, education breakdowns
- **Event Impact Modeling**: Links policy/infrastructure events to outcomes
- **Interactive Dashboard**: Real-time visualization and scenario planning
- **Forecasting Models**: Statistical and ML approaches for prediction

## Data Sources

- **Global Findex Database**: World Bank financial inclusion surveys
- **National Bank of Ethiopia**: Regulatory and policy information
- **Ethiopian Telecommunications**: Infrastructure and service data
- **Government Publications**: Policy documents and strategic plans

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or collaboration opportunities, please contact the Financial Inclusion Research Team.