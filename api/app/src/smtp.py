import logging
import uuid

import gevent
from gevent.queue import JoinableQueue
import boto.ses
from bs4 import BeautifulSoup

from config import WORKER_THREAD_COUNT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, SELF_URL, MAIL_SENDER
from segment import Segment
from template import Template
from contactinfo import ContactInfo
import user


logger = logging.getLogger()


def async_mail_sender(campaign):
    logger.debug("in async mail sender")
    logger.debug(campaign)
    campaign.find_campaign(Id=campaign.id)
    segment_list = [s.id for s in campaign.segment_list]
    contact_list = Segment.get_contact_list(segment_list)
    logger.debug(contact_list)
    queue = JoinableQueue()
    template = Template(campaign.templateid)
    template.get_template()

    def email_sender_worker(campaign, template):
        while True:
            email, contactid = queue.get()
            try:
                user_tracker_id, link_map,soup = prepare_mail(template.varaint_list[0].html_body)
                messageid = send_mail(MAIL_SENDER, template.varaint_list[0].subject, str(soup), email)
                if messageid is not None:
                    user.insert_open_tracking_details(user_tracker_id=user_tracker_id, campaignid=campaign.id,
                                                      contactid=contactid, variantid=template.varaint_list[0].id, messageid=messageid)
                    user.insert_click_tracking_details(user_tracker_id=user_tracker_id, link_map=link_map)
            finally:
                queue.task_done()

    for i in range(0, WORKER_THREAD_COUNT):
        gevent.spawn(email_sender_worker, campaign, template)
    for cont in contact_list:
        queue.put((cont["email"], cont["contactid"]))
    queue.join()


def prepare_mail(html_body):
    user_tracker_id = uuid.uuid4().hex
    soup = BeautifulSoup(html_body)
    logger.debug(soup)
    link_map = dict()
    for link in soup.find_all("a"):
        if not link_map.get(link['href']):
            linkid = uuid.uuid4().hex
            link_map[link["href"]] = linkid
            link["href"] = SELF_URL + "/link/" + linkid
    open_link = SELF_URL + "/campaign/" + user_tracker_id + "/id.png"
    new_tag = soup.new_tag("img", src=open_link)
    soup.append(new_tag)
    unsubscribe_link = SELF_URL + "/campaign/unsubscribe/" + user_tracker_id
    new_tag = soup.new_tag("a", href=unsubscribe_link)
    new_tag.string = "Unsubscribe"
    soup.append(new_tag)
    # soup.append("<a href='%s' target='_blank'><span style='color:#0055b8'>Unsubscribe</span></a>"%unsubscribe_link)
    logger.debug(soup)
    return user_tracker_id, link_map, soup


def send_mail(sender, subject, body, to):
    try:
        conn = boto.ses.connect_to_region(AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        resp = conn.send_email(sender, subject, body, to, format="html")
        messageid = resp.get("SendEmailResponse").get('SendEmailResult').get("MessageId")
        logger.debug(resp)
    except Exception as e:
        logger.exception(e)
    else:
        return messageid


def send_test_mail(templateid, email):
    template = Template(templateid)
    template.get_template()
    # contact = ContactInfo.find_contact_by_email(email)
    # if not contact:
    #      Contact.save
    user_tracker_id, link_map, soup = prepare_mail(template.varaint_list[0].html_body)
    resp = send_mail(MAIL_SENDER, template.varaint_list[0].subject, str(soup), email)
    logger.debug(resp)
