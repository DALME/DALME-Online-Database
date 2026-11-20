# app/CLAUDE.md

Backend guidance. The root `CLAUDE.md` holds the project-wide rules, gates and
commands.

## Tests

Run them through make: `make app.test [args='...']`, or one marker at a time with
`make app.test.u`, `.i` and `.p`. They run under the `Test` configuration, whose
storages are in memory.

The markers are `unit`, `integration` and `property`. `tests/conftest.py` sets
them: `integration` for a test that touches the database or a client, `property`
for one that uses Hypothesis's `given`, and `unit` for the rest. So a marker is
rarely written by hand.

### Fixtures live in a `conftest.py`, always

Every fixture is defined in a `conftest.py` and injected into the tests that
need it. Never define a fixture in a test module, even one that only that module
uses: a fixture is shared setup, and one kept in a test module can be reached
from nowhere else.

`conftest.py` files nest, and a fixture is visible at and below its directory.
Put each one in the narrowest `conftest.py` that covers all its users:
`tests/conftest.py` for anything shared across apps, `tests/<app>/conftest.py`
for anything shared within one, and a new `conftest.py` at any deeper level where
a group of tests wants its own. Shared helpers and Hypothesis strategies follow
the same rule. Model factories live in `tests/factories/` and reach tests through
the `factories` fixture.

### What a test may fake

Integration tests hit a real database. Never mock the database layer, because
the library's behaviour is usually part of the claim.

### Tests come first

New behaviour arrives with its tests. A bug gets a failing regression test
before its fix, and the test is watched failing for the reason it claims.

### Known traps

- Importing `domain.api` queries the database: `Agents.queryset` evaluates
  attribute lists when the class is defined
  (`domain/api/resources/agents/endpoints.py:24`). A test can only import a
  viewset once the database is available.
- A tenanted manager raises "object is not bound" when no tenant is current.
  No fixture binds one yet, so some tests mock `get_current_tenant` module by
  module (#59).

## Management commands

- An `ensure_*` command is idempotent and safe to run on every deploy; the ECS
  start chain runs them (`tf/modules/services/ida/main.tf`). A command that
  fails raises `CommandError`. It never logs and exits 0.
- A command runs in the public schema. Run one in every schema with
  `all_tenants_command <command>`, or in one with
  `tenant_command <command> --schema=<name>`.
- `create_superuser` runs only in development and `ensure_superuser` only in
  deploy environments. The builtin `createsuperuser` refuses.

## Migrations

Generate them with `make db.migrations.make`, and never edit one that has
landed: a changed migration breaks every database already past it. The
`migrations` hook fails on a model change that has no migration.
