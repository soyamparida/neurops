#!/bin/bash

echo "Deploying NeurOps to Kubernetes..."

# Build Docker images
echo "Building Docker images..."
docker build -t neurops-backend:latest ./backend
docker build -t neurops-frontend:latest ./frontend

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/backend-deployment.yml
kubectl apply -f k8s/frontend-deployment.yml
kubectl apply -f k8s/monitoring-deployment.yml

# Wait for deployments
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/neurops-backend
kubectl wait --for=condition=available --timeout=300s deployment/neurops-frontend
kubectl wait --for=condition=available --timeout=300s deployment/prometheus

# Get service URLs
echo "Getting service URLs..."
echo "Backend: $(kubectl get svc neurops-backend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):8000"
echo "Frontend: $(kubectl get svc neurops-frontend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):3000"
echo "Prometheus: $(kubectl get svc prometheus-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):9090"

echo "NeurOps deployment completed!"