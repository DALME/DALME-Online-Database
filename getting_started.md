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
