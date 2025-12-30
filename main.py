from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NeuroOps Decision API")

class InputData(BaseModel):
    failure_probability: float

class OutputData(BaseModel):
    failure_probability: float
    decision: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict", response_model=OutputData)
def predict(data: InputData):
    if data.failure_probability >= 0.7:
        decision = "ROLLBACK"
    else:
        decision = "PROCEED"

    return {
        "failure_probability": data.failure_probability,
        "decision": decision
    }


