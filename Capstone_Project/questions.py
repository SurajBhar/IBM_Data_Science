# questions.py
# Load the SpaceX launch data and answer the specified questions
import pandas as pd

# Load the dataset (relative path)
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Question 1: Which site has the largest successful launches?
success_counts = spacex_df[spacex_df['class'] == 1] \
    .groupby('Launch Site') \
    .size()
site_largest_success = success_counts.idxmax()
print(f"1. Site with the largest successful launches: {site_largest_success}")

# Question 2: Which site has the highest launch success rate?
site_summary = spacex_df.groupby('Launch Site').agg(
    total_launches=('class', 'size'),
    successes=('class', 'sum')
)
site_summary['success_rate'] = site_summary['successes'] / site_summary['total_launches']
site_highest_rate = site_summary['success_rate'].idxmax()
print(f"2. Site with the highest launch success rate: {site_highest_rate}")

# Question 3 & 4: Payload range(s) with highest/lowest launch success rate
# Define payload bins (kg)
bins = [0, 2500, 5000, 7500, 10000]
labels = ['0-2500', '2500-5000', '5000-7500', '7500-10000']
spacex_df['payload_range'] = pd.cut(spacex_df['Payload Mass (kg)'], bins=bins, labels=labels, include_lowest=True)

# Compute success rates by payload range
payload_summary = spacex_df.groupby('payload_range').agg(
    total=('class', 'size'),
    successes=('class', 'sum')
)
payload_summary['success_rate'] = payload_summary['successes'] / payload_summary['total']
highest_rate = payload_summary['success_rate'].max()
lowest_rate = payload_summary['success_rate'].min()
highest_ranges = payload_summary[payload_summary['success_rate'] == highest_rate].index.tolist()
lowest_ranges = payload_summary[payload_summary['success_rate'] == lowest_rate].index.tolist()
print(f"3. Payload range(s) with the highest launch success rate: {highest_ranges}")
print(f"4. Payload range(s) with the lowest launch success rate: {lowest_ranges}")

# Question 5: Which F9 Booster version has the highest launch success rate?
booster_summary = spacex_df.groupby('Booster Version Category').agg(
    total=('class', 'size'),
    successes=('class', 'sum')
)
booster_summary['success_rate'] = booster_summary['successes'] / booster_summary['total']
best_booster = booster_summary['success_rate'].idxmax()
print(f"5. F9 Booster version with the highest launch success rate: {best_booster}")
