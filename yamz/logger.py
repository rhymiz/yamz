import logging

FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'

logging.basicConfig(format=FORMAT)

logger = logging.getLogger("Yamz")
logger.setLevel(logging.INFO)
