# Use an official Python runtime as a parent image
FROM python:3.11-slim as base

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create working directory
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf ~/.cache/pip

# Copy project files
COPY . .

# Create session directory
RUN mkdir -p /app/sessions

# Expose the port for Gunicorn
EXPOSE 8000

# Set entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
