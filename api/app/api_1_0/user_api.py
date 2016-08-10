import logging
import uuid

from flask import send_file, g
from app.api_1_0 import api
from app.decorator import json
from app.src.mailtrack import MailTrack

logger = logging.getLogger()


@api.route("/campaign/unsubscribe/<usertrackerid>", methods=["POST"])
@json
def unsubscribe():
    return {"result": "success"}


@api.route("/campaign/<usertrackerid>/id.png", methods=["GET"])
def track_open(usertrackerid):
    g.UUID = uuid.uuid4()
    if usertrackerid:
        try:
            mailtrack = MailTrack(user_tracker_id=usertrackerid)
            result = mailtrack.update_open_status()
        except Exception as exception:
            logger.error('%s Exception in getting Campaign', g.UUID,
                         str(exception), exc_info=True)
            raise exception
        if result:
            return send_file('static/1.png')


@api.route("/campaign/<redirectid>", methods=["GET"])
@json
def track_click():
    return {"result": "success"}
