"""Management command to publish scheduled CMS pages.

We override the built-in Wagtail management command so we can callback to AWS
step functions and manage ECS task flows.

"""
import os

import boto3
import structlog
from wagtail.management.commands.publish_scheduled import Command as PublishScheduled

logger = structlog.get_logger(__name__)


class Command(PublishScheduled):
    """Override the publish scheduled command."""

    help = 'Publish any CMS pages due to go live.'  # noqa: A003

    def handle(self, *args, **options):
        super().handle(*args, **options)
        logger.info('Scheduled pages have been published')
        if token := os.environ.get('AWS_SFN_TASK_TOKEN'):
            stfn = boto3.client('stepfunctions')
            stfn.send_task_success(taskToken=token, output='{"Status": "Success"}')
