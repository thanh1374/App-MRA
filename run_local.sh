#!/bin/bash

# Ensure Node 20 is available
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
if command -v nvm &> /dev/null; then
    nvm use 20
fi

# Function to clean up background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

echo "======================================"
echo "🚀 Starting App Market Research Analyzer"
echo "======================================"

# Start Backend
echo "[1/2] Starting FastAPI Backend..."
cd backend
if [ ! -d ".venv" ]; then
    echo "Backend virtual environment not found. Please wait while it installs..."
    python3.12 -m venv .venv || python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi
uvicorn app.main:app --reload --reload-dir app --host 127.0.0.1 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "[2/2] Starting React Frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Frontend node_modules not found. Running npm install..."
    npm install > ../logs/frontend_install.log 2>&1
fi
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ All systems go!"
echo "📍 Frontend: http://localhost:5173"
echo "⚙️  Backend:  http://localhost:8000/docs"
echo "📂 Logs are written to the logs/ directory."
echo ""
echo "Press Ctrl+C to stop both servers."

# Wait indefinitely
wait
