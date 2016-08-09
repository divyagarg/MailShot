import functools
import logging

import ujson
import uuid
from flask import Response, request, g

logger = logging.getLogger()


def json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        g.UUID = uuid.uuid4()
        logger.debug('START_CALL %s, Request_URL = %s ', g.UUID, str(request.url))
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