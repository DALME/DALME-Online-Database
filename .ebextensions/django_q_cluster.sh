#!/usr/bin/env bash
# Get django environment variables
djangoqenv=`cat /opt/python/current/env | tr '\n' ',' | sed 's/export //g' | sed 's/$PATH/%(ENV_PATH)s/g' | sed 's/$PYTHONPATH//g' | sed 's/$LD_LIBRARY_PATH//g'`
djangoqenv=${djangoqenv%?}

# Create djangoq configuraiton script
djangoqconf="[program:django-q]
command=/opt/python/run/venv/bin/python manage.py qcluster
directory=/opt/python/current/app
user=nobody
numprocs=1
stdout_logfile=/var/log/djangoq/worker.log
stderr_logfile=/var/log/djangoq/worker.log
autostart=true
autorestart=true
startsecs=10
; Need to wait for currently executing tasks to finish at shutdown.
stopwaitsecs = 600
; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true
stopasgroup=true
environment=$djangoqenv
"

# Create the djangoq supervisord conf script
echo "$djangoqconf" | tee /opt/python/etc/djangoq.conf

# Add configuration script to supervisord conf (if not there already)
if ! grep -Fxq "[include]" /opt/python/etc/supervisord.conf
  then
  echo "[include]" | tee -a /opt/python/etc/supervisord.conf
  echo "files: djangoq.conf" | tee -a /opt/python/etc/supervisord.conf
fi

# Reread the supervisord config
/usr/local/bin/supervisorctl -c /opt/python/etc/supervisord.conf reread

# Update supervisord in cache without restarting all services
/usr/local/bin/supervisorctl -c /opt/python/etc/supervisord.conf update

# Start/Restart djangoqd through supervisord
/usr/local/bin/supervisorctl -c /opt/python/etc/supervisord.conf restart django-q
