#!/bin/bash
# ==============================================================================
# Mhmm.ai Development Environment Startup Script
# ==============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
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

log_info "Starting Mhmm.ai development environment..."

# 1. Check Docker CLI
if ! command -v docker &> /dev/null; then
    log_error "Docker could not be found. Please install Docker and Docker Compose."
    exit 1
fi

# 2. Check Docker daemon status
if ! docker info &> /dev/null; then
    log_error "Docker daemon is not running. Please start Docker."
    exit 1
fi

# 3. Verify .env files
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        log_info "Creating .env from .env.example..."
        cp .env.example .env
    fi
fi

if [ ! -f backend/.env ]; then
    if [ -f .env.example ]; then
        log_info "Creating backend/.env from .env.example..."
        cp .env.example backend/.env
    fi
fi

# 4. Bring up Docker services
log_info "Bringing up Docker Compose services (postgres, backend, frontend)..."
docker compose up -d

# 5. Wait for backend health check
log_info "Waiting for services to initialize..."
MAX_RETRIES=15
COUNTER=0

until curl -s http://localhost:8000/health &> /dev/null || [ $COUNTER -eq $MAX_RETRIES ]; do
    sleep 2
    COUNTER=$((COUNTER+1))
done

if [ $COUNTER -eq $MAX_RETRIES ]; then
    log_warn "Backend container health check timed out. Checking container status..."
    docker compose ps
else
    log_info "Backend service is healthy!"
fi

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}🚀 Mhmm.ai Development Platform is Running!${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e "📡 Backend API:         ${GREEN}http://localhost:8000${NC}"
echo -e "📖 API OpenAPI Docs:     ${GREEN}http://localhost:8000/docs${NC}"
echo -e "🎨 Frontend Workspace:   ${GREEN}http://localhost:5173${NC}"
echo -e "${CYAN}====================================================${NC}"
