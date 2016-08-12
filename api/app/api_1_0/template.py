import logging

from app.api_1_0 import api
from app.decorator import json

from app.src.sqlalchemydb import AlchemyDB
from app.src.template import Template
from app.src.variant import Variant
from flask import request
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
    template = Template(args.get('name'), args.get('userid'))
    template_id = template.save_template()
    return template_id


@api.route("/template/<templateid>/variant", methods=["POST"])
@json
def create_template_variant(templateid):
    if templateid:
        args = parser.parse(variant_args, request)
        variant = Variant(variant_name= args.get('variant_name'), html_body = args.get('html'), template_id = templateid, subject = args.get('subject'))
        variant_id = variant.save_variant()
        return variant_id


@api.route('/test', methods=['GET'])
@json
def test():
    result = {"success": True}
    return result






