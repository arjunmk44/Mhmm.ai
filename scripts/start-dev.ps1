$ErrorActionPreference = "Stop"

Write-Host "[INFO] Starting Mhmm.ai development environment..." -ForegroundColor Cyan

# 1. Check Docker CLI
if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Error "Docker could not be found. Please install Docker Desktop."
    exit 1
}

# 2. Check .env files
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "[INFO] Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
    }
}

if (-not (Test-Path "backend/.env")) {
    if (Test-Path ".env.example") {
        Write-Host "[INFO] Creating backend/.env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" "backend/.env"
    }
}

# 3. Bring up Docker services
Write-Host "[INFO] Bringing up Docker Compose services (postgres, backend, frontend)..." -ForegroundColor Cyan
docker compose up -d

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "🚀 Mhmm.ai Development Platform is Running!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "📡 Backend API:         http://localhost:8000" -ForegroundColor White
Write-Host "📖 API OpenAPI Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "🎨 Frontend Workspace:   http://localhost:5173" -ForegroundColor White
Write-Host "====================================================" -ForegroundColor Cyan
