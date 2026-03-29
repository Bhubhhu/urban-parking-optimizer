# Urban Parking Optimization using Ant Colony Optimization & Machine Learning

An intelligent, hybrid routing system that combines predictive Machine Learning with biologically inspired optimization to find the most efficient route to available urban parking spots in dynamic traffic conditions.

## 🚀 Overview

Traditional routing algorithms (like Dijkstra's or A*) often rely on static distances or purely reactive traffic data. This project introduces a more sophisticated approach by anticipating traffic conditions before they happen. 

By layering a **Random Forest Regressor** over an **Ant Colony Optimization (ACO)** algorithm, this system simulates virtual "ants" that query an ML model to predict traffic density on upcoming roads. The swarm then mathematically converges on the optimal path that balances physical distance, predicted congestion, and final parking availability.

## 🧠 Architecture

This project is divided into a three-layer pipeline:

1. **The Physical Layer (Environment):** Models the city grid as a mathematical Directed Graph using `NetworkX`. 
2. **The Intelligence Layer (Machine Learning):** A Scikit-Learn Random Forest Regressor trained on historical traffic data to predict future congestion based on road characteristics.
3. **The Routing Layer (Optimization):** An ACO algorithm where the heuristic ($\eta$) is driven by the ML model's traffic predictions, and the pheromone trail ($\tau$) reinforces the fastest successful routes to open parking.

## 📁 Project Structure

* `generate_mock_data.py`: Synthesizes realistic traffic and parking datasets to simulate a dynamic city grid.
* `environment.py`: Translates the CSV data into a functional `NetworkX` graph environment.
* `train_model.py`: Trains the Random Forest Regressor on the traffic data and exports the predictive model.
* `aco_algorithm.py`: The core optimization engine. Runs the ant simulation, queries the ML model, and visualizes the winning route.
* `/data`: Directory containing the generated `traffic_data.csv` and `parking_data.csv`.
* `/models`: Directory containing the exported `traffic_model.pkl` "brain".

## 🛠️ Prerequisites & Installation

Ensure you have Python 3.x installed. Install the required dependencies using pip:

```bash
pip install pandas networkx scikit-learn matplotlib joblib
