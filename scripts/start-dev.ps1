$ErrorActionPreference = "Stop"

Write-Host "Starting development environment..." -ForegroundColor Cyan

# Check if docker is installed
if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Error "Docker could not be found. Please install Docker."
    exit 1
}

# Copy .env if it doesn't exist
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
    } else {
        Write-Warning ".env.example not found, could not create .env"
    }
}

# Start services
Write-Host "Bringing up Docker Compose services..." -ForegroundColor Cyan
docker compose up -d

Write-Host "----------------------------------------" -ForegroundColor Green
Write-Host "✅ Development environment is running!" -ForegroundColor Green
Write-Host "📡 Backend: http://localhost:8000"
Write-Host "🎨 Frontend: http://localhost:5173"
Write-Host "----------------------------------------" -ForegroundColor Green
