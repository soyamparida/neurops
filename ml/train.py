import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("data.csv")

# Features and label
X = data.drop("failed", axis=1)
y = data["failed"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "model.joblib")

print("Model trained and saved as model.joblib")
