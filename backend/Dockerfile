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
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Command to run the application (Placeholder)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
