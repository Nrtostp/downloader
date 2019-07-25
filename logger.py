import logging
import logging.handlers
from config import msg_home
logger = logging.getLogger('logger')

import coloredlogs
coloredlogs.install(level='WARNING')

# handler1 = logging.StreamHandler()
handler2 = logging.FileHandler(filename=msg_home+'debug.log')

logger.setLevel(logging.DEBUG)
# handler1.setLevel(logging.WARNING)
handler2.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s %(name)s %(thread)d %(threadName)s %(levelname)s %(message)s")
# handler1.setFormatter(formatter)
handler2.setFormatter(formatter)

# logger.addHandler(handler1)
logger.addHandler(handler2)
