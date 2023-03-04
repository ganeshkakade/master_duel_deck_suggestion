import re
import pyautogui
import shutil
from pathlib import Path
from pytesseract import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from master_duel_deck_suggestion.scripts.constants import FIXED_SCREEN_SIZE

tesseract_path = shutil.which('tesseract')
if tesseract_path is not None:
    pytesseract.tesseract_cmd = shutil.which('tesseract')
else:
    pytesseract.tesseract_cmd =  r"C:\Users\UserName\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

size = pyautogui.size()
w_size_ratio = size.width / FIXED_SCREEN_SIZE['width']
h_size_ratio = size.height / FIXED_SCREEN_SIZE['height']

def preprocess_and_ocr_image(image):
    # enhance the image for better OCR accuracy
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2)
    image = image.convert('L')

    # apply thresholding to convert the image to black and white
    threshold = 128
    image = image.point(lambda x: 255 if x > threshold else 0)

    # apply image filter to remove noise
    image = image.filter(ImageFilter.MedianFilter())

    # apply image filter to enhance text
    image = image.filter(ImageFilter.MedianFilter())
    image = image.filter(ImageFilter.SHARPEN)

    # extract text using tesseract
    text = pytesseract.image_to_string(image)
    return text

def normalize_str(str):
    return (
        re.sub(r'[^\w\s-]', '', str)
        .strip()
        .lower()
    )

def alnum_str():
    return re.sub(r'[^a-zA-Z0-9]+', '_', s).strip('_').lower()

def path_exists(path):
    return Path(path).exists()

def makedirs(path):
    Path(path).parent.mkdir(exist_ok=True, parents=True)

def get_filesize(path):
    return Path(path).stat().st_size

def get_filepath(file_instance, relative_path):
    file_dir = Path(file_instance).resolve().parent
    file_path = file_dir.joinpath(relative_path).resolve()
    return file_path 

def get_region_coords(coords):
    dx = w_size_ratio * coords['x']
    dy = h_size_ratio * coords['y']
    return {'x': dx, 'y': dy}

def get_region_size(size):
    w = w_size_ratio * size['width']
    h = h_size_ratio * size['height']
    return {'width': w, 'height': h}
    