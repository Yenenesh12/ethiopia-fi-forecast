"""
Impact Modeling & Forecasting Module
Event-indicator association matrix, regression modeling, and scenario analysis
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class ImpactModeler:
    """Advanced impact modeling and forecasting for Ethiopia FI data"""
    
    def __init__(self, data_path="data/processed/ethiopia_fi_unified_data_enriched.csv"):
        self.data_path = Path(data_path)
        self.df = None
        self.models = {}
        self.forecasts = {}
        self.event_matrix = None
        self.load_data()
        
    def load_data(self):
        """Load and prepare data for modeling"""
        try:
            self.df = pd.read_csv(self.data_path)
            self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')
            self.df['value_numeric'] = pd.to_numeric(self.df['value_numeric'], errors='coerce')
            
            # Define events with detailed impact data
            self.events_data = [
                {'year': 2016, 'event': 'Digital Finance Strategy', 'impact': 8, 'type': 'Policy', 'duration': 2},
                {'year': 2019, 'event': 'EthSwitch Launch', 'impact': 5, 'type': 'Infrastructure', 'duration': 1},
                {'year': 2020, 'event': 'Mobile Money Regulation', 'impact': 7, 'type': 'Regulatory', 'duration': 1},
                {'year': 2021, 'event': 'Telebirr Launch', 'impact': 15, 'type': 'Technology', 'duration': 2},
                {'year': 2022, 'event': 'Agent Banking Expansion', 'impact': 3, 'type': 'Infrastructure', 'duration': 3},
                {'year': 2023, 'event': '4G Network Expansion', 'impact': 6, 'type': 'Infrastructure', 'duration': 2}
            ]
            
            print(f"✅ Data loaded for modeling: {len(self.df)} records")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            
    def create_event_indicator_matrix(self):
        """Create event-indicator association matrix"""
        
        print("🔗 CREATING EVENT-INDICATOR ASSOCIATION MATRIX")
        print("=" * 55)
        
        # Define indicators and their sensitivity to different event types
        indicators = [
            'Account Ownership Rate',
            'Mobile Money Account Rate', 
            'Digital Payment Usage',
            'Agent Banking Usage',
            '4G Population Coverage'
        ]
        
        events = [event['event'] for event in self.events_data]
        
        # Create impact matrix based on event type and indicator relationship
        # Values represent expected impact in percentage points
        impact_matrix = np.array([
            [8, 2, 3, 1, 0],    # Digital Finance Strategy
            [3, 1, 5, 2, 1],    # EthSwitch Launch  
            [5, 8, 4, 3, 0],    # Mobile Money Regulation
            [12, 15, 8, 5, 2],  # Telebirr Launch
            [2, 3, 2, 8, 1],    # Agent Banking Expansion
            [1, 2, 1, 1, 6]     # 4G Network Expansion
        ])
        
        # Create DataFrame
        self.event_matrix = pd.DataFrame(
            impact_matrix,
            index=events,
            columns=indicators
        )
        
        print("📊 Event-Indicator Impact Matrix:")
        print(self.event_matrix)
        
        # Calculate event effectiveness scores
        event_scores = self.event_matrix.sum(axis=1).sort_values(ascending=False)
        print(f"\n🏆 Most Effective Events:")
        for event, score in event_scores.head(3).items():
            print(f"   • {event}: {score} total impact points")
            
        # Calculate indicator sensitivity
        indicator_sensitivity = self.event_matrix.sum(axis=0).sort_values(ascending=False)
        print(f"\n📈 Most Event-Sensitive Indicators:")
        for indicator, sensitivity in indicator_sensitivity.head(3).items():
            print(f"   • {indicator}: {sensitivity} total sensitivity")
            
        return self.event_matrix
        
    def build_regression_models(self):
        """Build regression models for key indicators"""
        
        print("\n🤖 BUILDING REGRESSION MODELS")
        print("=" * 40)
        
        key_indicators = ['Account Ownership Rate', 'Mobile Money Account Rate']
        
        for indicator in key_indicators:
            print(f"\n📊 Modeling: {indicator}")
            
            # Get indicator data
            indicator_data = self.df[
                (self.df['indicator'] == indicator) & 
                (self.df['gender'] == 'all') &
                (self.df['value_numeric'].notna())
            ].sort_values('year')
            
            if len(indicator_data) < 3:
                print(f"   ❌ Insufficient data for {indicator}")
                continue
                
            # Prepare features
            X = indicator_data[['year']].values
            y = indicator_data['value_numeric'].values
            
            # Add event features
            event_features = np.zeros((len(X), len(self.events_data)))
            for i, row in indicator_data.iterrows():
                year = row['year']
                for j, event in enumerate(self.events_data):
                    # Event impact with decay
                    if year >= event['year']:
                        years_since = year - event['year']
                        if years_since <= event['duration']:
                            # Get impact for this indicator
                            if indicator in self.event_matrix.columns:
                                base_impact = self.event_matrix.loc[event['event'], indicator]
                                # Apply decay
                                decay_factor = max(0, 1 - (years_since / event['duration']))
                                event_features[indicator_data.index.get_loc(i), j] = base_impact * decay_factor
            
            # Combine features
            X_enhanced = np.column_stack([X, event_features])
            
            # Train models
            models = {
                'linear': LinearRegression(),
                'ridge': Ridge(alpha=1.0),
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42)
            }
            
            best_model = None
            best_score = -np.inf
            
            for name, model in models.items():
                try:
                    model.fit(X_enhanced, y)
                    score = model.score(X_enhanced, y)
                    
                    print(f"   • {name.title()}: R² = {score:.3f}")
                    
                    if score > best_score:
                        best_score = score
                        best_model = model
                        
                except Exception as e:
                    print(f"   ❌ {name} failed: {e}")
            
            if best_model is not None:
                self.models[indicator] = {
                    'model': best_model,
                    'score': best_score,
                    'features': X_enhanced,
                    'target': y,
                    'data': indicator_data
                }
                print(f"   ✅ Best model saved (R² = {best_score:.3f})")
            else:
                print(f"   ❌ No successful model for {indicator}")
                
        return self.models
        
    def generate_forecasts(self, forecast_years=[2025, 2026, 2027]):
        """Generate forecasts with uncertainty quantification"""
        
        print(f"\n🔮 GENERATING FORECASTS FOR {forecast_years}")
        print("=" * 50)
        
        for indicator, model_data in self.models.items():
            print(f"\n📈 Forecasting: {indicator}")
            
            model = model_data['model']
            historical_data = model_data['data']
            
            forecasts = []
            uncertainties = []
            
            for year in forecast_years:
                # Prepare features for forecast year
                X_forecast = np.array([[year]])
                
                # Add event features for forecast year
                event_features = np.zeros((1, len(self.events_data)))
                for j, event in enumerate(self.events_data):
                    if year >= event['year']:
                        years_since = year - event['year']
                        if years_since <= event['duration']:
                            if indicator in self.event_matrix.columns:
                                base_impact = self.event_matrix.loc[event['event'], indicator]
                                decay_factor = max(0, 1 - (years_since / event['duration']))
                                event_features[0, j] = base_impact * decay_factor
                
                X_forecast_enhanced = np.column_stack([X_forecast, event_features])
                
                # Generate forecast
                try:
                    forecast = model.predict(X_forecast_enhanced)[0]
                    
                    # Calculate uncertainty (using historical residuals)
                    historical_predictions = model.predict(model_data['features'])
                    residuals = model_data['target'] - historical_predictions
                    std_error = np.std(residuals)
                    
                    # 95% confidence interval
                    confidence_interval = 1.96 * std_error
                    
                    forecasts.append(forecast)
                    uncertainties.append(confidence_interval)
                    
                    print(f"   • {year}: {forecast:.1f}% ± {confidence_interval:.1f}%")
                    
                except Exception as e:
                    print(f"   ❌ Forecast failed for {year}: {e}")
                    forecasts.append(None)
                    uncertainties.append(None)
            
            self.forecasts[indicator] = {
                'years': forecast_years,
                'forecasts': forecasts,
                'uncertainties': uncertainties,
                'confidence_level': 0.95
            }
            
        return self.forecasts
        
    def scenario_analysis(self):
        """Perform scenario analysis with different policy assumptions"""
        
        print("\n🎭 SCENARIO ANALYSIS")
        print("=" * 30)
        
        # Define scenarios
        scenarios = {
            'baseline': {
                'name': 'Baseline (Current Trajectory)',
                'events': [],
                'description': 'No additional policy interventions'
            },
            'accelerated': {
                'name': 'Accelerated Digital Finance',
                'events': [
                    {'year': 2025, 'event': 'Enhanced Digital ID', 'impact': 10, 'type': 'Technology'},
                    {'year': 2026, 'event': 'Rural 5G Expansion', 'impact': 8, 'type': 'Infrastructure'}
                ],
                'description': 'Aggressive digital infrastructure investment'
            },
            'inclusive': {
                'name': 'Inclusive Finance Focus',
                'events': [
                    {'year': 2025, 'event': 'Women Financial Inclusion Program', 'impact': 12, 'type': 'Policy'},
                    {'year': 2026, 'event': 'Rural Agent Network Expansion', 'impact': 6, 'type': 'Infrastructure'}
                ],
                'description': 'Focus on gender and rural inclusion'
            }
        }
        
        scenario_results = {}
        
        for scenario_name, scenario in scenarios.items():
            print(f"\n📊 Scenario: {scenario['name']}")
            print(f"   Description: {scenario['description']}")
            
            scenario_forecasts = {}
            
            for indicator in self.models.keys():
                model_data = self.models[indicator]
                model = model_data['model']
                
                # Calculate scenario impact
                scenario_impact = 0
                for event in scenario['events']:
                    if indicator in self.event_matrix.columns:
                        # Use similar event as proxy for impact
                        similar_events = [e for e in self.event_matrix.index if event['type'].lower() in e.lower()]
                        if similar_events:
                            base_impact = self.event_matrix.loc[similar_events[0], indicator]
                            scenario_impact += base_impact * (event['impact'] / 10)  # Scale by event strength
                
                # Apply scenario impact to baseline forecast
                baseline_forecast = self.forecasts[indicator]['forecasts'][-1]  # 2027 forecast
                scenario_forecast = baseline_forecast + scenario_impact
                
                scenario_forecasts[indicator] = {
                    'baseline': baseline_forecast,
                    'scenario': scenario_forecast,
                    'impact': scenario_impact
                }
                
                print(f"   • {indicator}: {scenario_forecast:.1f}% (+{scenario_impact:.1f}pp)")
            
            scenario_results[scenario_name] = scenario_forecasts
            
        self.scenario_results = scenario_results
        return scenario_results
        
    def create_forecast_tables(self):
        """Create detailed forecast tables with confidence intervals"""
        
        print("\n📋 CREATING FORECAST TABLES")
        print("=" * 35)
        
        # Main forecast table
        forecast_data = []
        
        for indicator, forecast_data_dict in self.forecasts.items():
            for i, year in enumerate(forecast_data_dict['years']):
                forecast = forecast_data_dict['forecasts'][i]
                uncertainty = forecast_data_dict['uncertainties'][i]
                
                if forecast is not None and uncertainty is not None:
                    forecast_data.append({
                        'Indicator': indicator,
                        'Year': year,
                        'Forecast': round(forecast, 1),
                        'Lower_CI': round(forecast - uncertainty, 1),
                        'Upper_CI': round(forecast + uncertainty, 1),
                        'Uncertainty': round(uncertainty, 1)
                    })
        
        forecast_table = pd.DataFrame(forecast_data)
        
        # Scenario comparison table
        scenario_data = []
        
        if hasattr(self, 'scenario_results'):
            for scenario_name, scenario_forecasts in self.scenario_results.items():
                for indicator, forecast_info in scenario_forecasts.items():
                    scenario_data.append({
                        'Scenario': scenario_name,
                        'Indicator': indicator,
                        'Baseline_2027': round(forecast_info['baseline'], 1),
                        'Scenario_2027': round(forecast_info['scenario'], 1),
                        'Impact': round(forecast_info['impact'], 1)
                    })
        
        scenario_table = pd.DataFrame(scenario_data)
        
        # Save tables
        tables_dir = Path('tables')
        tables_dir.mkdir(exist_ok=True)
        
        forecast_table.to_csv(tables_dir / 'forecast_table.csv', index=False)
        scenario_table.to_csv(tables_dir / 'scenario_analysis.csv', index=False)
        
        print(f"💾 Forecast table saved: {tables_dir}/forecast_table.csv")
        print(f"💾 Scenario table saved: {tables_dir}/scenario_analysis.csv")
        
        return forecast_table, scenario_table
        
    def run_complete_modeling(self):
        """Run complete impact modeling pipeline"""
        
        print("🚀 STARTING COMPLETE IMPACT MODELING")
        print("=" * 50)
        
        # Create event-indicator matrix
        self.create_event_indicator_matrix()
        
        # Build regression models
        self.build_regression_models()
        
        # Generate forecasts
        self.generate_forecasts()
        
        # Scenario analysis
        self.scenario_analysis()
        
        # Create forecast tables
        forecast_table, scenario_table = self.create_forecast_tables()
        
        print("\n✅ IMPACT MODELING COMPLETE!")
        print("=" * 40)
        print(f"📊 Models trained: {len(self.models)}")
        print(f"🔮 Forecasts generated: {len(self.forecasts)}")
        print(f"🎭 Scenarios analyzed: {len(self.scenario_results) if hasattr(self, 'scenario_results') else 0}")
        print(f"📋 Tables created: 2")
        
        return {
            'models': self.models,
            'forecasts': self.forecasts,
            'scenarios': self.scenario_results if hasattr(self, 'scenario_results') else {},
            'event_matrix': self.event_matrix,
            'forecast_table': forecast_table,
            'scenario_table': scenario_table
        }

def main():
    """Main execution function"""
    modeler = ImpactModeler()
    results = modeler.run_complete_modeling()
    return results

if __name__ == "__main__":
    main()