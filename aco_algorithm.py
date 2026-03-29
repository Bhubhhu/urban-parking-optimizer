import networkx as nx
import random
import joblib
import warnings
import matplotlib.pyplot as plt
from environment import city_graph # Imports the real city graph

# Hide annoying ML warnings to keep the terminal clean
warnings.filterwarnings('ignore')

# 1. Load the Machine Learning Model globally so it only loads once
try:
    traffic_model = joblib.load('models/traffic_model.pkl')
except FileNotFoundError:
    print("Error: Could not find the ML model. Did you run train_model.py?")
    exit()

# 2. The Core API Function
def find_best_parking(user_start_node=None):
    # Initialize Pheromones
    for u, v in city_graph.edges():
        city_graph[u][v]['pheromone'] = 1.0

    # ACO Parameters
    NUM_ANTS = 20
    ITERATIONS = 50
    ALPHA = 1.0       
    BETA = 2.0        
    EVAPORATION = 0.3 
    
    # Dynamically pick a random starting intersection (that isn't a parking lot)
    valid_starts = [node for node, data in city_graph.nodes(data=True) if data.get('type') != 'parking']
    if not valid_starts:
        return {"status": "error", "message": "No valid starting intersections found."}
    if user_start_node and user_start_node in valid_starts:
        START_NODE = user_start_node 
    else:
        START_NODE = random.choice(valid_starts)
    print(f"Releasing swarm from intersection ID: {START_NODE}...")
    
    best_overall_path = None
    best_overall_cost = float('inf')

    # --- NEW: MASSIVE SPEED OPTIMIZATION (Batch Pre-computation) ---
    print("Pre-computing ML traffic predictions for all roads...")
    edges_list = list(city_graph.edges(data=True))
    
    # 1. Gather all distances and speed limits into one giant array
    features = [[data.get('distance', 10), data.get('speed_limit', 40)] for u, v, data in edges_list]
    
    # 2. Ask the ML model to predict ALL roads at the exact same time (Lightning fast!)
    if features:
        batch_predictions = traffic_model.predict(features)
    else:
        batch_predictions = []

    # 3. Save the results directly onto the graph edges so the ants can just read them
    for i, (u, v, data) in enumerate(edges_list):
        predicted_traffic = batch_predictions[i]
        dynamic_cost = data.get('distance', 10) * (1 + predicted_traffic)
        
        # Save to the graph
        city_graph[u][v]['dynamic_cost'] = dynamic_cost
        city_graph[u][v]['heuristic'] = 1.0 / dynamic_cost
    # ---------------------------------------------------------------

    # The Main ACO Loop
    for iteration in range(ITERATIONS):
        all_ant_paths = []
        
        # Phase A: Ants explore the city
        for ant in range(NUM_ANTS):
            current_node = START_NODE
            path = [current_node]
            visited = set([current_node]) # Tabu List: memory to prevent infinite loops
            path_cost = 0.0
            
            steps = 0
            max_steps = 100 # Fatigue limit
            
            while steps < max_steps:
                # Did the ant find a parking lot?
		# Did the ant find a parking lot that ACTUALLY has space?
                node_data = city_graph.nodes[current_node]
                if node_data.get('type') == 'parking' and node_data.get('available', 0) > 0:
                    break
                    
                all_neighbors = list(city_graph.successors(current_node))
                unvisited_neighbors = [n for n in all_neighbors if n not in visited]
                
                if not unvisited_neighbors:
                    break # Dead end
                    
                probabilities = []
                valid_moves = []
                
                for next_node in unvisited_neighbors:
                    edge = city_graph[current_node][next_node]
                    
                    # OPTIMIZED: Just read the pre-computed values! No ML needed here.
                    dynamic_cost = edge['dynamic_cost']
                    heuristic = edge['heuristic'] 
                    pheromone = edge['pheromone']
                    
                    move_probability = (pheromone ** ALPHA) * (heuristic ** BETA)
                    
                    probabilities.append(move_probability)
                    valid_moves.append((next_node, dynamic_cost))
                
                if sum(probabilities) == 0:
                    break
                    
                chosen_index = random.choices(range(len(valid_moves)), weights=probabilities)[0]
                chosen_node, chosen_cost = valid_moves[chosen_index]
                
                current_node = chosen_node
                path.append(current_node)
                visited.add(current_node)
                path_cost += chosen_cost
                steps += 1
                
            # Save the successful journeys
	    # Save the successful journeys
            end_node_data = city_graph.nodes[path[-1]]
            if end_node_data.get('type') == 'parking' and end_node_data.get('available', 0) > 0:
                all_ant_paths.append((path, path_cost))
                
            if path_cost < best_overall_cost:
                best_overall_cost = path_cost
                best_overall_path = path

        # Phase B: Evaporation
        for u, v in city_graph.edges():
            city_graph[u][v]['pheromone'] *= (1.0 - EVAPORATION)
            
        # Phase C: Deposit
        for path, cost in all_ant_paths:
            pheromone_to_drop = 1000.0 / cost 
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i+1]
                city_graph[u][v]['pheromone'] += pheromone_to_drop

    # Return the results formatted for an API or local printing
    if best_overall_path:
        route_coordinates = []
        for node in best_overall_path:
            node_data = city_graph.nodes[node]
            if 'y' in node_data and 'x' in node_data:
                route_coordinates.append([node_data['y'], node_data['x']])
                
        return {
            "status": "success",
            "start_node": START_NODE,
            "path_ids": best_overall_path,
            "coordinates": route_coordinates,
            "dynamic_cost": round(best_overall_cost, 2)
        }
    else:
        return {"status": "error", "message": "The swarm failed to find a parking lot."}

