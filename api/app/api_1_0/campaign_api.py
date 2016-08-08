import logging
from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()

@api.route("/test", methods=["GET"])
@json
def get_attribute_list():
    return {"result": "success"}