#!/bin/bash
set -e

if [ -v MIGRATE ]; then
  echo "Running migrations..."
  python manage.py migrate
fi

echo "Starting $@"
exec "$@"
