#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Stripe Payment Element Development Servers${NC}"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${GREEN}Creating .env file from template...${NC}"
    cp backend/env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your Stripe API keys!"
    echo ""
fi

# Start backend in background
echo -e "${GREEN}Starting Flask backend on port 5000...${NC}"
cd backend
source venv/bin/activate 2>/dev/null || echo "Virtual environment not found. Please create one with: python3 -m venv venv"
python app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend
echo -e "${GREEN}Starting React frontend on port 3000...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✓ Servers started!${NC}"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

