import json
import pyautogui
import pygetwindow
from master_duel_deck_suggestion.scripts.helpers import normalize_str, preprocess_and_ocr_image, get_region_coords, get_region_size, get_filepath, path_exists
from master_duel_deck_suggestion.scripts.constants import SEARCH_COORDS, SELECT_COORDS, SELECT_COORDS_DELTA, TITLE_SIZE, TITLE_COORDS, DETAIL_COORDS, CLOSE_COORS, TITLE_IMAGE_DEFECT
from master_duel_deck_suggestion.tools.debugging import logger
import time

data_dir = get_filepath(__file__, "../data")  
CARD_INFO_DATA_PATH = data_dir / "card_info.json"

search_region_coords = get_region_coords(SEARCH_COORDS)
select_region_coords = get_region_coords(SELECT_COORDS)
select_region_coords_delta = get_region_coords(SELECT_COORDS_DELTA)

title_region_size = get_region_size(TITLE_SIZE)
title_region_coords = get_region_coords(TITLE_COORDS)

select_detail_region_coords = get_region_coords(DETAIL_COORDS)
close_region_coords = get_region_coords(CLOSE_COORS)

def image_to_text_match(card):
    open_detail()
    
    image = take_title_screenshot(card)
    
    name = normalize_str(card['name'])
    text = normalize_str(preprocess_and_ocr_image(image))

    logger.debug(f"card name: {name}")
    logger.debug(f"extracted text: {text}")

    close_detail()

    if len(text) > 0 and (text == name or text in name): # also checks if text partially matches with the name
       return True
    return False

def validate_selected(card, repeat=0, dx=0, dy=0): # dx -> movement along x-axis
    if image_to_text_match(card):
        return True

    repeat = repeat + 1
    if repeat == 1: # max repeat limit 5. # increase limit to 30 with vertical 
        return False

    dx = dx + select_region_coords_delta['x']
    move_to_select(dx)
    return validate_selected(card, repeat, dx)

def get_card_info_from_file():
    if path_exists(CARD_INFO_DATA_PATH):
        try:
            with open(CARD_INFO_DATA_PATH) as json_file:
                return json.load(json_file)
        except json.decoder.JSONDecodeError:
            print("invalid card_info.json file")
    else:
        print("card_info.json file does not exist")
    return []


def get_card_owned_info(card_info):
    card_owned = []

    for card in card_info:
        move_to_search()
        type_name_enter(card)

        # before should check if result exists for entered name(same mechanism could be added in repeat) 
        # that "if condition" would save move to select time
        # also could log info on cards which does not exists in ocg / has weird card name like live*twin which are not searchable
        move_to_select(duration=2)

        if validate_selected(card):
            pass
            # gather the rest of information like card dismantalable, no owned etc
            # need to process more for card_owned info
        else:
            logger.debug(f"{TITLE_IMAGE_DEFECT}: {card['name']}")

    return card_owned

def take_title_screenshot(card):
    return pyautogui.screenshot(region=(title_region_coords['x'], title_region_coords['y'], title_region_size['width'], title_region_size['height'])) # might need to update based on screen resolution (default: 1920x1080)

def type_name_enter(card):
    pyautogui.typewrite(card['name'])
    pyautogui.press("enter")

def move_to_select(dx=0, dy=0, duration=0):
    pyautogui.moveTo(select_region_coords['x'] + dx, select_region_coords['y'] + dy, duration = duration) # added a duration delay since loading cards based on search takes more time
    pyautogui.click()
    
def move_to_search():
    pyautogui.moveTo(search_region_coords['x'], search_region_coords['y'])
    pyautogui.click()

def move_to_select_detail():
    pyautogui.moveTo(select_detail_region_coords['x'], select_detail_region_coords['y'])
    pyautogui.click()

def open_detail():
    move_to_select_detail() # open card detail
    time.sleep(0.5) # wait for detail window to open

def close_detail():
    pyautogui.moveTo(close_region_coords['x'], close_region_coords['y'])
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
        card_owned_info = get_card_owned_info(card_info)

    else:
        logger.debug(f"card info not available in the card_info.json file")

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
