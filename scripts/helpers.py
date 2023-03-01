import os
import logging
import pyautogui
import re
from constants import FIXED_SCREEN_SIZE, TITLE_SIZE, TITLE_COORDS

# create and configure logger
logging.basicConfig(filename="../debug.log",
                    format="%(asctime)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger()

size = pyautogui.size()

w_size_ratio = size.width / FIXED_SCREEN_SIZE['width']
h_size_ratio = size.height / FIXED_SCREEN_SIZE['height']

def normalize_str(str):
    return (
        re.sub(r'[^\w\s-]', '', str)
        .strip()
        .lower()
    )

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def safe_open(path, mode='r'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, mode)

def getfilesize(path):
    return os.stat(path).st_size

def get_region_coords(coords):
    dx = w_size_ratio * coords['x']
    dy = h_size_ratio * coords['y']

    return {'x': dx, 'y': dy}

def get_region_size(size):
    w = w_size_ratio * size['width']
    h = h_size_ratio * size['height']
    
    return {'width': w, 'height': h}
    