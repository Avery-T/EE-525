import pandas as pd
from datetime import datetime, timedelta

# === Configuration ===
input_csv = "SF.csv"       # your input daily summaries file
output_csv = "SF_annual.csv"

# === Load Data ===
df = pd.read_csv(input_csv)

# Typical NOAA Daily Summaries columns include:
# 'STATION', 'NAME', 'DATE', 'TMAX', 'TMIN', 'TAVG'
# Some stations might miss TAVG — we only need TMAX and TMIN here.

# Convert DATE to datetime
df['DATE'] = pd.to_datetime(df['DATE'])

# Sort by date to ensure chronological order
df = df.sort_values('DATE')

# Get metadata
station_id = df['STATION'].iloc[0]
station_name = df['NAME'].iloc[0]
start_date = df['DATE'].iloc[0]
end_date = df['DATE'].iloc[-1]

# === Compute Annual Ranges (Oct 27 → next Oct 26) ===
annual_data = []

# Define custom “year window” starting Oct 27
start_year = start_date.year
end_year = end_date.year

for year in range(start_year, end_year):
    # Define window from Oct 27 of this year to Oct 26 of the next
    window_start = datetime(year, 10, 27)
    window_end = datetime(year + 1, 10, 26)
    
    mask = (df['DATE'] >= window_start) & (df['DATE'] <= window_end)
    subset = df.loc[mask]
    
    if subset.empty:
        continue  # skip years without data
    
    annual_max = subset['TMAX'].max()
    annual_min = subset['TMIN'].min()
    
    annual_data.append({
        "Year_Start": window_start.strftime("%Y-%m-%d"),
        "Year_End": window_end.strftime("%Y-%m-%d"),
        "Annual_Max": annual_max,
        "Annual_Min": annual_min
    })

# === Create Output DataFrame ===
out_df = pd.DataFrame(annual_data)
out_df.insert(0, "STATION", station_id)
out_df.insert(1, "NAME", station_name)
out_df["Data_Range"] = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"

# === Save to CSV ===
out_df.to_csv(output_csv, index=False)

print(f"✅ Annual summary saved to {output_csv}")
print(f"Station: {station_name} ({station_id})")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')}")
