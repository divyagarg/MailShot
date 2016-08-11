import logging
import uuid
from app.src.contactinfo import ContactInfo

from flask import send_file, g, render_template
from app.api_1_0 import api
from app.decorator import json
from app.src.mailtrack import MailTrack

logger = logging.getLogger()


@api.route("/campaign/unsubscribe/<usertrackerid>", methods=["GET"])
def unsubscribe(usertrackerid):
    g.UUID = uuid.uuid4()
    if usertrackerid:
        try:
            mailtrack = MailTrack(user_tracker_id=usertrackerid)
            result = mailtrack.update_unsubscription_status()
            contact = ContactInfo(contactId = mailtrack.contactId)
            contact.getContact()
        except Exception as exception:
            logger.error('%s Exception in getting Campaign', g.UUID,
                         str(exception), exc_info=True)
            raise exception
        if result:
            response = render_template('OptOut.html', email = contact.email)
            return response


@api.route("/campaign/<usertrackerid>/id.png", methods=["GET"])
def track_open(usertrackerid):
    g.UUID = uuid.uuid4()
    if usertrackerid:
        try:
            mail_track = MailTrack(user_tracker_id=usertrackerid)
            result = mail_track.update_open_status()
        except Exception as exception:
            logger.error('%s Exception in getting Campaign', g.UUID,
                         str(exception), exc_info=True)
            raise exception
        if result:
            response = send_file('static/1.png')
            response.cache_control.no_cache = True
            return response


@api.route("/campaign/<redirectid>", methods=["GET"])
@json
def track_click():
    return {"result": "success"}


