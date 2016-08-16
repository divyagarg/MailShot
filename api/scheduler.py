import logging

from redis import Redis
from rq import Connection
from rq_scheduler import Scheduler
from app.src.sqlalchemydb import AlchemyDB
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_QUEUE

logger = logging.getLogger()

listen = [REDIS_QUEUE]
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s-[in %(pathname)s:%(lineno)d]- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# from api.manage import flask_app

AlchemyDB.init()

if __name__ == '__main__':
    with Connection(redis_conn):
        logger.debug("setting up redis")
        scheduler = Scheduler()
        scheduler.run()