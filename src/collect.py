import pandas as pd
import numpy as np

PORT_HEDLAND_LAT = -20.3
PORT_HEDLAND_LON = 118.6

def load_and_filter_cyclones(filepath, max_dist_km=500):
    df = pd.read_csv(filepath, skiprows=[1], low_memory=False)

    # keep only relevant columns — adjust names based on what you saw in 2b
    cols = ['SID', 'NAME', 'ISO_TIME', 'LAT', 'LON', 'USA_WIND', 'USA_PRES']
    df = df[cols].copy()

    # convert types
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
    df['USA_WIND'] = pd.to_numeric(df['USA_WIND'], errors='coerce')
    df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'], errors='coerce')

    df = df.dropna(subset=['LAT', 'LON', 'ISO_TIME'])

    # approximate distance in km (good enough at this latitude)
    df['dist_km'] = np.sqrt(
        (df['LAT'] - PORT_HEDLAND_LAT)**2 +
        (df['LON'] - PORT_HEDLAND_LON)**2
    ) * 111

    pilbara = df[df['dist_km'] <= max_dist_km].copy()
    return pilbara

if __name__ == "__main__":
    pilbara_cyclones = load_and_filter_cyclones(
        '/Users/kdpaa/Documents/Pilbara/pilbara-disruption-forecaster/data/raw/ibtracs_southern_hemisphere.csv'
    )
    print(f"Found {pilbara_cyclones['SID'].nunique()} unique storms near Pilbara")
    pilbara_cyclones.to_csv('/Users/kdpaa/Documents/Pilbara/pilbara-disruption-forecaster/data/processed/pilbara_cyclones.csv', index=False)


