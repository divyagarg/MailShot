import functools
import logging

import ujson
from flask import Response

logger = logging.getLogger()


def json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        resp = dict()
        resp["data"] = rv
        if isinstance(rv, Exception):
            resp["status"] = False
        else:
            resp["status"] = True
        logger.debug(resp)
        resp = ujson.dumps(resp)
        return Response(resp, mimetype='application/json')

    return wrapped