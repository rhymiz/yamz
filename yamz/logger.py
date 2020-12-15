import logging

FORMAT = '%(name)s (%(levelname)s): %(message)s'

logging.basicConfig(format=FORMAT)

logger = logging.getLogger("yamz")
logger.setLevel(logging.INFO)
