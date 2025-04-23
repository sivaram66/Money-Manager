# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# 3. Create workdir
WORKDIR /app

# 4. Install system deps for PostgreSQL and building packages in a single RUN command
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 6. Copy the rest of the code (this must come after the dependency installation)
COPY . .

# 7. Create a session directory
RUN mkdir -p /app/sessions

# 8. Expose the port Gunicorn will run on
EXPOSE 8000

# 9. Run migrations, collectstatic & launch Gunicorn
ENTRYPOINT ["./entrypoint.sh"]
