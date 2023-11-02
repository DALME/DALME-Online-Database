"""Utility to retrieve the active, request tenant.

We can't define this in utils/middleware because the import tree is getting
quite complex and brittle at this point and it breaks start-up trying to import
everything in the utils module which includes lots of models that are not yet
loaded. So just put this at the top-level so it's clean and ready for use.

"""


def get_current_tenant():
    """Defer importing the tenant context to minimize impact on import resolution."""
    from dalme_app.utils import TENANT

    return TENANT
