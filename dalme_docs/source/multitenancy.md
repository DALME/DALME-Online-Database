# Multitenancy

We've had to employ two different modes of multitenancy in order to implement
our desired architecture.

- Postgres schemas
  - Public site
  - Wagtail needs its db tree to be logically isolated.

- ORM Scope
  - Using a db value we can scope our queries to the appropriate tenant which
    is determined via the incoming request.

Falling out of this design is a third category.

- Unscoped
  - Certain resources should be available to all tenants.
  - IDA `core` models.
