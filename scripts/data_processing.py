import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from math import radians, cos, sin, acos

# Load data
data = {
    'id': [1, 2, 3, 4],
    'event': ['SOSP', 'EOSP', 'SOSP', 'EOSP'],
    'dateStamp': [43831, 43831, 43832, 43832],
    'timeStamp': [0.708333, 0.791667, 0.333333, 0.583333],
    'voyage_From': ['Port A', 'Port A', 'Port B', 'Port B'],
    'lat': [34.0522, 34.0522, 36.7783, 36.7783],
    'lon': [-118.2437, -118.2437, -119.4179, -119.4179],
    'imo_num': ['9434761', '9434761', '9434761', '9434761'],
    'voyage_Id': ['6', '6', '6', '6'],
    'allocatedVoyageId': [None, None, None, None]
}

df = pd.DataFrame(data)

# Calculate event_time
df['event_time'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(df['dateStamp'], unit='D') + pd.to_timedelta(df['timeStamp'] * 24, unit='H')

# Calculate previous event time and coordinates
df['prev_event_time'] = df['event_time'].shift(1)
df['prev_lat'] = df['lat'].shift(1)
df['prev_lon'] = df['lon'].shift(1)

# Calculate time difference in hours
df['time_diff_hours'] = (df['event_time'] - df['prev_event_time']).dt.total_seconds() / 3600.0

# Function to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 3959  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return R * acos(cos(lat1) * cos(lat2) * cos(lon2 - lon1) + sin(lat1) * sin(lat2))

# Calculate distance travelled
df['distance_travelled'] = df.apply(
    lambda row: haversine(row['lat'], row['lon'], row['prev_lat'], row['prev_lon']) if pd.notnull(row['prev_lat']) else 0,
    axis=1
)

# Calculate sailing time and port stay duration
df['sailing_time'] = np.where(df['event'] == 'SOSP', df['time_diff_hours'], np.nan)
df['port_stay_duration'] = np.where(df['event'] == 'EOSP', df['time_diff_hours'], np.nan)

df.to_csv('data/voyages_processed.csv', index=False)
print(df[['id', 'event', 'event_time', 'voyage_From', 'lat', 'lon', 'imo_num', 'voyage_Id', 'prev_event_time', 'time_diff_hours', 'distance_travelled', 'sailing_time', 'port_stay_duration']])
