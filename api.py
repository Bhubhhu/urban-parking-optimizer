from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aco_algorithm import find_best_parking, city_graph

# Initialize the API
app = FastAPI(title="Smart Parking API")

# Enable CORS so our HTML frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real production app, you'd lock this down to your website domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is online."}

# NEW: Endpoint to get a list of valid starting intersections for the frontend dropdown
@app.get("/api/v1/intersections")
def get_intersections():
    valid_starts = []
    
    # 1. Grab all valid starting points
    all_nodes = [(node, data) for node, data in city_graph.nodes(data=True) if data.get('type') != 'parking']
    
    # 2. STRICT FILTER: Only keep nodes that have a real street name!
    named_nodes = [(node, data) for node, data in all_nodes if "Unnamed" not in data.get('name', 'Unnamed')]
    
    import random
    
    # 3. Sample 20 nodes ONLY from the named_nodes list. 
    # (If there are fewer than 20 named nodes, just grab whatever is available)
    if len(named_nodes) >= 20:
        sample_nodes = random.sample(named_nodes, 20)
    elif len(named_nodes) > 0:
        sample_nodes = named_nodes
    else:
        # Absolute fallback just in case the map has no names at all
        sample_nodes = random.sample(all_nodes, min(20, len(all_nodes)))
    
    for node, data in sample_nodes:
        valid_starts.append({
            "id": node, 
            "name": data.get('name') 
        })
        
    # Sort them alphabetically
    valid_starts = sorted(valid_starts, key=lambda x: x['name'])
    
    return {"intersections": valid_starts}


# UPDATED: Endpoint now accepts an optional 'start_node' parameter
@app.get("/api/v1/get-route")
def get_optimal_route(start_node: float = None):
    print(f"Received routing request. Start Node: {start_node}")
    
    # We pass the start_node to our algorithm (we'll update that next!)
    result = find_best_parking(start_node)
    return result
