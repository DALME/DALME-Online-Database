"""Configure logging for gunicorn."""

from __future__ import annotations

import time
import typing as T  # noqa: N812

from gunicorn.http.message import Request
from gunicorn.http.wsgi import Response
from gunicorn.workers.base import Worker


def post_fork(server, worker: Worker):
    """Call just after a worker has been forked.

    https://docs.gunicorn.org/en/stable/settings.html#post-fork

    """


def pre_request(worker: Worker, req: Request) -> None:
    """Call before a worker processes a request.

    https://docs.gunicorn.org/en/stable/settings.html#pre-request

    """
    req._gunicorn_start_time = time.time()  # noqa: SLF001
    worker.log.info('[begin] %s %s', req.method, req.path)


def post_request(
    worker: Worker,
    req: Request,
    environ: dict[str, T.Any],  # noqa: ARG001
    resp: Response,
) -> None:
    """Call after a worker processes a request.

    https://docs.gunicorn.org/en/stable/settings.html#post-request

    """
    duration = time.time() - req._gunicorn_start_time  # noqa: SLF001
    trace_id = next(iter([v for k, v in req.headers if k == 'X-B3-TRACEID']), None)
    worker.log.info(
        '[status=%s] %s %s duration=%s traceID=%s',
        resp.status,
        req.method,
        req.path,
        duration,
        trace_id,
    )
