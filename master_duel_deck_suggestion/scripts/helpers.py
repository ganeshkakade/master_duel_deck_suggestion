import os
import pyautogui
import re
from PIL import Image, ImageFilter, ImageEnhance
from pytesseract import pytesseract
from master_duel_deck_suggestion.scripts.constants import FIXED_SCREEN_SIZE, TITLE_SIZE, TITLE_COORDS

pytesseract.tesseract_cmd = f"C:/Users/Ganesh Kakade/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

size = pyautogui.size()

w_size_ratio = size.width / FIXED_SCREEN_SIZE['width']
h_size_ratio = size.height / FIXED_SCREEN_SIZE['height']

def preprocess_and_ocr_image(image_path):
    # load the image
    img = Image.open(image_path)

    # enhance the image for better OCR accuracy
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2)
    img = img.convert('L')

    # apply thresholding to convert the image to black and white
    threshold = 128
    img = img.point(lambda x: 255 if x > threshold else 0)

    # apply image filter to remove noise
    img = img.filter(ImageFilter.MedianFilter())

    # apply image filter to enhance text
    img = img.filter(ImageFilter.MedianFilter())
    img = img.filter(ImageFilter.SHARPEN)

    # extract text using tesseract
    text = pytesseract.image_to_string(img)

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
    