#!/bin/bash

# Exit on error
set -e

echo "Starting development environment..."

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker could not be found. Please install Docker."
    exit 1
fi

# Copy .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        echo "Warning: .env.example not found, could not create .env"
    fi
fi

# Start services
echo "Bringing up Docker Compose services..."
# Use docker compose plugin directly (newer standard)
docker compose up -d

echo "----------------------------------------"
echo "✅ Development environment is running!"
echo "📡 Backend: http://localhost:8000"
echo "🎨 Frontend: http://localhost:5173"
echo "----------------------------------------"
