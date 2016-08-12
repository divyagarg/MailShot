import logging
from app.src.notification import process_notification

from flask import request, g
from webargs import fields
from marshmallow import validate
from webargs.flaskparser import parser

from app.api_1_0 import api
from app.decorator import json


__author__ = 'divyagarg'


logger = logging.getLogger()

notification_args = {
    "Type": fields.Str(required = True),
    "MessageId": fields.Str(required = True),
    "TopicArn": fields.Str(required = True),
    "Timestamp": fields.Str(required = True),
    "Message": fields.Nested({
        "notificationType": fields.Str(required=True),
        "mail": fields.Nested({
            "timestamp":fields.DateTime(required=True),
            "messageId": fields.Str(required=True),
            "source": fields.Str(required=True, validate=validate.Email()),
            "sourceArn": fields.Str(required=True),
            "sendingAccountId": fields.Int(required=True),
            "destination": fields.List(fields.Str(validate=validate.Email()), required=True),
            "headersTruncated": fields.Bool(required=False)
        }),
        "bounce": fields.Nested({
            "bounceType": fields.Str(required=True),
            "bounceSubType": fields.Str(required=True),
            "bouncedRecipients": fields.DelimitedList(
                            fields.Nested(
                                {
                                    "emailAddress": fields.Str(required=True, validate=validate.Email()),
                                    "action": fields.Str(required=False),
                                    "status": fields.Str(required=False),
                                    "diagnosticCode": fields.Str(required=False)
                                }
                            )
                        ),
            "timestamp":fields.DateTime(required=True),
            "feedbackId": fields.Int(required=True),
            "reportingMTA": fields.Str(required=False),
        }),
        "complaint": fields.Nested(
            {
                "userAgent":fields.Str(required=False),
                "complainedRecipients":fields.DelimitedList(
                      fields.Nested(
                      {
                         "emailAddress":fields.Str(required=True, validate=validate.Email())
                      })
                ),
                "complaintFeedbackType":fields.Str(required=False),
                "arrivalDate":fields.DateTime(required=False),
                "timestamp":fields.DateTime(required=True),
                "feedbackId":fields.Str(required=True)
                }
        ),
        "delivery": fields.Nested(
            {
               "timestamp":fields.DateTime(required=False),
               "processingTimeMillis":fields.Int(required=True),
               "recipients": fields.DelimitedList(fields.Str(validate=validate.Email()), required=True),
               "smtpResponse":fields.Str(required=True),
               "reportingMTA":fields.Str(required=True)
            }
        )
    })
}


@api.route("/notification", methods=["POST"])
@json
def read_notification():
    try:
        args = parser.parse(notification_args, request)
        logger.debug(args)
        result = process_notification(args)
    except Exception as exception:
        logger.error("%s Exception in parsing notification %s", g.UUID, args)
        logger.error(exception)
        raise exception
    return result



