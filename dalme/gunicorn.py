"""Configure logging for gunicorn."""
import time


def post_fork(server, worker):  # noqa: ARG001
    pass


def pre_request(worker, req):
    req._gunicorn_start_time = time.time()  # noqa: SLF001
    worker.log.info('[begin] %s %s', req.method, req.path)


def post_request(worker, req, environ, resp):  # noqa: ARG001
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
