import pandas as pd
import random
import os

# Create a 'data' directory if it doesn't exist
os.makedirs('data', exist_ok=True)

def generate_traffic_data():
    # Let's build a slightly larger city grid: A, B, C, D, E, F
    roads = [
        {'start': 'A', 'end': 'B', 'dist': 400, 'speed': 40},
        {'start': 'B', 'end': 'C', 'dist': 300, 'speed': 50},
        {'start': 'A', 'end': 'D', 'dist': 500, 'speed': 40},
        {'start': 'D', 'end': 'E', 'dist': 450, 'speed': 50},
        {'start': 'B', 'end': 'E', 'dist': 350, 'speed': 30},
        {'start': 'E', 'end': 'F', 'dist': 200, 'speed': 30},
        {'start': 'C', 'end': 'Parking_1', 'dist': 100, 'speed': 20},
        {'start': 'F', 'end': 'Parking_2', 'dist': 150, 'speed': 20},
        {'start': 'E', 'end': 'Parking_3', 'dist': 50,  'speed': 15}
    ]

    data = []
    for road in roads:
        # Simulate current traffic density (0.0 is empty, 1.0 is bumper-to-bumper)
        # We use random.uniform to generate realistic decimal values
        traffic_density = round(random.uniform(0.1, 0.9), 2)
        
        data.append({
            'start_node': road['start'],
            'end_node': road['end'],
            'distance_meters': road['dist'],
            'speed_limit_kmh': road['speed'],
            'current_traffic_density': traffic_density
        })

    df = pd.DataFrame(data)
    filepath = 'data/traffic_data.csv'
    df.to_csv(filepath, index=False)
    print(f"✅ Traffic data saved to {filepath}")

def generate_parking_data():
    parking_lots = [
        {'id': 'Parking_1', 'capacity': 100},
        {'id': 'Parking_2', 'capacity': 50},
        {'id': 'Parking_3', 'capacity': 200}
    ]

    data = []
    for lot in parking_lots:
        # Simulate how many spots are currently available
        available = random.randint(0, lot['capacity'])
        
        data.append({
            'node_id': lot['id'],
            'total_capacity': lot['capacity'],
            'currently_available': available
        })

    df = pd.DataFrame(data)
    filepath = 'data/parking_data.csv'
    df.to_csv(filepath, index=False)
    print(f"✅ Parking data saved to {filepath}")

# Run the functions
if __name__ == "__main__":
    print("Generating mock dataset...")
    generate_traffic_data()
    generate_parking_data()
    print("Done! You can now use these CSVs in environment.py")
