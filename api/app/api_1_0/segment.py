import logging
from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()


@api.route("/segment", methods=["GET"])
@json
def get_segment():
    return {"result": "success"}