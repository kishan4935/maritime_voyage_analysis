import pandas as pd
import matplotlib.pyplot as plt

# Load processed data
df = pd.read_csv('data/voyages_processed.csv')

# Filter out rows with NaN values in sailing_time or port_stay_duration for plotting
df_sailing = df.dropna(subset=['sailing_time'])
df_port = df.dropna(subset=['port_stay_duration'])

plt.figure(figsize=(12, 6))

# Plot sailing times
plt.bar(df_sailing['event_time'], df_sailing['sailing_time'], width=0.1, label='Sailing Time (hours)')

# Plot port stay durations
plt.bar(df_port['event_time'], df_port['port_stay_duration'], width=0.1, label='Port Stay Duration (hours)', color='orange')

plt.xlabel('Event Time')
plt.ylabel('Duration (hours)')
plt.title('Voyage Timeline')
plt.legend()
plt.show()
