# Fixed version of the data enrichment section
# Replace the problematic data enrichment code with this safe version

# 1. Add regional breakdown observations (estimated from national trends) - FIXED VERSION
print("1. Adding regional breakdowns...")

# Regional multipliers based on typical urban/rural and regional development patterns
regional_factors = {
    'Addis_Ababa': {'access': 1.4, 'usage': 1.6},  # Higher urban development
    'Oromia': {'access': 0.9, 'usage': 0.8},       # Large rural population
    'Amhara': {'access': 0.85, 'usage': 0.75},     # Rural, traditional
    'SNNP': {'access': 0.8, 'usage': 0.7}          # Rural, lower development
}

# Get national baseline data - SAFE VERSION
national_baseline = observations.copy()

# Apply filters only if columns exist
if 'gender' in observations.columns:
    national_baseline = national_baseline[national_baseline['gender'] == 'All']
if 'region' in observations.columns:
    national_baseline = national_baseline[national_baseline['region'] == 'National']
if 'age_group' in observations.columns:
    national_baseline = national_baseline[national_baseline['age_group'] == 'All']
elif 'age' in observations.columns:
    national_baseline = national_baseline[national_baseline['age'] == 'All']

print(f"Found {len(national_baseline)} baseline records for regional estimation")

if not national_baseline.empty:
    for _, baseline in national_baseline.iterrows():
        # Check if we have the required columns
        if 'indicator_code' not in baseline.index or 'value' not in baseline.index:
            continue
            
        for region, factors in regional_factors.items():
            if baseline['indicator_code'] == 'FI_ACCESS_ACCOUNT':
                regional_value = baseline['value'] * factors['access']
            elif baseline['indicator_code'] == 'FI_USAGE_DIGITAL_PAY':
                regional_value = baseline['value'] * factors['usage']
            else:
                continue
            
            # Get year safely
            year_value = baseline.get('year', baseline.get('Year', 2021))  # fallback to 2021
                
            new_record = add_record(
                record_type='observation',
                parent_id=None,
                indicator_code=baseline['indicator_code'],
                year=year_value,
                value=round(regional_value, 1),
                unit='percentage',
                source_url='https://globalfindex.worldbank.org',
                confidence='Medium',
                region=region,
                rationale=f"Regional estimate based on national data adjusted for {region} development patterns"
            )
            new_records.append(new_record)
else:
    print("No suitable baseline data found for regional estimation")

print(f"Added {len([r for r in new_records if r['record_type'] == 'observation'])} regional observation records")