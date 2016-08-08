import logging
from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()


@api.route("/campaign", methods=["POST"])
@json
def create_campaign():
    return {"result": "success"}


@api.route("/campaign", methods=["GET"])
@json
def get_all_campaigns():
    return {"result": "success"}


@api.route("/campaign/<campaignid>", methods=["GET"])
@json
def get_campaigns_by_id():
    return {"result": "success"}


@api.route("/campaign/summary/<campaignid>", methods=["GET"])
@json
def get_campaigns_summary_by_id():
    return {"result": "success"}