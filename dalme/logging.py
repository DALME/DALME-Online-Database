"""Configure logging settings."""
import os

import structlog
from django_structlog import signals
from django_structlog.middlewares.request import get_request_header
from django_structlog.signals import bind_extra_request_metadata
from rest_framework_simplejwt.tokens import UntypedToken

from django.dispatch import receiver

BASE_PROCESSORS = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.TimeStamper(fmt='iso'),
    structlog.processors.UnicodeDecoder(),
    structlog.processors.format_exc_info,
]

# Must be last so append it here leaving us open to dynamically extend the
# basic processing chain.
PROCESSORS = [
    *BASE_PROCESSORS,
    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
]

structlog.configure(
    processors=PROCESSORS,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

@receiver(signals.update_failure_response)
@receiver(signals.bind_extra_request_finished_metadata)
def add_request_id_to_error_response(response, logger, **kwargs):  # noqa: ARG001
    context = structlog.contextvars.get_merged_contextvars(logger)
    response['X-Request-ID'] = context['request_id']


@receiver(bind_extra_request_metadata)
def bind_token_user_id(request, logger, **kwargs):  # noqa: ARG001
    try:
        header = request.META.get('HTTP_AUTHORIZATION')
        if header:
            raw_token = header.split()[1]
            token = UntypedToken(raw_token)
            user_id = token['user_id']
            structlog.contextvars.bind_contextvars(user_id=user_id)
    except Exception:  # noqa: BLE001
        pass


if os.environ['ENV'] in {'staging', 'production'}:
    @receiver(signals.bind_extra_request_metadata)
    def bind_trace_id(request, logger, **kwargs):  # noqa: ARG001
        trace_id = get_request_header(
             request, 'x-amzn-trace-id', 'HTTP_X_AMZN_TRACE_ID',
        )
        if trace_id:
            structlog.contextvars.bind_contextvars(trace_id=trace_id)
