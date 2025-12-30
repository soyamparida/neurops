import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = pd.DataFrame({
    "feature1": [0.1, 0.5, 0.8, 0.3, 0.9, 0.2],
    "feature2": [1, 0, 1, 0, 1, 0],
    "target": [0, 1, 1, 0, 1, 0]
})

X = data[["feature1", "feature2"]]
y = data["target"]

model = RandomForestClassifier()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("ML model trained and saved as model.pkl")
