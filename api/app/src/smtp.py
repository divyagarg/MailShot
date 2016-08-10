
import logging
import uuid

import gevent
from gevent.queue import JoinableQueue
import boto.ses
from bs4 import BeautifulSoup

from api.config import WORKER_THREAD_COUNT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, SELF_URL, MAIL_SENDER
from segment import Segment
from template import Template
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
        print "here"
        while True:
            email, contactid = queue.get()
            try:
                user_tracker_id = uuid.uuid4().hex
                soup = BeautifulSoup(template.varaint_list[0].html_body)
                logger.debug(soup)
                link_map = dict()
                for link in soup.find_all("a"):
                    print link
                    if not link_map.get(link['href']):
                        linkid = uuid.uuid4().hex
                        link_map[link["href"]] = linkid
                        link["href"] = SELF_URL +"/link/"+linkid
                user.insert_open_tracking_details(user_tracker_id=user_tracker_id, campaignid=campaign.id, contactid=contactid, variantid=template.varaint_list[0].id)
                user.insert_click_tracking_details(user_tracker_id=user_tracker_id, link_map=link_map)
                open_link = SELF_URL + "/campaign/" + user_tracker_id + "id.png"
                new_tag = soup.new_tag("img", href=open_link)
                soup.append(new_tag)
                unsubscribe_link = SELF_URL + "/campaign/unsubscribe/" + user_tracker_id
                new_tag = soup.new_tag("a", href=unsubscribe_link)
                new_tag.string = "Unsubscribe"
                soup.append(new_tag)
                # soup.append("<img src='%s'></img>" % open_link)
                # unsubscribe_link = SELF_URL + "/campaign/unsubscribe/" + user_tracker_id
                # soup.append("<a href='%s' target='_blank'><span style='color:#0055b8'>Unsubscribe</span></a>"%unsubscribe_link)
                print str(soup)
                send_mail(MAIL_SENDER, template.varaint_list[0].subject, str(soup),email)
            finally:
                queue.task_done()
    for i in range(0, 1):
        gevent.spawn(email_sender_worker,campaign, template)
    for cont in contact_list:
        queue.put((cont["email"], cont["contactid"]))
    queue.join()


def send_mail(sender, subject, body, to):
    conn = boto.ses.connect_to_region(AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    conn.send_email(sender, subject, body, to)