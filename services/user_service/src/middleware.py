import time

from flask import Request, Response
from flask_http_middleware import BaseHTTPMiddleware
from opentelemetry import metrics


class RequestTimingMiddleware(BaseHTTPMiddleware):
    def __init__(self):
        super().__init__()
        meter = metrics.get_meter(__name__)
        self.request_time = meter.create_histogram("http.server.request.duration", unit="ms")

    def dispatch(self, request: Request, call_next):
        start_time_seconds = time.perf_counter()
        response: Response = call_next(request)
        end_time_seconds = time.perf_counter()

        attributes = {
            "http.request.method": request.method,
            "http.route": request.path,
            "http.request.scheme": request.scheme,
            "http.response.status_code": response.status_code,
        }
        duration_seconds = end_time_seconds - start_time_seconds
        duration_milliseconds = duration_seconds * 1000

        self.request_time.record(duration_milliseconds, attributes)
        return response
