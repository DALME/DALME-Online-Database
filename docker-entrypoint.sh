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

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Updating compress manifest..."
python manage.py compress

echo "Starting runserver..."
mod_wsgi-express start-server \
    --url-alias /static www/static \
    --application-type module dalme.wsgi \
    --log-to-terminal \
    --log-level info \
    --startup-log \
    --https-port 8443 \
    --https-only \
    --server-name db.127.0.0.1.xip.io \
    --server-alias public.127.0.0.1.xip.io \
    --server-alias data.127.0.0.1.xip.io \
    --server-alias purl.127.0.0.1.xip.io \
    --ssl-certificate-file dev-localhost.cert \
    --ssl-certificate-key-file dev-localhost.key \
    --reload-on-changes \
    --user whiskey \
    --group root
