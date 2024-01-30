# Multitenancy

The DALME codebase was originally designed for just a single 'tenant' or team,
DALME itself. The decision to open the system up for the use of multiple,
concurrent parties has led to the need for a significant refactoring in order
to become a 'multitenant architecture'.

## Multitenancy Modes

We've had to implement three different modes of multitenancy in order to meet
our desired requirements.

### #1 Postgres Schemas

Used **only** by the `dalme_public` site (ie. the Wagtail CMS).

Due to the design of Wagtail, not everything has a place on the CMS tree
([Snippets](https://docs.wagtail.org/en/stable/topics/snippets/index.html) for
example), so it's not enough to achieve multitenancy in Wagtail simply by
making the db tree alone logically isolated and only filtering strictly within
a particular tree for example. Such a method will still return values from
other CMS instances which don't reside within the tree, something we don't want
to happen.

Because of this design fact we've had to take a stronger approach and
absolutely isolate Wagtail/CMS data per tenant within namespaced [postgres
schemas](https://www.postgresql.org/docs/current/ddl-schemas.html). Only tables
from the `dalme_public` app use these tenant schemas. Everything else resides
in the [default `public`
schema](https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PUBLIC)

:::{note}
There is some slightly confusing terminology here, but it's just a coincidence.
Just don't mistake the `public` schema for the `dalme_public` app, even though
they are related conceptually.
:::

### #2 ORM Scoped (aka "Core")

Using a `tenant` column on a table we can scope our queries to the
appropriate tenant which is determined via the origin of the incoming request.


### #3 Unscoped (aka "Research")

Falling out of this design is a third category. Certain resources should be
available to all tenants and so do not fall under the remit of any scoping
mechanisms.

For example the IDA data models fall into this category. That data set
represents the common documentary substrata out of which all tenants can curate
their own scoped 'research' data.

Technically speaking this mode is not really 'multitenant' at all, not being
scoped in any way. However in the context of our particular architecture it
makes up a significant part of the system and so should be seen as a kind of
negative complement to the overall multitenancy patterns.

## Tenant Middleware

- https://django-tenants.readthedocs.io/en/latest/
