import logging

logger = logging.getLogger()


class MailShotException(Exception):
    """
    Handles user defined exception and process that for action
    error: contains error string
    payload : any name value custom object to be attached in error
    """
    status_code = 200

    def __init__(self, error, status_code=None, **args):
        Exception.__init__(self)
        self.error = error
        logger.error(self.error, exc_info=True)
        if status_code is not None:
            self.status_code = status_code
        self.payload = args

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        rv['status'] = False
        return rv


