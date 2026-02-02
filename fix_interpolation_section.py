# Fixed version of the interpolation section
# Replace the problematic interpolation code with this safe version

# 4. Add intermediate year estimates for trend analysis - FIXED VERSION
print("\n4. Adding intermediate year estimates...")

# Find the year column
year_col = None
possible_year_cols = ['year', 'Year', 'YEAR', 'date', 'Date', 'time_period']
for col in possible_year_cols:
    if col in observations.columns:
        year_col = col
        break

if year_col and 'indicator_code' in observations.columns and 'value' in observations.columns:
    # Linear interpolation for missing years between 2017 and 2021
    for indicator in ['FI_ACCESS_ACCOUNT', 'FI_USAGE_DIGITAL_PAY']:
        # Check if we have gender column, otherwise just use 'All'
        if 'gender' in observations.columns:
            gender_values = ['All', 'Male', 'Female']
        else:
            gender_values = ['All']
            
        for gender in gender_values:
            # Build filter conditions based on available columns
            filter_conditions = [
                observations['indicator_code'] == indicator,
                observations[year_col].isin([2017, 2021])
            ]
            
            # Add gender filter if column exists
            if 'gender' in observations.columns:
                filter_conditions.append(observations['gender'] == gender)
            
            # Add region filter if column exists
            if 'region' in observations.columns:
                filter_conditions.append(observations['region'] == 'National')
            
            # Add age filter if column exists
            if 'age_group' in observations.columns:
                filter_conditions.append(observations['age_group'] == 'All')
            elif 'age' in observations.columns:
                filter_conditions.append(observations['age'] == 'All')
            
            # Combine all conditions
            combined_filter = filter_conditions[0]
            for condition in filter_conditions[1:]:
                combined_filter = combined_filter & condition
            
            # Get data for both years
            data_points = observations[combined_filter]
            
            if len(data_points) >= 2:
                # Get 2017 and 2021 values
                data_2017 = data_points[data_points[year_col] == 2017]
                data_2021 = data_points[data_points[year_col] == 2021]
                
                if not data_2017.empty and not data_2021.empty:
                    value_2017 = data_2017.iloc[0]['value']
                    value_2021 = data_2021.iloc[0]['value']
                    
                    # Interpolate for 2018, 2019, 2020
                    for year in [2018, 2019, 2020]:
                        # Linear interpolation
                        progress = (year - 2017) / (2021 - 2017)
                        interpolated_value = value_2017 + (value_2021 - value_2017) * progress
                        
                        new_record = add_record(
                            record_type='observation',
                            parent_id=None,
                            indicator_code=indicator,
                            year=year,
                            value=round(interpolated_value, 1),
                            unit='percentage',
                            source_url='https://globalfindex.worldbank.org',
                            confidence='Low',
                            gender=gender if 'gender' in observations.columns else 'All',
                            rationale=f"Linear interpolation between 2017 and 2021 Global Findex data points"
                        )
                        new_records.append(new_record)

    interpolated_count = len([r for r in new_records if r['record_type'] == 'observation' and r['confidence'] == 'Low'])
    print(f"Added {interpolated_count} interpolated observation records")
else:
    print("Cannot perform interpolation - missing required columns (year, indicator_code, value)")
    print(f"Available columns: {list(observations.columns)}")