import logging
from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()


@api.route("/template", methods=["POST"])
@json
def create_template():
    return {"result": "success"}


@api.route("/template/<templateid>/variant", methods=["POST"])
@json
def create_template_variant():
    return {"result": "success"}







