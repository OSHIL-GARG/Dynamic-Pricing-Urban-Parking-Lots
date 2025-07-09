
# Dynamic Pricing for Urban Parking Lots

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants
BASE_PRICE = 10.0
ALPHA_LINEAR = 0.5  # Linear model coefficient
LAMBDA_DEMAND = 0.5  # Demand impact coefficient
VEHICLE_WEIGHTS = {'car': 1.0, 'bike': 0.7, 'truck': 1.5}
TRAFFIC_LEVELS = {'low': 1, 'medium': 2, 'high': 3}

# Load data
df = pd.read_csv("dataset.csv")

# Preprocessing
df['OccupancyRate'] = df['Occupancy'] / df['Capacity']
df['VehicleWeight'] = df['VehicleType'].map(VEHICLE_WEIGHTS)
df['TrafficLevel'] = df['TrafficConditionNearby'].map(TRAFFIC_LEVELS)
df['Timestamp'] = pd.to_datetime(df['LastUpdatedDate'] + ' ' + df['LastUpdatedTime'], format='%d-%m-%Y %H:%M:%S')
df.sort_values(by=['SystemCodeNumber', 'Timestamp'], inplace=True)

# Linear Pricing Model
def linear_model(prev_price, occupancy_rate):
    return prev_price + ALPHA_LINEAR * occupancy_rate

# Demand Calculation
def calculate_demand(row):
    return (
        0.3 * row['OccupancyRate'] +
        0.2 * row['QueueLength'] -
        0.2 * row['TrafficLevel'] +
        0.15 * row['IsSpecialDay'] +
        0.15 * row['VehicleWeight']
    )

# Demand-Based Pricing Model
def demand_based_price(demand):
    norm_demand = min(max(demand, 0), 1)
    return np.clip(BASE_PRICE * (1 + LAMBDA_DEMAND * norm_demand), 5, 20)

# Simulation function for a single lot
def simulate_lot(df, lot_id):
    lot_df = df[df['SystemCodeNumber'] == lot_id].copy()
    lot_df['Price_Model1'] = BASE_PRICE
    lot_df['Price_Model2'] = BASE_PRICE

    for i in range(1, len(lot_df)):
        prev_price_1 = lot_df.iloc[i - 1]['Price_Model1']
        occ_rate = lot_df.iloc[i]['OccupancyRate']
        lot_df.at[lot_df.index[i], 'Price_Model1'] = linear_model(prev_price_1, occ_rate)

        demand = calculate_demand(lot_df.iloc[i])
        lot_df.at[lot_df.index[i], 'Price_Model2'] = demand_based_price(demand)

    return lot_df

# Run simulation for all lots
all_lots = df['SystemCodeNumber'].unique()
all_results = []

for lot_id in all_lots:
    lot_result = simulate_lot(df, lot_id)
    all_results.append(lot_result)

final_df = pd.concat(all_results)

# Plot price trends for one example lot
example_lot = all_lots[0]
example_df = final_df[final_df['SystemCodeNumber'] == example_lot]

plt.figure(figsize=(12, 6))
plt.plot(example_df['Timestamp'], example_df['Price_Model1'], label='Model 1: Linear', marker='o')
plt.plot(example_df['Timestamp'], example_df['Price_Model2'], label='Model 2: Demand-Based', marker='x')
plt.title(f'Dynamic Pricing for Parking Lot {example_lot}')
plt.xlabel('Timestamp')
plt.ylabel('Price ($)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
