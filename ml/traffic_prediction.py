import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import joblib

# Generate synthetic traffic data
np.random.seed(42)
hours = np.arange(0, 24, 0.5)
base_traffic = 100 + 50 * np.sin(2 * np.pi * hours / 24) + 30 * np.sin(4 * np.pi * hours / 24)
noise = np.random.normal(0, 10, len(hours))
traffic = base_traffic + noise

# Create features (hour, day_of_week, etc.)
features = np.column_stack([
    hours,
    np.sin(2 * np.pi * hours / 24),
    np.cos(2 * np.pi * hours / 24),
    np.sin(2 * np.pi * hours / (24 * 7)),
    np.cos(2 * np.pi * hours / (24 * 7))
])

# Polynomial features for better fitting
poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(features)

# Train model
traffic_model = LinearRegression()
traffic_model.fit(X_poly, traffic)

# Save model and transformer
joblib.dump(traffic_model, "traffic_model.joblib")
joblib.dump(poly_features, "poly_features.joblib")

print("Traffic prediction model trained and saved")
print(f"Model R² score: {traffic_model.score(X_poly, traffic):.3f}")