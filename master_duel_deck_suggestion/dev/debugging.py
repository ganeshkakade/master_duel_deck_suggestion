import os
import logging

file_dir = os.path.dirname(os.path.abspath(__file__))
DEBUG_LOG_PATH = os.path.join(file_dir, "../logs/debug.log")
DEFECT_LOG_PATH = os.path.join(file_dir, "../logs/defect.log")

# create and configure logger
logging.basicConfig(filename=DEBUG_LOG_PATH,
                    format="%(asctime)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger()
