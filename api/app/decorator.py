import functools
import ujson

from flask import Response


def json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        rv = ujson.dumps(rv)
        return Response(rv, mimetype='application/json')
    return wrapped