#!/usr/bin/env bash
commands:
  create_post_dir:
    command: "mkdir /opt/elasticbeanstalk/hooks/appdeploy/post"
    ignoreErrors: true

files:
  "/opt/elasticbeanstalk/hooks/appdeploy/post/99_start_djangoq.sh":
    mode: "000755"
    owner: root
    group: root
    content: |
      #!/usr/bin/env bash
      cd /opt/python/current/app
      nohup /opt/python/run/venv/bin/python manage.py qcluster >/dev/null 2>&1 &
