#!/usr/bin/env bash
# exit on error
set -o errexit

# prepare backend stuff, think of running collect static and compilemessages in build step
python manage.py collectstatic --no-input
python manage.py migrate

# run web server
gunicorn config.wsgi -b 0.0.0.0:8000