# 3. Advanced Visualization Function

import folium

# --- TRULY INTERACTIVE WEB MAP VISUALIZER ---
def create_interactive_web_map(graph, winning_path):
    if not winning_path:
        return

    print("\n3. Generating Interactive Web Map...")
    
    # 1. Extract the GPS coordinates of the winning route
    # OSMnx stores latitude as 'y' and longitude as 'x'
    route_coords = []
    for node in winning_path:
        lat = graph.nodes[node]['y']
        lon = graph.nodes[node]['x']
        route_coords.append((lat, lon))

    # 2. Find the center to focus the camera (we'll center on the start point)
    start_lat, start_lon = route_coords[0]

    # 3. Create the Base Map 
    # 'CartoDB dark_matter' gives it that sleek, modern dark-mode aesthetic
    m = folium.Map(location=[start_lat, start_lon], zoom_start=16, tiles='CartoDB dark_matter')

    # 4. Draw the Glowing Route
    folium.PolyLine(
        locations=route_coords,
        color='#00A3FF', # Apple Maps-style vibrant blue
        weight=7,        # Nice thick line
        opacity=0.8,
        tooltip="Click to see: Optimal ACO Route"
    ).add_to(m)

    # 5. Add a Start Marker
    folium.Marker(
        location=[start_lat, start_lon],
        popup="<b>Start Location</b>",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    # 6. Add a Destination (Parking) Marker
    end_lat, end_lon = route_coords[-1]
    
    # Let's see how many spots are left at this destination
    spots_left = graph.nodes[winning_path[-1]].get('available', 'Unknown')
    
    folium.Marker(
        location=[end_lat, end_lon],
        popup=f"<b>Parking Found!</b><br>Available Spots: {spots_left}",
        icon=folium.Icon(color="red", icon="car", prefix='fa')
    ).add_to(m)

    # 7. Save it as an actual webpage!
    html_filename = "interactive_parking_map.html"
    m.save(html_filename)
    print(f"✅ Success! Open the file '{html_filename}' in your web browser to explore your map.")

# Update the trigger at the bottom of your file to use the new function:
# (Make sure to comment out or delete the old visualize_winning_route call)
if __name__ == "__main__":
    result = find_best_parking()
    if result["status"] == "success":
        # Call our new Folium function
        create_interactive_web_map(city_graph, result['path_ids'])

# 4. Execution Block (Runs only ifyou execute this file directly)
