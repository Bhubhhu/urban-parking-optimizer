import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

def create_micro_map():
    # 1. Define your center point and radius
    # Latitude and Longitude for a busy intersection in San Francisco
    center_point = (37.7879, -122.3988) 
    radius_meters = 500 # A 500m radius creates a highly manageable 1km-wide micro-map

    print("Downloading street network from OpenStreetMap...")
    
    # 2. Fetch the graph
    # network_type='drive' ensures we exclude pedestrian walking paths and bike lanes
    G = ox.graph_from_point(center_point, dist=radius_meters, network_type='drive')
    
    print(f"Success! Map downloaded.")
    print(f"Total Intersections (Nodes): {len(G.nodes)}")
    print(f"Total Road Segments (Edges): {len(G.edges)}")

    # 3. Convert to GeoDataFrames (Crucial for your ML step later)
    # This converts the graph into a tabular format so you can merge your CSV traffic data into it
    nodes, edges = ox.graph_to_gdfs(G)
    
    print("\n--- Snippet of Road Data ---")
    # Displaying the street name and length in meters
    print(edges[['name', 'length']].head(5))

    # 4. Visualize the map
    print("\nGenerating visualization...")
    # Plotting with a dark background to easily see the structure
    fig, ax = ox.plot_graph(
        G, 
        node_size=15, 
        node_color='cyan', 
        edge_color='gray', 
        edge_linewidth=1.5,
        bgcolor='black'
    )
    
    return G, nodes, edges

if __name__ == "__main__":
    # Run the function
    city_graph, city_nodes, city_edges = create_micro_map()
