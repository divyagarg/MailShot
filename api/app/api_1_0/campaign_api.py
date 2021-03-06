import logging

from app.src.campaignsummary import CampaignSummary
from webargs import fields
from webargs.flaskparser import parser
from app.api_1_0 import api
from app.src.campaign import Campaign
from app.decorator import json
from flask import request, g
from app.src.smtp import send_test_mail

logger = logging.getLogger()


@api.route("/campaign", methods=["POST"])
@json
def create_campaign():
    args = {
        'name': fields.Str(required=True),
        'send_time': fields.Str(require=True),
        'categoryid': fields.Int(required=False),
        'templateid': fields.Int(required=True),
        'segment_list': fields.List(fields.Int(), required=True)
    }

    request_args = parser.parse(args, request)
    logger.debug(request_args)
    campaign = Campaign(name=request_args.get('name'),
                        send_time=request_args.get('send_time'),
                        categoryid=request_args.get('categoryid'),
                        templateid=request_args.get('templateid'),
                        segment_list=request_args.get('segment_list'))
    campaign.save_campaign()
    return campaign.to_json()


@api.route("/campaign", methods=["GET"])
@json
def get_all_campaigns():

    campaign_query_param = {
    "limit": fields.Int(required=True),
    "offset": fields.Int(required=True)

    }
    args = parser.parse(campaign_query_param, request)
    campaign = Campaign()
    try:
        campaigns = campaign.get_campaigns_list(args.get('limit'),
                                                args.get('offset'))
    except Exception as exception:
        logger.error('%s Exception in getting Campaigns', g.UUID,
                     str(exception), exc_info=True)
        raise exception
    else:
        return campaigns


@api.route("/campaign/<campaignid>", methods=["GET"])
@json
def get_campaigns_by_id(campaignid):
    if campaignid:
        campaign = Campaign(id=campaignid)
        try:
            result = campaign.find_campaign(Id=campaignid)
            logger.debug(campaign)
        except Exception as exception:
            logger.error(g.UUID)
            logger.exception(exception)
            raise exception
        if result:
            return campaign.to_json()


@api.route("/campaign/summary/<campaignid>", methods=["GET"])
@json
def get_campaigns_summary_by_id(campaignid):
    if campaignid:
        campaignSummary = CampaignSummary(campaign_id=campaignid)
        try:
            campaignSummaryResult = campaignSummary.get_campaign_summary()
            logger.debug(campaignSummary)
        except Exception as exception:
            logger.error('%s Exception in getting Campaign', g.UUID,
                         str(exception), exc_info=True)
            raise exception
        if campaignSummaryResult:
            return campaignSummary.to_json()


@api.route("/campaign/sendtest", methods=["POST"])
@json
def sendtestmail():
    request_args = {
                        "templateid": fields.Int(required=True),
                        "variantid": fields.Int(required=False),
                        "email": fields.Str(required=True)
                    }
    args = parser.parse(request_args, request)
    campaign = Campaign()
    try:
       send_test_mail(args.get('templateid'), args.get('email'))
    except Exception as exception:
        logger.error('%s Exception in getting Campaigns'%(exception))
        raise exception
    else:
        return {"result": "success"}

