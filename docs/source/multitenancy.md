# Multitenancy

IDA hosts several research projects on one platform. The IDA itself is the
{term}`Central Tenant`, which holds the shared research, and each research
project is an {term}`Orbiting Tenant`. The root `CONTEXT.md` states the model;
this page says how it is built today. #89 documents the system in full,
including which models each kind of tenancy covers.

Tenancy comes in two kinds. They are built differently, bound by different
middleware, and must not be confused.

## Schema tenancy

Each orbiting tenant's CMS lives in its own Postgres schema: the Wagtail sites
and the `web` apps (`PROJECT_TENANT_APPS`), with their own admin log, sessions
and messages. The central tenant lives in the `public` schema, which holds
everything shared (`SHARED_TENANT_APPS`): the ontology, users, OAuth and the
tenants themselves. Every schema can also read `public`.

Each project keeps its own admin log, because the log points at CMS objects by
id and those ids repeat across schemas. A project's sessions are stored with it,
beside the host that set the cookie.

Wagtail keeps data outside its page tree, snippets for example, so filtering one
tree would still show another project's data. A schema per project isolates
each CMS completely.

On each request, `TenantMiddleware` (django-tenants) finds the host among the
registered domains and switches the connection to that tenant's schema. The
tenant's type picks the URL configuration: `app.urls.urls` for the central
tenant, `app.urls.urls_tenant` for an orbiting one (`TENANT_TYPES` in
`app/app/settings.py`).

## Row tenancy

A project's working material is drawn from the IDA and lives in the shared
`public` schema, beside the shared research, but each of its rows carries a
tenant key (`TenantMixin`,
`app/tenants/models/tenant_mixin.py`). On each request,
`TenantContextMiddleware` binds the current tenant into a context variable.
Tenanted managers (`CustomManager`) filter by it when a queryset is built, and
`TenantMixin.save` writes it onto a new row.

The schema and the current tenant are bound separately, so outside a request
they can disagree (#74).

## Neither: the shared research and users

The ontology is not scoped by tenancy. Every project sees the same records,
people, places and attributes, and the data is secured instead by ownership and
authorization over it.

Users are shared too. A user belongs to no tenant, and is a {term}`Member` of
projects through `Tenant.members`.
