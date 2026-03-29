import networkx as nx
import pandas as pd

# 1. Load the data directly from the CSV files
try:
    traffic_df = pd.read_csv("data/traffic_data.csv")
    parking_df = pd.read_csv("data/parking_data.csv")
    node_df = pd.read_csv("data/node_data.csv") # NEW: Load the GPS coordinates
    print("Successfully loaded datasets.")
except FileNotFoundError:
    print("Error: Could not find the CSV files.")
    exit()

# 2. Initialize the Graph
city_graph = nx.DiGraph()

# 3. NEW: Populate Nodes with their GPS Coordinates FIRST
for index, row in node_df.iterrows():
    city_graph.add_node(row['node_id'], x=row['x'], y=row['y'],name=row.get('name',f"Node {row['node_id']}"))

# 4. Populate Edges (Roads)
for index, row in traffic_df.iterrows():
    city_graph.add_edge(
        row['start_node'], 
        row['end_node'], 
        distance=row['distance_meters'],
        speed_limit=row['speed_limit_kmh'],
        traffic_density=row['current_traffic_density']
    )

# 5. Populate Parking Lot Attributes
for index, row in parking_df.iterrows():
    city_graph.add_node(
        row['node_id'], 
        type='parking',
        capacity=row['total_capacity'],
        available=row['currently_available']
    )

print(f"Total Intersections/Nodes: {city_graph.number_of_nodes()}")
print(f"Total Roads/Edges: {city_graph.number_of_edges()}")
