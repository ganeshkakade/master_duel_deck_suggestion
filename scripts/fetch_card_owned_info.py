import json
import pyautogui
import pygetwindow
from PIL import Image
from pytesseract import pytesseract
from helpers import logger, normalize_str, makedirs, safe_open, getfilesize, get_region_coords, get_region_size
from constants import CARD_INFO_DATA_PATH, CARD_IMAGE_DATA_PATH, SEARCH_COORDS, SELECT_COORDS, SELECT_COORDS_DELTA, TITLE_SIZE, TITLE_COORDS

path_to_tesseract = f"C:/Users/Ganesh Kakade/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

search_region_coords = get_region_coords(SEARCH_COORDS)
select_region_coords = get_region_coords(SELECT_COORDS)
select_region_coords_delta = get_region_coords(SELECT_COORDS_DELTA)

title_region_size = get_region_size(TITLE_SIZE)
title_region_coords = get_region_coords(TITLE_COORDS)

def image_to_text_match(card):
    image_path = take_title_screenshot(card)
    
    image = Image.open(image_path)
    pytesseract.tesseract_cmd = path_to_tesseract

    text = normalize_str(pytesseract.image_to_string(image))
    name = normalize_str(card['name'])

    logger.debug(f"card name: {name}")
    logger.debug(f"extracted text: {text}")
    logger.debug(f"match result: {name == text or text in name}")

    if name == text or text in name: # also checks if text partially matches with the name
       return True
    return False

def validate_select(card, repeat=0, dx=0): # dx -> movement along x-axis
    if image_to_text_match(card):  
        return True

    repeat = repeat + 1
    if repeat == 3: # max repeat limit 5
        return False
    
    dx = dx + select_region_coords_delta['x']
    move_to_select(dx)
    return validate_select(card, repeat, dx)

def get_card_info_from_file():
    with safe_open(CARD_INFO_DATA_PATH) as json_file:
        if getfilesize(CARD_INFO_DATA_PATH) > 0:
            return json.load(json_file)
    return []

def get_card_owned_info(card_info):
    card_owned = []

    for card in card_info:
        move_to_search()
        type_name_enter(card)
        move_to_select(duration=2)

        if validate_select(card):
            take_screenshot(card)
            # need to process more for card_owned info
        else:
            logger.debug(f"screenshot not taken. no image title match found for the card: {card['name']}")

    return card_owned

def take_title_screenshot(card):
    image_path = f"{CARD_IMAGE_DATA_PATH}/title_{normalize_str(card['name'])}.png"
    pyautogui.screenshot(image_path, region=(title_region_coords['x'], title_region_coords['y'], title_region_size['width'], title_region_size['height'])) # might need to change based on screen resolution (default: 1920x1080)
    return image_path

def take_screenshot(card):
    image_path = f"{CARD_IMAGE_DATA_PATH}/{normalize_str(card['name'])}.png"
    pyautogui.screenshot(image_path)
    return image_path

def type_name_enter(card):
    pyautogui.typewrite(card['name'])
    pyautogui.press("enter")

def move_to_select(dx=0, dy=0, duration=0):
    pyautogui.moveTo(select_region_coords['x'] + dx, select_region_coords['y'] + dy, duration = duration) # added a duration delay since loading cards based on search takes more time
    pyautogui.click()
    
def move_to_search(duration=0):
    pyautogui.moveTo(search_region_coords['x'], search_region_coords['y'], duration = duration)
    pyautogui.click()

def switch_window():
    handle = pygetwindow.getWindowsWithTitle('masterduel')
    if handle:
        handle[0].activate()
        handle[0].maximize()

def main():
    card_owned_info = []
    card_info = get_card_info_from_file()

    if card_info:
        switch_window()
        makedirs(CARD_IMAGE_DATA_PATH) # make dir to store processed card images
        card_owned_info = get_card_owned_info(card_info)
        logger.debug(f"card owned info: {card_owned_info}")

    else: logger.debug(f"card info is not available in the {CARD_INFO_DATA_PATH} file")

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
