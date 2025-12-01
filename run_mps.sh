#!/bin/bash

# Script to run the multimodal application with MPS support

echo "🚀 Starting Multimodal AI Playground with MPS support..."

# Activate virtual environment
source multimodal_env/bin/activate

# Set environment variables for MPS
export DEVICE=mps
export PORT=8000
export CACHE_DIR=./models

# Start the application
echo "Starting server on http://localhost:$PORT"
echo "Using device: MPS (Metal Performance Shaders)"
echo "Models will be cached in: $CACHE_DIR"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT