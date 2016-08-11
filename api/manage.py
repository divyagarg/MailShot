from gevent.monkey import patch_all;

patch_all()
from app.log import setup_logging
import os
from app import create_app
from flask_script import Manager, Server
from app.src.sqlalchemydb import AlchemyDB
from app.log import setup_logging


basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv('HOSTENV') or 'development'
new_relic_cfg = basedir + '/config/' + env + '_newrelic.ini'

# import newrelic.agent
# newrelic.agent.initialize(new_relic_cfg)

flask_app = create_app()
manager = Manager(flask_app)
manager.add_command("runserver", Server(host="localhost", port=9048))
setup_logging()
AlchemyDB.init()
if __name__ == '__main__':
    manager.run()
