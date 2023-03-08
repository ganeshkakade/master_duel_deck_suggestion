import re
import json
import string
from pathlib import Path

import shutil
import pyautogui
import numpy as np
from pytesseract import pytesseract
from PIL import Image, ImageFilter, ImageEnhance

from master_duel_deck_suggestion.scripts.constants import FIXED_SCREEN_SIZE, FILE_CONFIG

tesseract_path = shutil.which('tesseract')
if tesseract_path is not None:
    pytesseract.tesseract_cmd = tesseract_path
else:
    pytesseract.tesseract_cmd =  r"C:\Users\UserName\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

size = pyautogui.size()
w_size_ratio = size.width / FIXED_SCREEN_SIZE.get('width')
h_size_ratio = size.height / FIXED_SCREEN_SIZE.get('height')

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

def vibrant_colorfulness(image):
    # convert the image to RGB color space
    image = image.convert("RGB")

    # convert the image to a numpy array
    img_array = np.array(image)

    # calculate the standard deviation of each color channel
    r_std = np.std(img_array[:,:,0])
    g_std = np.std(img_array[:,:,1])
    b_std = np.std(img_array[:,:,2])

    # calculate the average standard deviation
    avg_std = (r_std + g_std + b_std) / 3

    # define a threshold for colorfulness
    colorful_threshold = 25

    # check if the image is colorful or not
    # if avg_std > colorful_threshold:
    #     return True
    # else:
    #     return False
    return avg_std

def path_exists(path):
    return path.exists()

def makedirs(path):
    Path(path).mkdir(exist_ok=True, parents=True)

def get_filesize(path):
    return Path(path).stat().st_size

def get_filepath(file_instance, relative_path):
    file_dir = Path(file_instance).resolve().parent
    file_path = file_dir.joinpath(relative_path).resolve()
    return file_path 

def get_region_coords(coords):
    dx = w_size_ratio * coords.get('x')
    dy = h_size_ratio * coords.get('y')
    return {'x': dx, 'y': dy}

def get_region_size(size):
    w = w_size_ratio * size.get('width')
    h = h_size_ratio * size.get('height')
    return {'width': w, 'height': h}

def get_json_file(file_path):
    if file_path.exists():
        try:
            with file_path.open(**FILE_CONFIG) as json_file:
                return json.load(json_file)
        except json.decoder.JSONDecodeError:
            print(f"invalid {file_path}")
    else:
        print(f"{file_path} does not exists")

def write_to_file(file_path, contents):
    with file_path.open(mode='w', **FILE_CONFIG) as file:
        file.write(contents)

def writelines_to_file(file_path, contents):
    with file_path.open(mode='w', **FILE_CONFIG) as file:
            file.writelines(contents)

def get_log_file(file_path):
    if file_path.exists():
        with file_path.open(**FILE_CONFIG) as file:
            return file.readlines()
    else:
        print(f"{file_path} does not exists")

def remove_file(file_path):
    if file_path.exists():
        file_path.unlink()

def truncate_file(file_path):
     with file_path.open(mode='w', **FILE_CONFIG) as file:
        pass

def normalize_str(s):
    return s.strip().lower()

def replace_non_ascii_with_space(s):
    printable_chars = set(string.printable)
    return ''.join(char if char in printable_chars else ' ' for char in s)
