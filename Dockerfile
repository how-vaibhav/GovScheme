# Multi-stage Dockerfile for GovAid

# Stage 1: Build Tailwind CSS
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY package*.json tailwind.config.js ./
RUN npm install
COPY templates/ ./templates/
COPY schemesapp/templates/ ./schemesapp/templates/
COPY static/ ./static/
RUN npm run build:css

# Stage 2: Python Application
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Copy compiled CSS from frontend builder
COPY --from=frontend-builder /app/static/css/output.css ./static/css/output.css

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "gov_schemes.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
