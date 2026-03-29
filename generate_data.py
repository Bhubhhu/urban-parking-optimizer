import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_parking_data():
    print("Generating synthetic parking data for our SF micro-map...")
    
    # Street names pulled directly from your extract_map.py output!
    streets = ['Harrison Street', 'Essex Street', 'Folsom Street']
    
    # Create a time range for a single week (data recorded every 15 mins)
    start_time = datetime(2023, 10, 1, 0, 0)
    times = [start_time + timedelta(minutes=15*i) for i in range(7 * 24 * 4)] 
    
    data = []
    
    for street in streets:
        # Assign a random total parking capacity for this street segment
        total_spaces = np.random.randint(20, 50)
        
        for t in times:
            hour = t.hour
            
            # Simulate "Rush Hour" (High occupancy at 8-10 AM and 4-6 PM)
            if (8 <= hour <= 10) or (16 <= hour <= 18):
                base_occupancy = 0.85 # 85% full
            elif (11 <= hour <= 15):
                base_occupancy = 0.60 # 60% full
            else:
                base_occupancy = 0.20 # 20% full overnight
                
            # Add some mathematical noise so it looks like real-world data
            noise = np.random.uniform(-0.1, 0.15)
            occupancy_rate = min(max(base_occupancy + noise, 0), 1)
            occupied_spaces = int(total_spaces * occupancy_rate)
            
            data.append({
                'STREET_NAME': street,
                'DATE': t.strftime('%Y-%m-%d'),
                'TIME': t.strftime('%H:%M:%S'),
                'TOTAL_SPACES': total_spaces,
                'OCCUPIED_SPACES': occupied_spaces
            })
            
    df = pd.DataFrame(data)
    df.to_csv('synthetic_sfpark_data.csv', index=False)
    print(f"Success! Generated {len(df)} rows of data and saved to 'synthetic_sfpark_data.csv'")

if __name__ == "__main__":
    generate_synthetic_parking_data()
