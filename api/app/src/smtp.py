import logging
import segment

import gevent
from multiprocessing import JoinableQueue
from api.config import WORKER_THREAD_COUNT

num_worker_threads = 20


def async_mail_sender(campaign):
    campaign.load_details()
    email_list = campaign.get_email_list()
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
            #send email
            pass
        finally:
            queue.task_done()