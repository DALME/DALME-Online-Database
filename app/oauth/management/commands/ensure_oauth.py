"""Management command to ensure an oauth application is registered."""

import io

import structlog

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from oauth.models import Application

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the ensure_oauth command."""

    CALLBACK_URL = 'api/oauth/authorize/callback/'
    DEFAULTS = {
        'algorithm': 'RS256',
        'authorization_grant_type': 'authorization-code',
        'client_type': 'confidential',
        'name': 'IDA',
        'skip_authorization': True,
    }

    help = 'Create an oauth application.'

    @property
    def success(self):
        """The expected success message from the sub-command."""
        return f'New application {self.DEFAULTS["name"]} created successfully'

    def handle(self, *args, **options):  # noqa: ARG002
        """Create an oauth application record."""
        client_id = settings.OAUTH_CLIENT_ID
        client_secret = settings.OAUTH_CLIENT_SECRET

        domains = []
        for tenant in settings.TENANTS():
            domains.append(tenant.value.domain)
            for additional_domain in tenant.value.additional_domains:
                domains.append(additional_domain)

        domains = [f'http://{domain}:8000' if settings.IS_DEV else f'https://{domain}' for domain in domains]

        redirect_uris = [f'{domain}/{self.CALLBACK_URL}' for domain in domains]
        post_logout_redirect_uris = [f'{domain}/' for domain in domains]

        try:
            application = Application.objects.get(client_id=client_id)
        except Application.DoesNotExist:
            kwargs = {
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uris': ' '.join(redirect_uris),
                'post_logout_redirect_uris': ' '.join(post_logout_redirect_uris),
                **options,
                **self.DEFAULTS,
            }
            authorization_grant_type = kwargs.pop('authorization_grant_type')
            client_type = kwargs.pop('client_type')

            # Here when we call the subcommand we have to capture stdout to
            # determine success or otherwise because doing so doesn't return an
            # exit code or anything else useful.
            with io.StringIO() as out:
                call_command('createapplication', client_type, authorization_grant_type, stdout=out, **kwargs)
                output = out.getvalue()

                if self.success in output:
                    # The command doesn't seem to handle setting the
                    # 'allowed_origins' field so let's do it ourselves here.
                    application = Application.objects.get(client_id=client_id)
                    application.allowed_origins = ' '.join(domains)
                    application.save()

                    logger.info('Created oauth application with client_id: %s', client_id=client_id)
                else:
                    logger.error(output)  # noqa: TRY400
                    logger.error('Failed to create oauth application')  # noqa: TRY400
        else:
            # We only support updating the values that are injected by a deploy
            # environment here for rotation purposes. For anything else let's
            # just speculate that some other kind of intervention will happen.
            # This is not meant to be an all-purpose create application command.
            application.client_id = client_id
            application.client_secret = client_secret
            application.save()
            logger.info('Refreshed existing oauth application with client_id: %s', client_id=client_id)
