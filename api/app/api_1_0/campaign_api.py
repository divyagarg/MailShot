import logging

from flask import request
from webargs import fields, validate
from webargs.flaskparser import parser

from app.api_1_0 import api
from app.decorator import json
from app.src.campaign import Campaign

logger = logging.getLogger()


@api.route("/campaign", methods=["POST"])
@json
def create_campaign():
    args = {
        'name': fields.Str(required=True),
        'send_time': fields.Str(require=True),
        'categoryid': fields.Int(required=False),
        'templateid': fields.Int(required=True)
    }

    request_args = parser.parse(args, request)
    campaign = Campaign(name=request_args.get('name'), send_time=request_args.get('send_time'),
                        categoryid=request_args.get('categoryid'), templateid=request_args.get('templateid'))
    campaign.save_campaign()
    return campaign.to_json()


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