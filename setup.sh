#!/bin/bash

echo "Setting up NeurOps AI-Driven DevOps Automation Platform..."

# Install Python dependencies for ML
echo "Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Train ML models
echo "Training ML models..."
cd ml
python3 train.py
python3 anomaly_detection.py
python3 traffic_prediction.py
cd ..

echo "Setup completed! You can now run:"
echo "  docker-compose up --build    # For Docker deployment"
echo "  ./deploy.sh                  # For Kubernetes deployment"
echo ""
echo "Or run services individually:"
echo "  Backend:  cd backend && uvicorn main:app --reload"
echo "  Frontend: cd frontend && npm start"