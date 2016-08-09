import logging
import uuid
from app.api_1_0 import api
from app.decorator import json
from app.src.models import Segment
from flask import g, request


logger = logging.getLogger()


@api.route("/segment", methods=["GET"])
@json
def get_segment():
    g.UUID = uuid.uuid4()
    logger.info('START_CALL= %s Request_url = %s', g.UUID, str(request.url))
    segment = Segment()
    try:
        segments = segment.get_all_segments()
    except Exception as exception:
       logger.error('%s Exception in getting all segments', g.UUID, str(exception), exc_info=True)
       return {"result": "Failure", "message": str(exception)}
    else:
        logger.info('END_CALL=%s segments = %s', g.UUID, segments)
        return {"result": "success", "data": segments}
