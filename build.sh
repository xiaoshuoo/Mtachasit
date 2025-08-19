#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend

# Install dependencies
pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Go back to root and use manage.py
cd ..
python manage.py collectstatic --no-input
python manage.py migrate
