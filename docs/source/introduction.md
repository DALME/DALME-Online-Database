# Introduction

Welcome to the IDA documentation.

## Getting Started

The `Makefile` system provides an interface for all development functionality.

You can get `make` help at any time with:

```
$ make
# Which is an alias for...
$ make help
```

### `.env`

We still need to utilize a `.env` file for some RDS/DAM credentials
but we are working to eliminate that need completely in the local
environment. If you do still need it ask for it and add those values
to a file located at `config/env.web.dev` (which is `.gitignored` so
you'll have to create it yourself). This file will be picked up and
used by the development Docker image.

### Initialization

To initialize the developer environment for the first time, invoke the
following.

```
$ make init
$ make db.migrate
$ make web.manage args='ensure_tenants'
$ make web.manage args='ensure_oauth'
$ make web.manage args='createsuperuser'
```

Once everything is built you can come back and start the environment
at anytime with:

```
$ make dev
```

This command will also tail the Docker logs in the terminal for your
reference.
