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

We still need to utilize a `.env` file for the RDS database credentials but we
are working to eliminate that need in the local environment. If you need it ask
for it and add those values to a file located at `config/env.web.dev` (which
is .gitignored). This file will be picked up by the development Docker image.

To initialize the developer environment for the first time, invoke:

```
$ make init
$ make db.migrate
$ make web.manage args='ensure_tenants'
$ make web.manage args='createsuperuser'
```

Once everything is built you can come back and start the environment with:

```
$ make dev
```
