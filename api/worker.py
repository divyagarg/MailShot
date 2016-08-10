import logging

from redis import Redis
from rq import Worker, Queue, Connection

from api.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_QUEUE

logger = logging.getLogger()

listen = [REDIS_QUEUE]
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)





# from api.manage import app as flask_app
from app.src.smtp import async_mail_sender
from app.src.campaign import Campaign
from app.src.sqlalchemydb import AlchemyDB

AlchemyDB.init()

async_mail_sender(Campaign(id=18))

# if __name__ == '__main__':
#     with Connection(redis_conn):
#         logger.debug("setting up redis")
#         worker = Worker(map(Queue, listen))
#         worker.work()