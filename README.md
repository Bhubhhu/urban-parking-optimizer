# 🏙️ Urban Parking Optimization: AI & Swarm Intelligence

A full-stack, AI-powered routing engine that calculates the optimal path to available urban parking spots. This application combines Machine Learning for traffic prediction with an Ant Colony Optimization (ACO) algorithm to navigate real-world city grids dynamically.

## 🚀 The Architecture

This project solves the "last-mile" urban routing problem by evaluating static physical distances against dynamically predicted traffic congestion.

1.  **Data Ingestion Layer:** Uses `OSMnx` to download real-world street networks (Chandigarh, India), extracting GPS coordinates, road lengths, and street names.
2.  **Predictive Layer:** A Scikit-Learn **Random Forest Regressor** anticipates traffic density based on road constraints (speed limits and distances). To ensure near-zero latency, the engine utilizes **vectorized batch-precomputation** to predict the entire city's traffic state instantly.
3.  **Routing Engine:** A biologically-inspired **Ant Colony Optimization (ACO)** swarm navigates the graph. It balances the heuristic (predicted travel cost) against the pheromone trail (historical success) to find the absolute best route to an open parking lot.
4.  **API & Frontend:** A **FastAPI** backend exposes the engine via REST endpoints, consumed by a responsive, dark-mode **Leaflet.js** frontend map.

## 🛠️ Tech Stack

* **Backend:** Python 3, FastAPI, Uvicorn
* **AI/ML:** Scikit-Learn (Random Forest), NetworkX
* **Geospatial:** OSMnx, OpenStreetMap Data
* **Frontend:** HTML5, CSS3 (Glassmorphism UI), JavaScript, Leaflet.js

## 🚦 Installation & Usage

**1. Clone the repository and install dependencies:**
```bash
git clone [https://github.com/YOUR_USERNAME/parking-optimization.git](https://github.com/YOUR_USERNAME/parking-optimization.git)
cd parking-optimization
pip install -r requirements.txt
