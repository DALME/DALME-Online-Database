"""Customize the database router."""


class ModelDatabaseRouter:
    """Allows each model to set its own db target."""

    def db_for_read(self, model, **hints):  # noqa: ARG002
        """Return db for read."""
        return model._meta.in_db if hasattr(model._meta, 'in_db') else None  # noqa: SLF001

    def db_for_write(self, model, **hints):  # noqa: ARG002
        """Return db for write."""
        return model._meta.in_db if hasattr(model._meta, 'in_db') else None  # noqa: SLF001

    def allow_syncdb(self, db, model):
        """Return boolean indicating whether db sync is allowed."""
        # Random models that don't specify a database can only go to 'default'
        return model._meta.in_db == db if hasattr(model._meta, 'in_db') else db == 'default'  # noqa: SLF001
