FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure start.sh permissions and ownership
RUN chmod +x start.sh && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Command to run database migration & application
CMD ["/app/start.sh"]

