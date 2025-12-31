#!/bin/bash

echo "Starting NeurOps AI-Driven DevOps Platform..."

# Function to cleanup background processes
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Start backend
echo "Starting backend on http://localhost:8000..."
cd backend
source ../venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend on http://localhost:3000..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🚀 NeurOps is running!"
echo "📊 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📈 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for background processes
wait