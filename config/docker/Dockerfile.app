# ; -*- mode: dockerfile;-*-
# vim: set ft=dockerfile:
ARG BUILD

FROM python:3.11-slim-bookworm AS base
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    libcurl4-openssl-dev \
    libmariadbd-dev \
    libpq-dev \
    libssl-dev \
    python3-dev && \
    apt-get clean

### Development stages
FROM base AS dev-reqs
WORKDIR /opt/build
COPY ./app/requirements.txt ./app/requirements-dev.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir ./wheels -r requirements-dev.txt

FROM python:3.11-slim-bookworm AS install-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libxmlsec1 \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libmariadbd-dev \
    libpq-dev \
    vim \
    xmlsec1 \
    gcc \
    python3-dev \
    graphviz && \
    apt-get clean
COPY --from=dev-reqs /opt/build/wheels ./wheels
RUN pip install --user --no-cache-dir --upgrade pip
RUN pip install --no-cache ./wheels/*

### TARGET: development
FROM install-dev AS development
ENV ENV=development
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONBREAKPOINT=ipdb.set_trace
WORKDIR /opt/app
COPY ./config/env.web.dev ./.env
COPY ./config/oidc.key ./oidc.key
RUN mkdir /opt/app/www
CMD ["python", "manage.py", "runserver_plus", "--nostatic", "0.0.0.0:8001"]
STOPSIGNAL SIGINT

### CI stage
FROM install-dev AS ci
ENV ENV=ci
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG DAM_DB_NAME
ARG DAM_DB_USER
ARG DAM_DB_PASSWORD
ARG DAM_DB_HOST
ENV DAM_DB_NAME=$DAM_DB_NAME \
    DAM_DB_USER=$DAM_DB_USER \
    DAM_DB_PASSWORD=$DAM_DB_PASSWORD \
    DAM_DB_HOST=$DAM_DB_HOST \
    DAM_DB_PORT=$DAM_DB_PORT
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST
ARG POSTGRES_PORT
ENV POSTGRES_DB=$POSTGRES_DB \
    POSTGRES_USER=$POSTGRES_USER \
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    POSTGRES_HOST=$POSTGRES_HOST \
    POSTGRES_PORT=$POSTGRES_PORT
ENV LOG_LEVEL=ERROR
ENV OAUTH_CLIENT_ID=oauth.ida.development
ENV OAUTH_CLIENT_SECRET=django-insecure-development-environment-oauth-client-secret
ENV OIDC_RSA_PRIVATE_KEY=/opt/app/oidc.key
WORKDIR /opt/app
COPY ./app .
RUN mkdir /opt/app/www
RUN openssl genrsa -out /opt/app/oidc.key 4096

### Production stages
FROM base AS reqs
WORKDIR /opt/build
COPY ./app/requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir ./wheels -r requirements.txt

FROM python:3.11-slim-bookworm AS install
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libxmlsec1 \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libmariadbd-dev \
    libpq-dev \
    xmlsec1 && \
    apt-get clean
COPY --from=reqs /opt/build/wheels ./wheels
RUN pip install --user --no-cache-dir --upgrade pip
RUN pip install --no-cache ./wheels/*

### TARGET: production
FROM install AS production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=en_US.UTF-8
ENV BUILD=$BUILD
WORKDIR /opt/app
COPY ./app/manage.py ./
COPY ./app/app ./app
COPY ./app/domain ./domain
COPY ./app/api ./api
COPY ./app/purl ./purl
COPY ./app/web ./web
COPY ./app/tenants ./tenants
COPY ./app/static ./static
STOPSIGNAL SIGTERM
