"""Test the structlog configuration the app loads at startup."""

import io
import logging

import structlog
from django_structlog.middlewares import RequestMiddleware

from django.http import HttpResponse

# These read structlog's live configuration rather than importing
# `app.logging`, because importing it would load it whether or not the app
# does. pytest-structlog only swaps the configuration inside its `log` fixture.


def test_structlog_routes_through_stdlib_logging():
    assert isinstance(structlog.get_config()['logger_factory'], structlog.stdlib.LoggerFactory)


def test_loggers_are_not_cached_under_test():
    assert structlog.get_config()['cache_logger_on_first_use'] is False


def test_configured_chain_renders_an_event():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(processor=structlog.dev.ConsoleRenderer(colors=False)),
    )
    stdlib_logger = logging.getLogger('tests.app.test_logging')
    stdlib_logger.addHandler(handler)
    stdlib_logger.setLevel(logging.INFO)
    stdlib_logger.propagate = False
    processors = structlog.get_config()['processors']

    structlog.wrap_logger(stdlib_logger, processors=processors).info('hello', key='value')

    assert 'hello' in stream.getvalue()
    assert 'key=value' in stream.getvalue()


def test_responses_carry_the_request_id(rf):
    middleware = RequestMiddleware(lambda _request: HttpResponse())

    response = middleware(rf.get('/'))

    assert response.has_header('X-Request-ID')
