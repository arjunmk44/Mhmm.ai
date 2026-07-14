#!/bin/bash

# Exit on error
set -e

echo "Setting up Industrial Knowledge Intelligence project..."

# Python virtual environment setup
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Frontend setup
echo "Setting up frontend..."
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    (cd frontend && npm ci || npm install)
else
    echo "Frontend scaffolding incomplete (package.json not found). Skipping npm install."
fi

# Backend setup
echo "Setting up backend..."
if [ -d "backend" ] && [ -f "backend/requirements.txt" ]; then
    (
        source .venv/bin/activate || source .venv/Scripts/activate
        pip install --upgrade pip
        pip install -r backend/requirements.txt
    )
else
    echo "Backend scaffolding incomplete (requirements.txt not found). Skipping pip install."
fi

echo "Setup complete! Run 'scripts/start-dev.sh' to start the application."
