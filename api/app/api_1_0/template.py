import logging
import uuid

from app.api_1_0 import api
from app.decorator import json
from app.errors import MailShotException
from app.src.models import Template, Variant
from app.src.sqlalchemydb import AlchemyDB
from flask import g, request
from webargs import fields
from webargs.flaskparser import parser

logger = logging.getLogger()

@api.before_app_first_request
def before_app_first_request():
    AlchemyDB.init()

template_args = {
                 "name": fields.Str(required=True),
                 "userid": fields.Str(required=True)
                 }

variant_args = {
    "variant_name": fields.Str(required=True),
    "html": fields.Str(required=True),
    "subject": fields.Str(required=True)
}


@api.route("/template", methods=["POST"])
@json
def create_template():
    args = parser.parse(template_args, request)
    g.UUID = uuid.uuid4()
    logger.info('START_CALL= %s Request_url = %s, arguments = %s', g.UUID, str(request.url), args)
    template = Template(args.get('name'), args.get('userid'))
    result = template.save_template()
    if result:
        logger.info('END_CALL=%s', g.UUID)
        return {"result": "success"}
    return {"result": "Failure"}




@api.route("/template/<templateid>/variant", methods=["POST"])
@json
def create_template_variant(templateid):
    if templateid:
        args = parser.parse(variant_args, request)
        g.UUID = uuid.uuid4()
        logger.info('START_CALL= %s Request_url = %s, arguments = %s', g.UUID, str(request.url), args)
        variant = Variant(args.get('variant_name'), args.get('html'), templateid, args.get('subject'))
        try:
            result = variant.save_variant()
            if result is True:
                logger.info('END_CALL=%s', g.UUID)
                return {"result": "success"}
            else:
                return {"result": "Failure"}
        except MailShotException as mse:
            return {"result": mse.status_code}






@api.route('/test', methods=['GET'])
@json
def test():
	logger.info("Getting call for test function with request data %s", request.data)
	result = {"success": True}
	return result






