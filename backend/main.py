from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="NeuroOps Decision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
origins = [
    "http://localhost:3000",
    "http://localhost:3001"
]
class InputData(BaseModel):
    cpu_load: float
    memory_usage: float
    error_rate: float
    latency: float

class OutputData(BaseModel):
    failure_probability: float
    decision: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict", response_model=OutputData)
def predict(data: InputData):
    # Example: simple weighted formula for failure probability
    failure_probability = (
        0.3 * data.cpu_load +
        0.3 * data.memory_usage +
        0.2 * data.error_rate +
        0.2 * (data.latency / 1000)  # normalize latency
    )

    decision = "ROLLBACK" if failure_probability >= 0.7 else "PROCEED"

    return {
        "failure_probability": round(failure_probability, 2),
        "decision": decision
    }


