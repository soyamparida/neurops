from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import joblib
import numpy as np
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
from database import SessionLocal, Prediction, SystemMetrics, Alert
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import psutil
import threading


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    message: str
    severity: str
    resolved: bool
    timestamp: datetime

class MetricsResponse(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: float
    timestamp: datetime

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# System metrics collection
def collect_system_metrics():
    while True:
        db = SessionLocal()
        try:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            network = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            
            metrics = SystemMetrics(
                cpu_usage=cpu,
                memory_usage=memory,
                disk_usage=disk,
                network_io=network
            )
            db.add(metrics)
            db.commit()
            
            if cpu > 80 or memory > 80:
                alert = Alert(
                    alert_type="HIGH_RESOURCE_USAGE",
                    message=f"High resource usage detected: CPU {cpu}%, Memory {memory}%",
                    severity="HIGH"
                )
                db.add(alert)
                db.commit()
                
        except Exception as e:
            print(f"Error collecting metrics: {e}")
        finally:
            db.close()
        time.sleep(30)

# Start metrics collection in background
metrics_thread = threading.Thread(target=collect_system_metrics, daemon=True)
metrics_thread.start()

# Prometheus metrics
prediction_counter = Counter('predictions_total', 'Total predictions made')
rollback_counter = Counter('rollbacks_total', 'Total rollback decisions')
prediction_duration = Histogram('prediction_duration_seconds', 'Time spent on predictions')

app = FastAPI(title="NeuroOps Decision API")

# Load ML model
model_path = "../ml/model.joblib"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print("Warning: ML model not found, using fallback logic")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class InputData(BaseModel):
    cpu_load: float
    memory_usage: float
    error_rate: float
    latency: float

class OutputData(BaseModel):
    failure_probability: float
    decision: str

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict", response_model=OutputData)
def predict(data: InputData, db: Session = Depends(get_db)):
    start_time = time.time()
    
    if model is not None:
        features = np.array([[data.cpu_load * 100, data.memory_usage * 100, data.error_rate, data.latency]])
        failure_probability = model.predict_proba(features)[0][1]
    else:
        failure_probability = (
            0.3 * data.cpu_load +
            0.3 * data.memory_usage +
            0.2 * data.error_rate +
            0.2 * (data.latency / 1000)
        )

    decision = "ROLLBACK" if failure_probability >= 0.7 else "PROCEED"
    
    # Save prediction to database
    prediction = Prediction(
        cpu_load=data.cpu_load,
        memory_usage=data.memory_usage,
        error_rate=data.error_rate,
        latency=data.latency,
        failure_probability=failure_probability,
        decision=decision
    )
    db.add(prediction)
    db.commit()
    
    # Create alert if rollback decision
    if decision == "ROLLBACK":
        alert = Alert(
            alert_type="ROLLBACK_DECISION",
            message=f"Automatic rollback triggered - Failure probability: {failure_probability:.2f}",
            severity="CRITICAL"
        )
        db.add(alert)
        db.commit()
    
    # Update metrics
    prediction_counter.inc()
    if decision == "ROLLBACK":
        rollback_counter.inc()
    prediction_duration.observe(time.time() - start_time)

    return {
        "failure_probability": round(failure_probability, 2),
        "decision": decision
    }


@app.get("/alerts", response_model=List[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.resolved == False).order_by(Alert.timestamp.desc()).limit(10).all()
    return alerts

@app.post("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.resolved = True
        db.commit()
        return {"message": "Alert resolved"}
    return {"error": "Alert not found"}

@app.get("/system-metrics", response_model=List[MetricsResponse])
def get_system_metrics(db: Session = Depends(get_db)):
    metrics = db.query(SystemMetrics).order_by(SystemMetrics.timestamp.desc()).limit(20).all()
    return metrics

@app.get("/predictions/history")
def get_prediction_history(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).order_by(Prediction.timestamp.desc()).limit(50).all()
    return predictions

@app.post("/rollback")
def execute_rollback(db: Session = Depends(get_db)):
    alert = Alert(
        alert_type="ROLLBACK_EXECUTED",
        message="Rollback executed successfully",
        severity="INFO"
    )
    db.add(alert)
    db.commit()
    return {"status": "Rollback executed", "timestamp": datetime.utcnow()}