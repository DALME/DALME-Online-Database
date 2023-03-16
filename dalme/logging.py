"""Configure logger settings."""
import os

import structlog

# KEY_ORDER = ["event", "tenant", "request_id"]

processors = [
    structlog.contextvars.merge_contextvars,
    # structlog.processors.KeyValueRenderer(
    #     key_order=KEY_ORDER,
    # ),
    structlog.stdlib.filter_by_level,
    structlog.processors.TimeStamper(fmt='iso'),
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    # structlog.processors.CallsiteParameterAdder(
    #     {
    #         structlog.processors.CallsiteParameter.FILENAME,
    #         structlog.processors.CallsiteParameter.FUNC_NAME,
    #         structlog.processors.CallsiteParameter.LINENO,
    #     },
    # ),
]

# if os.environ['ENV'] in {'staging', 'production'}:
#     processors = [*processors, structlog.processors.dict_tracebacks]
# processors = [*processors, structlog.stdlib.ProcessorFormatter.wrap_for_formatter]

structlog.configure(
    processors=processors,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


logger = structlog.get_logger(__name__)


class GunicornLogger:
    """Integrate structlog into the gunicorn logger.

    https://github.com/benoitc/gunicorn/blob/master/gunicorn/glogging.py to

    """

    def __init__(self, cfg):
        """Initialize a GunicornLogger object."""
        self._error_logger = structlog.get_logger('gunicorn.error')
        self._access_logger = structlog.get_logger('gunicorn.access')
        self.cfg = cfg

    def critical(self, msg, *args, **kwargs):
        """Log at critical level."""
        self._error_logger.error(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Log at error level."""
        self._error_logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Log at warning level."""
        self._error_logger.warning(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Log at info level."""
        self._error_logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Log at debug level."""
        self._error_logger.debug(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """Log at exception level."""
        self._error_logger.exception(msg, *args, **kwargs)

    def log(self, lvl: str, msg, *args, **kwargs):
        """Emit a log."""
        self._error_logger.log(lvl, msg, *args, **kwargs)

    def access(self, resp, req, environ, request_time):  # noqa: ARG002
        """Override the access method."""
        status = resp.status
        if isinstance(status, str):
            status = status.split(None, 1)[0]

        self._access_logger.info(
            'request',
            method=environ['REQUEST_METHOD'],
            request_uri=environ['RAW_URI'],
            status=status,
            response_length=getattr(resp, 'sent', None),
            request_time_seconds='%d.%06d'
            % (request_time.seconds, request_time.microseconds),
            pid='<%s>' % os.getpid(),
        )

    def reopen_files(self):
        """Stub out the reopen_files method."""
        # We don't support files here.

    def close_on_exec(self):
        """Stub out the close_on_exec method."""
        # We don't support files here.
