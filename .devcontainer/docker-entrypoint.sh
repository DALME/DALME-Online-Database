#!/bin/sh
set -eu

echo "Checking DB connection..."
i=0
until [ $i -ge 20 ]
do
  nc -z db 3306 && break
  i=$(( i + 1 ))
  echo "$i: Waiting for DB..."
  sleep 1
done

if [ $i -eq 20 ]
then
  echo "DB connection refused, terminating..."
  exit 1
fi

echo "DB is up..."

echo "Running Migrations..."
python manage.py migrate

echo "Starting runserver..."
python manage.py runserver 0.0.0.0:8000
