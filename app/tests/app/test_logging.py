"""Test the structlog configuration the app loads at startup."""

import io
import logging

import structlog
from django_structlog.middlewares import RequestMiddleware

from django.http import HttpResponse

from tests.factories.fakers import fake

# These read structlog's live configuration rather than importing
# `app.logging`, because importing it would load it whether or not the app
# does. pytest-structlog only swaps the configuration inside its `log` fixture.


def test_structlog_routes_through_stdlib_logging():
    assert isinstance(structlog.get_config()['logger_factory'], structlog.stdlib.LoggerFactory)


def test_loggers_are_not_cached_under_test():
    assert structlog.get_config()['cache_logger_on_first_use'] is False


def render_with_configured_chain(event, **fields):
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(processor=structlog.dev.ConsoleRenderer(colors=False)),
    )
    stdlib_logger = logging.getLogger(f'tests.app.test_logging.{fake.uuid4()}')
    stdlib_logger.addHandler(handler)
    stdlib_logger.setLevel(logging.INFO)
    stdlib_logger.propagate = False
    processors = structlog.get_config()['processors']

    structlog.wrap_logger(stdlib_logger, processors=processors).info(event, **fields)
    return stream.getvalue()


def test_configured_chain_renders_an_event():
    value = fake.word()

    output = render_with_configured_chain('hello', key=value)

    assert 'hello' in output
    assert f'key={value}' in output


def test_configured_chain_masks_credentials():
    password, token = fake.password(length=16), fake.sha256()

    output = render_with_configured_chain('signed in', password=password, access_token=token)

    assert password not in output
    assert token not in output
    assert '*** REDACTED ***' in output


def test_responses_carry_the_request_id(rf):
    middleware = RequestMiddleware(lambda _request: HttpResponse())

    response = middleware(rf.get('/'))

    assert response.has_header('X-Request-ID')
