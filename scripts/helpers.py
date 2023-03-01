import os
import logging
import pyautogui
import re
from PIL import Image, ImageFilter, ImageEnhance
from pytesseract import pytesseract
from constants import FIXED_SCREEN_SIZE, TITLE_SIZE, TITLE_COORDS

pytesseract.tesseract_cmd = f"C:/Users/Ganesh Kakade/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

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

basewidth = 800

def preprocess_and_ocr_image(image_path):
    image = Image.open(image_path)

    # rescale the image to a fixed width of 800 pixels
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)

    # apply Gaussian blur to smooth out the image
    blur_radius = 2
    image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # convert the image to grayscale
    gray = image.convert('L')

    # apply binary thresholding
    threshold_value = 200
    threshold_img = gray.point(lambda x: 0 if x < threshold_value else 255, '1')

    # apply dilation to thicken the characters
    dilated_img = threshold_img.filter(ImageFilter.MaxFilter(size=3))

    # apply erosion to remove noise from the image
    eroded_img = dilated_img.filter(ImageFilter.MinFilter(size=3))

    # convert image to "RGB" mode
    rgb_img = eroded_img.convert('RGB')

    # apply sharpening
    sharpen_factor = 2
    enhancer = ImageEnhance.Sharpness(rgb_img)
    sharpened_img = enhancer.enhance(sharpen_factor)

    # Convert image back to "L" mode
    final_img = sharpened_img.convert('L')

    text = pytesseract.image_to_string(final_img)

    return text

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
    