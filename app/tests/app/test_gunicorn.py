"""Tests for gunicorn hooks in the app module."""

import time

from app import gunicorn


class DummyLog:
    def __init__(self):
        self.calls = []

    def info(self, msg, *args):
        self.calls.append((msg, args))


class DummyWorker:
    def __init__(self):
        self.log = DummyLog()


class DummyRequest:
    def __init__(self, method='GET', path='/test', headers=None):
        self.method = method
        self.path = path
        self.headers = headers or []
        # _gunicorn_start_time will be set by pre_request


class DummyResponse:
    def __init__(self, status='200 OK'):
        self.status = status


def test_pre_request_sets_start_time_and_logs():
    worker = DummyWorker()
    req = DummyRequest()
    before = time.time()
    gunicorn.pre_request(worker, req)
    after = time.time()
    assert hasattr(req, '_gunicorn_start_time')
    assert before <= req._gunicorn_start_time <= after  # noqa: SLF001
    assert worker.log.calls
    msg, args = worker.log.calls[0]
    assert msg == '[begin] %s %s'
    assert args == (req.method, req.path)


def test_post_request_logs_status_and_duration():
    worker = DummyWorker()
    req = DummyRequest(headers=[('X-B3-TRACEID', 'abc123'), ('Other', 'val')])
    req.method = 'POST'
    req.path = '/foo'
    req._gunicorn_start_time = time.time() - 1.5  # noqa: SLF001
    resp = DummyResponse(status='404 NOT FOUND')
    environ = {}
    gunicorn.post_request(worker, req, environ, resp)
    assert worker.log.calls
    msg, args = worker.log.calls[0]
    assert msg == '[status=%s] %s %s duration=%s traceID=%s'
    assert args[0] == resp.status
    assert args[1] == req.method
    assert args[2] == req.path
    assert isinstance(args[3], float)
    assert args[3] >= 1.5  # noqa: PLR2004
    assert args[4] == 'abc123'


def test_post_request_logs_none_trace_id_when_missing():
    worker = DummyWorker()
    req = DummyRequest(headers=[('Other', 'val')])
    req._gunicorn_start_time = time.time() - 0.5  # noqa: SLF001
    resp = DummyResponse(status='200 OK')
    environ = {}
    gunicorn.post_request(worker, req, environ, resp)
    msg, args = worker.log.calls[0]
    assert args[4] is None


def test_post_fork_is_noop():
    worker = DummyWorker()
    server = object()
    assert gunicorn.post_fork(server, worker) is None
