from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI(title="NeuroOps ML API")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

class InputData(BaseModel):
    feature1: float
    feature2: float

class OutputData(BaseModel):
    prediction: int
    decision: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict", response_model=OutputData)
def predict(data: InputData):
    X_input = np.array([[data.feature1, data.feature2]])
    pred = model.predict(X_input)[0]
    decision = "ROLLBACK" if pred == 1 else "PROCEED"
    return {"prediction": int(pred), "decision": decision}

