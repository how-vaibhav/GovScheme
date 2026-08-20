#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Handling CSS Build..."
if command -v npm &> /dev/null; then
    npm install --no-audit --no-fund || true
    if [ -d "node_modules/.bin" ]; then
        chmod -R +x node_modules/.bin || true
    fi
    npm run build:css || npx --yes tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify || echo "Using pre-compiled static/css/output.css"
else
    echo "Node/NPM not found, using pre-compiled static/css/output.css"
fi

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Seeding initial schemes..."
python manage.py populate_schemes

echo "==> Build complete!"
