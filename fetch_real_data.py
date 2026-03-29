import osmnx as ox
import pandas as pd
import random
import os

# Create the data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# 1. Download the Real Street Network
place_name = "Sector 17, Chandigarh, India"
print(f"Downloading street network for {place_name}...")

# network_type='drive' ensures we only get roads cars can actually drive on
G = ox.graph_from_place(place_name, network_type='drive')
print(f"Successfully downloaded {G.number_of_nodes()} intersections and {G.number_of_edges()} roads.")

# --- 2. Extract Street Names for Intersections ---
print("Extracting street names for user-friendly labels...")
node_street_names = {node: set() for node in G.nodes()}

# Look at every road and assign its name to the intersections it connects
for u, v, key, data in G.edges(keys=True, data=True):
    if 'name' in data:
        street_name = data['name']
        if isinstance(street_name, list): 
            street_name = street_name[0] # Take the first name if multiple exist
        node_street_names[u].add(street_name)
        node_street_names[v].add(street_name)

# --- 3. Save the Nodes (with GPS and Friendly Names) ---
node_data = []
for node, data in G.nodes(data=True):
    streets = list(node_street_names[node])
    
    # Create a clean name like "Main St & 1st Ave"
    if len(streets) > 1:
        friendly_name = f"{streets[0]} & {streets[1]}"
    elif len(streets) == 1:
        friendly_name = streets[0]
    else:
        friendly_name = f"Unnamed Street (ID: {str(node)[-4:]})" # Fallback

    node_data.append({
        'node_id': node,
        'x': data['x'], # Longitude
        'y': data['y'], # Latitude
        'name': friendly_name # The new user-friendly name
    })

pd.DataFrame(node_data).to_csv('data/node_data.csv', index=False)
print("✅ Node data (with GPS and names) saved to data/node_data.csv")

# --- 4. Extract Road Data (Edges) ---
traffic_data = []
for u, v, key, data in G.edges(keys=True, data=True):
    # OSMnx provides distance in meters under the 'length' key
    distance = round(data.get('length', 0), 2)
    
    # Speed limits can be messy in real data
    speed_limit = data.get('maxspeed', 40) 
    if isinstance(speed_limit, list):
        speed_limit = speed_limit[0] 
    try:
        speed_limit = float(speed_limit)
    except ValueError:
        speed_limit = 40.0 # Default fallback
        
    # Simulate live traffic density
    traffic_density = round(random.uniform(0.1, 0.95), 2)
    
    traffic_data.append({
        'start_node': u,
        'end_node': v,
        'distance_meters': distance,
        'speed_limit_kmh': speed_limit,
        'current_traffic_density': traffic_density
    })

pd.DataFrame(traffic_data).to_csv('data/traffic_data.csv', index=False)
print("✅ Real road network saved to data/traffic_data.csv")

# --- 5. Designate Parking Lots ---
# Randomly select 10 intersections to act as parking garages
parking_nodes = random.sample(list(G.nodes()), 10)
parking_data = []

for node_id in parking_nodes:
    capacity = random.choice([50, 100, 200, 500])
    # Simulate available spots
    available = random.randint(0, capacity)
    
    parking_data.append({
        'node_id': node_id,
        'total_capacity': capacity,
        'currently_available': available
    })

pd.DataFrame(parking_data).to_csv('data/parking_data.csv', index=False)
print("✅ Parking locations saved to data/parking_data.csv")
