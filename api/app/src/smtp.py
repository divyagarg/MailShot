from multiprocessing import JoinableQueue

import gevent
import boto.ses

from api.config import WORKER_THREAD_COUNT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from segment import Segment


def async_mail_sender(campaign):
    campaign.load_details()
    email_list = Segment.get_email_list(campaign.segment_list)
    queue = JoinableQueue()
    for email in email_list:
        queue.put(email)
    for i in range(WORKER_THREAD_COUNT):
        gevent.spawn(email_sender_worker, queue, campaign.mail)
    queue.join()


def email_sender_worker(queue, mail):
    while True:
        item = queue.get()
        try:
            user_tracker_id = generate_user_tarcker_id()

            pass
        finally:
            queue.task_done()


def generate_user_tarcker_id():
    pass


def generate_link_id():
    pass


def send_mail(sender, subject, body, to):
    conn = boto.ses.connect_to_region(AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    conn.send_email(sender, subject, body, to)