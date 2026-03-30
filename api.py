import math # <-- NEW IMPORT for distance calculations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from aco_algorithm import find_best_parking, city_graph

app = FastAPI(title="Smart Parking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/api/v1/intersections")
def get_intersections():
    valid_starts = []
    all_nodes = [(node, data) for node, data in city_graph.nodes(data=True) if data.get('type') != 'parking']
    named_nodes = [(node, data) for node, data in all_nodes if "Unnamed" not in data.get('name', 'Unnamed')]
    
    import random
    if len(named_nodes) >= 20:
        sample_nodes = random.sample(named_nodes, 20)
    elif len(named_nodes) > 0:
        sample_nodes = named_nodes
    else:
        sample_nodes = random.sample(all_nodes, min(20, len(all_nodes)))
    
    for node, data in sample_nodes:
        valid_starts.append({"id": node, "name": data.get('name')})
        
    valid_starts = sorted(valid_starts, key=lambda x: x['name'])
    return {"intersections": valid_starts}

# --- NEW SNAP-TO-ROAD FUNCTION ---
def find_nearest_node(lat, lon):
    best_node = None
    min_dist = float('inf')
    
    for node, data in city_graph.nodes(data=True):
        # Don't let users start inside a parking lot
        if data.get('type') == 'parking':
            continue
            
        # Euclidean distance to find the closest road intersection
        dist = math.sqrt((data['y'] - lat)**2 + (data['x'] - lon)**2)
        
        if dist < min_dist:
            min_dist = dist
            best_node = node
            
    return best_node

# --- UPDATED ROUTING ENDPOINT ---
# It now accepts an exact node ID, OR a raw lat/lon click from the map
@app.get("/api/v1/get-route")
def get_optimal_route(start_node: float = None, lat: float = None, lon: float = None):
    
    # 1. Snap to the nearest physical road so the AI can run
    if lat is not None and lon is not None:
        start_node = find_nearest_node(lat, lon)
        
    # 2. Run the AI from that road
    result = find_best_parking(start_node)
    
    # 3. THE FIX: Inject the exact click into the very beginning of the driving route
    if lat is not None and lon is not None and result.get("status") == "success":
        # This makes the blue line start exactly where the user clicked
        result['coordinates'].insert(0, [lat, lon])
        
    return result
