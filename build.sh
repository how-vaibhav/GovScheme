#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Installing Node dependencies & compiling Tailwind CSS..."
npm install
npm run build:css

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Seeding initial schemes..."
python manage.py populate_schemes

echo "==> Build complete!"
