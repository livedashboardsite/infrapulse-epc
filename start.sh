#!/bin/bash

# Start InfraPulse EPC Backend and Frontend on Unix/Linux/Mac

echo "========================================"
echo "InfraPulse EPC - Starting Application"
echo "========================================"

echo -e "\nStarting Backend (FastAPI on http://localhost:8000..."
cd backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload &
BACKEND_PID=$!
cd ..

sleep 3

echo -e "\nStarting Frontend (Vite on http://localhost:5173..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "\nApplication started successfully!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
