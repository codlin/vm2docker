import logging
import logging.handlers

logger = logging.getLogger('vm2docker')

if len(logger.handlers) == 0:
    # create console handler and set level
    handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d [%(levelname)s]: %(message)s", '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical
