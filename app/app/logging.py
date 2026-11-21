"""Configure structlog and its request signals. Loaded by `app.apps`."""

import structlog
from django_structlog import signals
from django_structlog.middlewares.request import get_request_header

from django.conf import settings
from django.dispatch import receiver

REDACTED = '*** REDACTED ***'
CREDENTIAL_KEYS = frozenset(
    {
        'access_token',
        'authorization',
        'client_secret',
        'code_verifier',
        'password',
        'refresh_token',
        'secret',
        'token',
    }
)


def redact_credentials(_logger, _method_name, event_dict):
    """Mask the value of any event key that may carry a credential."""
    for key in event_dict:
        if key.lower() in CREDENTIAL_KEYS:
            event_dict[key] = REDACTED
    return event_dict


BASE_PROCESSORS = [
    structlog.contextvars.merge_contextvars,
    redact_credentials,
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
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
    # A cached logger keeps the chain it was first used with, which defeats
    # pytest-structlog's capture for every later test, so cache only in deploys.
    cache_logger_on_first_use=not settings.IS_DEV,
)


@receiver(signals.update_failure_response)
@receiver(signals.bind_extra_request_finished_metadata)
def add_request_id_to_error_response(response, logger, **kwargs):  # noqa: ARG001
    context = structlog.contextvars.get_merged_contextvars(logger)
    response['X-Request-ID'] = context['request_id']


if not settings.IS_DEV:

    @receiver(signals.bind_extra_request_metadata)
    def bind_trace_id(request, logger, **kwargs):  # noqa: ARG001
        trace_id = get_request_header(
            request,
            'x-amzn-trace-id',
            'HTTP_X_AMZN_TRACE_ID',
        )
        if trace_id:
            structlog.contextvars.bind_contextvars(trace_id=trace_id)
