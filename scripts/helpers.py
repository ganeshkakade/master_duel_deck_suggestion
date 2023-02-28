import os
import logging

# create and configure logger
logging.basicConfig(filename="../debug.log",
                    format='%(asctime)s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filemode='w',
                    level=logging.DEBUG)

# creating an logging object
logger = logging.getLogger()

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def safe_open(path, mode='r'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, mode)
