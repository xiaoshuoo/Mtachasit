#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r backend/requirements.txt

# Collect static files
cd backend
python manage.py collectstatic --no-input
python manage.py migrate
