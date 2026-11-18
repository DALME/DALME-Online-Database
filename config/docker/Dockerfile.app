# ; -*- mode: dockerfile;-*-
# vim: set ft=dockerfile:
ARG BUILD

FROM ghcr.io/astral-sh/uv:0.13.9 AS uv

# Resolves the app's locked dependencies into /opt/venv. Every package in
# uv.lock ships a wheel or is pure Python, so no compiler is needed.
FROM python:3.11-slim-bookworm AS base
COPY --from=uv /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /opt/build
COPY ./pyproject.toml ./uv.lock ./
COPY ./app/pyproject.toml ./app/
COPY ./docs/pyproject.toml ./docs/

### Development stages
FROM base AS dev-reqs
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package dalme-app

FROM python:3.11-slim-bookworm AS install-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libxmlsec1 \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libpq-dev \
    vim \
    xmlsec1 \
    gcc \
    python3-dev \
    graphviz && \
    apt-get clean
COPY --from=dev-reqs /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

### TARGET: development
FROM install-dev AS development
ENV ENV=development
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONBREAKPOINT=ipdb.set_trace
WORKDIR /opt/app
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
ENV DJANGO_CONFIGURATION='CI'
WORKDIR /opt/app
COPY ./app .
RUN mkdir /opt/app/www
RUN openssl genrsa -out /opt/app/oidc.key 4096

### Production stages
FROM base AS reqs
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package dalme-app --no-dev

FROM python:3.11-slim-bookworm AS install
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libxmlsec1 \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libpq-dev \
    xmlsec1 && \
    apt-get clean
COPY --from=reqs /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

### TARGET: production
FROM install AS production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=en_US.UTF-8
ENV BUILD=$BUILD
WORKDIR /opt/app
COPY ./app/app ./app
COPY ./app/authorization ./authorization
COPY ./app/domain ./domain
COPY ./app/oauth ./oauth
COPY ./app/search ./search
COPY ./app/tenants ./tenants
COPY ./app/templates ./templates
COPY ./app/web ./web
COPY ./app/manage.py ./

STOPSIGNAL SIGTERM
