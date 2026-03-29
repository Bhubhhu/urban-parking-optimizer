import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

print("1. Loading traffic data...")
df = pd.read_csv("data/traffic_data.csv")

# 2. Prepare Features (X) and Target (y)
# We want to predict 'current_traffic_density' (y) using the road's distance and speed limit (X).
X = df[['distance_meters', 'speed_limit_kmh']]
y = df['current_traffic_density']

# 3. Split the data into Training and Testing sets
# We hold back 20% of the data to test how accurate our model is later.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("2. Training Random Forest Regressor...")
# n_estimators=100 means we are building a "forest" of 100 decision trees.
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate the Model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"3. Model Mean Absolute Error (MAE): {mae:.4f}")
print("   (Note: High/weird error is expected here because our mock dataset is tiny!)")

# 5. Save the trained model to a file
# This is crucial. We don't want to retrain the model every time we run the ACO algorithm.
os.makedirs('models', exist_ok=True)
model_path = 'models/traffic_model.pkl'
joblib.dump(model, model_path)
print(f"\n✅ Model successfully saved to {model_path}")

# 6. Helper Function for Future Predictions
def predict_traffic(distance, speed_limit):
    """
    This function will be called by your Ant Colony Algorithm to predict 
    traffic on roads it hasn't seen yet.
    """
    loaded_model = joblib.load('models/traffic_model.pkl')
    # Format the input to match the dataframe structure the model was trained on
    input_data = pd.DataFrame([[distance, speed_limit]], columns=['distance_meters', 'speed_limit_kmh'])
    prediction = loaded_model.predict(input_data)[0]
    return round(prediction, 2)

# 7. Let's test the prediction function with a made-up road
test_dist = 350
test_speed = 45
predicted_density = predict_traffic(test_dist, test_speed)

print(f"\n--- Prediction Test ---")
print(f"A {test_dist}m road with a {test_speed}km/h speed limit has a predicted traffic density of: {predicted_density}")
