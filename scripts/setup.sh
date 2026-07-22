#!/bin/bash
# ==============================================================================
# Mhmm.ai Developer Setup Script (Idempotent)
# ==============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${ROOT_DIR}"

log_info "Setting up Industrial Knowledge Intelligence Platform (Mhmm.ai)..."

# 1. Environment files setup
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        log_info "Creating root .env from .env.example..."
        cp .env.example .env
    else
        log_warn ".env.example not found; skipping root .env creation."
    fi
else
    log_info "Root .env file already exists."
fi

if [ ! -f backend/.env ]; then
    if [ -f .env.example ]; then
        log_info "Creating backend/.env from .env.example..."
        cp .env.example backend/.env
    fi
else
    log_info "Backend backend/.env file already exists."
fi

# 2. Python virtual environment setup
if [ ! -d ".venv" ]; then
    log_info "Creating Python 3 virtual environment in .venv..."
    python3 -m venv .venv
else
    log_info "Python virtual environment (.venv) already exists."
fi

log_info "Installing Python dependencies (backend & ai_ml)..."
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null || true
pip install --upgrade pip --quiet

if [ -f "backend/requirements.txt" ]; then
    log_info "Installing backend dependencies..."
    pip install -r backend/requirements.txt --quiet
fi

if [ -f "ai_ml/requirements.txt" ]; then
    log_info "Installing ai_ml dependencies..."
    pip install -r ai_ml/requirements.txt --quiet
fi

# 3. Frontend setup
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    log_info "Installing Frontend npm dependencies..."
    (cd frontend && npm install --quiet 2>/dev/null) || log_warn "Host npm install deferred; node_modules is managed inside iki-frontend container."
else
    log_warn "Frontend package.json not found; skipping npm install."
fi

log_info "----------------------------------------------------"
log_info "✅ Setup complete! You can now start the environment with:"
log_info "   bash scripts/start-dev.sh"
log_info "----------------------------------------------------"
