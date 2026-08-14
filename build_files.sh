#!/bin/bash
# Install dependencies with --break-system-packages flag for Vercel
pip install --break-system-packages -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Make migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput
