"""Define the health check middleware."""

from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class HealthCheckMiddleware(MiddlewareMixin):
    """Smoke test middleware for ECS production environments.

    The healthcheck request itself comes from ECS at service deploy time, and
    since we don't know the private IP beforehand this middleware ensures that
    the route always returns some informative response even after we restrict
    ALLOWED_HOSTS later down the chain.

    """

    def __init__(self, get_response):
        """Initialize HealthCheckMiddleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Intercept ping requests.

        If we are in development mode we probably just want to see the familiar
        Django debug info page telling us that some relation doesn't exist and
        that we've forgotten to run the migrations, so we'll skip this check
        when DEBUG is on and just let the request pass through unhindered.

        """
        if request.META['PATH_INFO'] == '/api/healthcheck/':
            executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            detail, status = ('Unhealthy', 503) if plan else ('OK', 200)
            return JsonResponse({'detail': detail}, status=status)

        return self.get_response(request)
