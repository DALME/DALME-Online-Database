# Getting Started

### Software Required

- [Docker](https://www.docker.com/get-started)

### Setup

Clone this repo and `cd` into the project.
```
git clone https://github.com/DALME/dalme.git
````

Copy the `env.web.dev` and `env.ui.dev` files to the `config/dev` directory.

`env.web.dev` should contain the following variables:

AWS credentials:
- AWS_DEFAULT_REGION (e.g. us-east-1)
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_ES_ENDPOINT (e.g. <endpoint>.us-east-1.es.amazonaws.com)
- AWS_STORAGE_BUCKET_NAME
- AWS_SQS_QUEUE

Django settings:
- SECRET_KEY
- DJANGO_SETTINGS_MODULE (e.g. dalme.settings.development)
- DJANGO_SUPERUSER_EMAIL
- DJANGO_SUPERUSER_NAME
- DJANGO_SUPERUSER_PASSWORD
- HOST (e.g. 127.0.0.1.sslip.io:8000)
- DEBUG (on=1, off=0)
- EMAIL_HOST (e.g. smtp.gmail.com)
- EMAIL_USER
- EMAIL_PASSWORD

Database settings, either for RDS or local MySQL instance (if both are provided the system will prioritize RDS):
- RDS_DB_NAME or MYSQL_DATABASE
- RDS_USERNAME or MYSQL_USER
- RDS_PASSWORD or MYSQL_PASSWORD
- RDS_HOSTNAME or MYSQL_HOST
- RDS_PORT or MYSQL_PORT

Gunicorn settings:
- GUNICORN_BIND
- GUNICORN_WORKERS
- GUNICORN_WORKER_CLASS
- GUNICORN_THREADS
- GUNICORN_RELOAD
- GUNICORN_KEYFILE
- GUNICORN_CERTFILE

DAM access credentials:
- DAM_API_KEY
- DAM_API_USER
- DAM_DB_NAME
- DAM_HOSTNAME
- DAM_PORT (e.g. 3306)
- DAM_USERNAME
- DAM_PASSWORD

Zotero API information:
- ZOTERO_LIBRARY_ID
- ZOTERO_API_KEY

Recaptcha keys:
- RECAPTCHA_PUBLIC_KEY
- RECAPTCHA_PRIVATE_KEY

`env.ui.dev` contains a single variable to that sets the environment for the SPA:

- NODE_ENV (e.g. development, beta, production)

Create an `ssl-certs` directory in the project root and copy the
`dev-localhost.cert` and `dev-localhost.key` there.

Move your copy of the DALME database to the `./sql` directory at the top-level
of the project. Docker will mount this entire directory and run all `.sql`
files it finds here (in alphabetical order) when building the `dalme.db`
container for the first time. The db will persist its state in a volume when
you stop and start the containers, but if for whatever reason you want to start
fresh just drop the volumes when you spin down with `docker-compose down -v`.

Build and start the container network in the background.
```
$ docker compose -f docker-compose.dev.yml up -d --build

# List running containers.
$ docker ps

# Show the container logs.
$ docker compose logs
$ docker compose logs dalme.ui

# Stop the containers.
$ docker compose -f docker-compose.dev.yml down

# Start them again (they are already built).
$ docker compose -f docker-compose.dev.yml up -d

# Rebuild them.
$ docker compose -f docker-compose.dev.yml up --build --force-recreate

# prune system (esp. to address 'no space left on device' error arising from lack of available i-nodes)
$ docker system prune --all
```

Run commands against docker containers.
```
# docker compose -f docker-compose.dev.yml run $CONTAINER $COMMAND
$ docker compose -f docker-compose.dev.yml run dalme.web python manage.py makemigrations
$ docker compose -f docker-compose.dev.yml run dalme.web python manage.py migrate

# Shell into a running container.
$ docker compose -f docker-compose.dev.yml run dalme.web bash
```

Note, due to Chrome recently disallowing its users to manually bypass insecure
SSL connections, in order to demo the site locally you will either need to use
Firefox as your browser or know about
[`thisisunsafe`](https://dev.to/brettimus/this-is-unsafe-and-a-bad-idea-5ej4).

Once running, login to the [new DALME editing environment](https://127.0.0.1.sslip.io:8000/db/).

The main entrypoint URLs are found below.
```
https://127.0.0.1.sslip.io:8000/       # Public site.
https://127.0.0.1.sslip.io:8000/cms/   # Wagtail CMS.
https://127.0.0.1.sslip.io:8000/api/    # DALME API.
https://127.0.0.1.sslip.io:8000/db/     # Vue editing-environment.
```
Using the [`sslip.io`](http://sslip.io/) DNS resolution is necessary for
CSRF/cookie signing across local subdomains.
