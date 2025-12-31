import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Generate synthetic anomaly detection data
np.random.seed(42)
normal_data = np.random.normal(0, 1, (1000, 4))
anomaly_data = np.random.normal(3, 2, (50, 4))
data = np.vstack([normal_data, anomaly_data])

# Create labels (1 for normal, -1 for anomaly)
labels = np.hstack([np.ones(1000), -np.ones(50)])

# Scale the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Train Isolation Forest
anomaly_model = IsolationForest(contamination=0.05, random_state=42)
anomaly_model.fit(data_scaled)

# Save model and scaler
joblib.dump(anomaly_model, "anomaly_model.joblib")
joblib.dump(scaler, "scaler.joblib")

print("Anomaly detection model trained and saved")
print(f"Model accuracy: {np.mean(anomaly_model.predict(data_scaled) == labels):.2f}")