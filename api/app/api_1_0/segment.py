import logging

from app.api_1_0 import api
from app.decorator import json
from app.src.segment import Segment
from flask import g


logger = logging.getLogger()


@api.route("/segment", methods=["GET"])
@json
def get_segment():
    segment = Segment()
    try:
        segments = segment.get_all_segments()
    except Exception as exception:
        logger.error('%s Exception in getting all segments', g.UUID, str(exception), exc_info=True)
        raise exception
    else:
        return segments
