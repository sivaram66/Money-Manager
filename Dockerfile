# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 3. Create workdir
WORKDIR /app

# 4. Install system deps for PostgreSQL and building packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 6. Copy the rest of the code
COPY . .


# 8. Expose the port Gunicorn will run on
EXPOSE 8000
RUN mkdir -p /app/sessions
# 9. Run migrations, collectstatic & launch Gunicorn
ENTRYPOINT ["./entrypoint.sh"]