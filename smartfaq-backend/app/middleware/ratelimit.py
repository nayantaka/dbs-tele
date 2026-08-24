import time
import threading
from functools import wraps
from flask import request, abort

class _SlidingWindow:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self._hits = {}
        self._lock = threading.Lock()

    def allow(self, key):
        now = time.time()
        cutoff = now - self.window
        with self._lock:
            bucket = [t for t in self._hits.get(key, []) if t > cutoff]
            if len(bucket) >= self.limit:
                self._hits[key] = bucket
                return False
            bucket.append(now)
            self._hits[key] = bucket
            return True

def rate_limit(limit, window, key_func=None):
    limiter = _SlidingWindow(limit, window)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = key_func() if key_func else request.remote_addr
            if not limiter.allow(key):
                abort(429, description="too many requests, slow down")
            return fn(*args, **kwargs)
        return wrapper
    return decorator