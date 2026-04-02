#!/bin/bash
# Render Build Script for Finance Dashboard Backend
# This script runs during the deployment process

set -e  # Exit on error

echo "=== Building Finance Dashboard Backend ==="

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build Complete ==="
