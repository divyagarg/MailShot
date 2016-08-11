import logging


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    errorhandler = logging.StreamHandler()
    errorhandler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s-[in %(pathname)s:%(lineno)d]- %(message)s")
    handler.setFormatter(formatter)
    errorhandler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(errorhandler)