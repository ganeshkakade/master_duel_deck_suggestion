import os
import logging

scripts_dir = os.path.dirname(os.path.abspath(__file__))
DEBUG_LOG_PATH = os.path.join(scripts_dir, "../../debug.log")

# create and configure logger
logging.basicConfig(filename=DEBUG_LOG_PATH,
                    format="%(asctime)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger()