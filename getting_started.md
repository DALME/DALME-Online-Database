# Getting Started

### Software Required

- [Docker](https://www.docker.com/get-started)

### Setup

Clone this repo and `cd` into the project.
```
git clone https://github.com/DALME/dalme.git
````

Copy the `env.web.dev` and `env.ui.dev` files to the `config/dev` directory.

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
$ docker-compose up -d --build

# List running containers.
$ docker ps

# Show the container logs.
$ docker-compose logs
$ docker-compose logs dalme.ui

# Stop the containers.
$ docker-compose down

# Start them again (they are already built).
$ docker-compose up -d

# Rebuild them.
$ docker-compose up -d --build --force-recreate
```

Run commands against docker containers.
```
# docker-compose run $CONTAINER $COMMAND
$ docker-compose run dalme.web python manage.py makemigrations
$ docker-compose run dalme.web python manage.py migrate

# Shell into a running container.
$ docker-compose run dalme.web bash
```

Login to the DALME editing environment at
`https://db.127.0.0.1.sslip.io:8000/`.  You will probably have to bypass an SSL
insecure certificate warning and then you are likely see further
`net::ERR_CERT_AUTHORITY_INVALID` errors due to failing API calls in dev tools
console. If this is the case, open up one of the failing URLs in a new tab
(for example, [this
one](https://data.127.0.0.1.sslip.io:8000/session/retrieve/) and
again bypass the SSL certificate warning. Remote calls to the API subdomain
should then succeed.

The main entrypoint URLs are found below.
```
https://127.0.0.1.sslip.io:8000/       # Public site.
https://127.0.0.1.sslip.io:8000/cms/   # Wagtail CMS.
https://data.127.0.0.1.sslip.io:8000/  # DALME API.
https://127.0.0.1.sslip.io:8000/ui     # Vue editing-environment.
```
Using the [`sslip.io`](http://sslip.io/) DNS resolution is necessary for
CSRF/cookie signing across local subdomains.
