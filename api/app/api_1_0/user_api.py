import logging
from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()


@api.route("/campaign/unsubscribe/<usertrackerid>", methods=["POST"])
@json
def unsubscribe():
    return {"result": "success"}


@api.route("/campaign/<usertrackerid>/id.png", methods=["POST"])
@json
def track_open():
    return {"result": "success"}


@api.route("/campaign/<redirectid>", methods=["GET"])
@json
def track_click():
    return {"result": "success"}