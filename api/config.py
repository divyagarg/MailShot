import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))

env = os.getenv('HOSTENV') or 'development'

config_file = basedir + '/config/' + env + '.yml'

with open(config_file, 'r') as f:
    CONFIG = yaml.safe_load(f)


DATABASE_URL = CONFIG["mysql"]["connection"]
LOG_FILE = CONFIG["logfile"]
LOG_FILE_ERROR = CONFIG["errorlogfile"]

REDIS_HOST = CONFIG["redis"]["host"]
REDIS_PORT = CONFIG["redis"]["port"]
REDIS_DB = CONFIG["redis"]["db"]
REDIS_QUEUE = CONFIG["redis"]["queue"]
WORKER_THREAD_COUNT = CONFIG["email_worker_threads_count"]

AWS_ACCESS_KEY_ID = CONFIG["aws_access_key_id"]
AWS_SECRET_ACCESS_KEY = CONFIG["aws_secret_access_key"]
AWS_REGION = CONFIG["aws_region"]