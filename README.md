# NeurOps - AI-Driven DevOps Automation Platform

## Overview
NeurOps is a smart DevOps automation platform that uses Artificial Intelligence to monitor, predict, and manage application deployments automatically. It reduces manual intervention and prevents system failures before users are affected.

## Features
- 🤖 **AI-Powered Predictions** - ML models predict deployment failures
- 📊 **Real-time Monitoring** - System metrics and alerts dashboard
- 🔄 **Automated Rollbacks** - Automatic rollback on failure detection
- 📈 **Anomaly Detection** - Identifies unusual system behavior
- 🚀 **Traffic Prediction** - Forecasts load spikes
- 🐳 **Containerized** - Docker and Kubernetes ready
- 📱 **React Dashboard** - Modern web interface

## Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │    │   FastAPI       │    │   ML Models     │
│   Dashboard     │◄──►│   Backend       │◄──►│   & Database    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Prometheus    │    │   Kubernetes    │    │   CI/CD         │
│   Monitoring    │    │   Deployment    │    │   Pipeline      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Node.js 18+
- Kubernetes (optional)

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd neurops

# Start with Docker Compose
docker-compose up --build

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
```

### Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start

# ML Models
cd ml
python train.py
python anomaly_detection.py
python traffic_prediction.py
```

### Kubernetes Deployment
```bash
# Deploy to Kubernetes
./deploy.sh

# Or manually
kubectl apply -f k8s/
```

## API Endpoints

### Predictions
- `POST /predict` - Make deployment decision
- `GET /predictions/history` - Get prediction history

### Monitoring
- `GET /alerts` - Get active alerts
- `POST /alerts/{id}/resolve` - Resolve alert
- `GET /system-metrics` - Get system metrics
- `GET /metrics` - Prometheus metrics

### Operations
- `POST /rollback` - Execute rollback
- `GET /` - Health check

## ML Models

### 1. Deployment Failure Prediction
- **Algorithm**: Random Forest Classifier
- **Features**: CPU load, memory usage, error rate, latency
- **Output**: Failure probability, PROCEED/ROLLBACK decision

### 2. Anomaly Detection
- **Algorithm**: Isolation Forest
- **Purpose**: Detect unusual system behavior
- **Features**: System metrics patterns

### 3. Traffic Prediction
- **Algorithm**: Polynomial Linear Regression
- **Purpose**: Forecast traffic spikes
- **Features**: Time-based patterns

## Dashboard Features

### Predictions Tab
- Manual metric input
- Auto-mode simulation
- Real-time predictions
- Decision history

### Alerts Tab
- Active system alerts
- Alert resolution
- Severity levels (Critical, High, Info)

### Metrics Tab
- System resource usage
- Real-time monitoring
- Historical data

## Configuration

### Environment Variables
```bash
# Backend
DATABASE_URL=sqlite:///./neurops.db
PYTHONPATH=/app

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### Docker Compose Services
- `backend` - FastAPI application
- `frontend` - React application
- `prometheus` - Metrics collection
- `grafana` - Visualization dashboard

## CI/CD Pipeline

GitHub Actions workflow includes:
- Automated testing
- Docker image building
- Kubernetes deployment
- Model retraining

## Model Retraining

Automated retraining pipeline:
```bash
cd ml
python retrain_pipeline.py
```

Features:
- Incremental learning
- Performance evaluation
- Model versioning
- Metadata tracking

## Monitoring Stack

### Prometheus Metrics
- `predictions_total` - Total predictions made
- `rollbacks_total` - Total rollback decisions
- `prediction_duration_seconds` - Prediction latency

### System Metrics
- CPU usage percentage
- Memory usage percentage
- Disk usage percentage
- Network I/O

### Alerts
- High resource usage (>80%)
- Rollback decisions
- System anomalies

## Production Deployment

### Security
- Environment-based configuration
- Database connection pooling
- Rate limiting (recommended)
- Authentication (to be implemented)

### Scaling
- Horizontal pod autoscaling
- Load balancing
- Database clustering
- Caching layer

### Monitoring
- Log aggregation
- Error tracking
- Performance monitoring
- Alerting rules

## Development

### Project Structure
```
neurops/
├── backend/           # FastAPI application
├── frontend/          # React application
├── ml/               # Machine learning models
├── k8s/              # Kubernetes manifests
├── monitoring/       # Prometheus config
├── .github/          # CI/CD workflows
└── docker-compose.yml
```

### Adding New Features
1. Update ML models in `ml/`
2. Add API endpoints in `backend/main.py`
3. Update frontend in `frontend/src/`
4. Update documentation

## Troubleshooting

### Common Issues
1. **Backend not starting**: Check Python dependencies
2. **Frontend build fails**: Verify Node.js version
3. **ML model errors**: Ensure training data exists
4. **Database issues**: Check SQLite permissions

### Logs
```bash
# Docker logs
docker-compose logs backend
docker-compose logs frontend

# Kubernetes logs
kubectl logs deployment/neurops-backend
kubectl logs deployment/neurops-frontend
```

## Contributing
1. Fork the repository
2. Create feature branch
3. Add tests
4. Submit pull request

## License
MIT License - see LICENSE file for details