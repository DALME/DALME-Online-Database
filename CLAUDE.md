# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project Overview

DALME v2: Django 5.1 / Wagtail 6.4 / DRF backend (Python 3.11), Quasar 2 / Vue 3
frontend (JavaScript), multitenant via django-tenants. All dev tasks run through
`make`.

- `development.v2` is the working branch, deployed to **staging**. Staging is
  improved in place.
- `master` is v1, in production. Out of scope: do not touch it.
- Neither maintainer has had the bandwidth to keep the project current, so
  expect everything to be out of date. Drift is the starting state, not a
  finding; it is overhauled under #50, not patched piecemeal.

## The Process

All work follows **The Process** (`docs/source/process/`). It shares its
fundamentals with the SHARIAsource Hub's, but the two may diverge in detail.

- Tickets live on `DALME/DALME-Online-Database`, never the `ocp` fork.
- Organisation issue types: Meta, Story, Epic, Task, Fix, Bug, Feature, Intake
  and ADR. Templates are in `.github/ISSUE_TEMPLATE/`.
- Titles: `META | <Area>`, `<Topic> | <Name>` for stories and epics,
  `ADR | <Decision>`; tasks, fixes, features and bugs are plain. Bodies open
  with `` `ida/#N` ``; branches are `ida/#N`, cut from `development.v2`.
- Raw feedback, bugs and ideas go under the rolling intake, #49.
- Create and edit tickets with `gh issue create|edit --type <Type> --parent <N>`
  (`--add-sub-issue` on the parent side), not `gh api`.
- Before reasoning about the domain, read the chain of `CONTEXT.md` files from
  the root down. The ontology in `app/domain` is @gpizzorno's design: learn its
  intent before judging any part of it.
- Draft every ticket, comment and PR in full and wait for approval before
  posting.

## Quality Gates

Mandatory once you have produced a real diff. Run them yourself.

1. **Always:** `.venv/bin/prek run --all-files` (lint and format for backend,
   frontend, docs and Terraform).
2. **Scoped tests:**

| Changed | Run |
|---|---|
| `app/` | `make app.test` |
| `ui/` | `make ui.test` |
| `docs/` | `make docs.render` (Sphinx with `-nW`: any warning fails the build) |
| `tf/` | `make deploy.lint` |
| mixed | every relevant row |

Fix a failing gate; never bypass it. Never use `--no-verify`. Never present
commit commands before the gates pass.

## Commit Rule

Never run `git commit`. Give the user the exact message and command.

## Workflow Rules

- Git flow, pull requests and the pipelines: `.github/CLAUDE.md`.
- Drive every task through `make`, tests above all: never call `manage.py`,
  `pytest`, `yarn` or `vitest` directly, on the host or through
  `docker compose exec`. If no target fits, ask before reaching round one.
- Do not scan `node_modules`, `.venv`, `.terraform`, `.terragrunt-cache` or
  `docs/_build` unless asked.
- Never commit secrets. `config/env.web.dev` and `*.key` files are gitignored.

## Essential Commands

```bash
make init                             # Bootstrap the dev environment
make dev                              # Start all services and follow logs
make sync                             # Rebuild after dependency changes
make app.lock                         # Re-resolve uv.lock after editing a pyproject.toml
make app.upgrade                      # Upgrade every locked dependency
make test                             # app.test + ui.test

make app.test [args='...']            # pytest with coverage
make app.test.u / .i / .p             # Unit / integration / property
make app.manage args='...'            # Django management command
make app.python                       # shell_plus

make ui.test                          # Vitest
make ui.lint                          # ESLint

make db.migrate                       # migrate_schemas
make db.migrations.make               # makemigrations
make db.psql

make docs.render                      # Static Sphinx build
make deploy.plan module='...'         # Terragrunt, staging only
```

Host ports are defined once in the `Makefile` and overridden per run, as in
`make dev DEV_PORT=8001`: `DEV_PORT` (8000), `DOCS_PORT` (8002), `ES_PORT`
(9200), `NOTEBOOK_PORT` (8888) and `PGADMIN_PORT` (5050). Local tenants are
served on `DEV_PORT`:
`ida.localhost`, `dalme.localhost` and `pharmacopeias.localhost`. After `make init` and `make db.migrate`, run
`make app.manage args="ensure_tenants"` and `make app.manage args="ensure_oauth"`,
then `make app.manage args="create_superuser"` to make a login.

## Architecture

Backend packages under `app/`:

- `app/`: settings, URL routing, middleware, shared mixins, access policies.
- `domain/`: the research ontology, its DRF API, and the v1→v2 `migrate_data`
  pipeline.
- `tenants/`: tenant and domain models, tenancy middleware, storage backends.
- `oauth/`: users, and the app's own OAuth2/OIDC provider.
- `web/`: the Wagtail public sites and `web.extensions.*`.
- `search/`: Elasticsearch/OpenSearch indexing.
- `authorization/`: drf-access-policy statements.

Tenancy comes in two kinds: Postgres schemas for the CMS, and tenant ids on rows
for the backend and ontology. Only some data is tenanted; the rest is
deliberately **shared**.

Frontend in `ui/`; infrastructure in `tf/` (Terragrunt on AWS); docs in `docs/`
(Sphinx + MyST).
