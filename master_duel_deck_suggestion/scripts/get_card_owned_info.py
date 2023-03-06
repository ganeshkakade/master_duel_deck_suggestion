import re
import json
import time

import pyautogui
import pygetwindow

from master_duel_deck_suggestion.scripts.helpers import (
    normalize_str, 
    preprocess_and_ocr_image, 
    get_region_coords, 
    get_region_size, 
    get_filepath, path_exists, 
    vibrant_colors_exists,
    get_json_info,
    unescape_ucode_with_space
)
from master_duel_deck_suggestion.scripts.constants import (
    SEARCH_COORDS, 
    SELECT_COORDS, 
    SELECT_COORDS_DELTA, 
    TITLE_SIZE, 
    TITLE_COORDS, 
    DETAIL_COORDS, 
    CLOSE_COORDS, 
    TITLE_IMAGE_DEFECT, 
    CARD_SELECTION_SIZE, 
    CARD_SELECTION_COORDS, 
    OUT_OF_BOUND_DEFECT, 
    SEARCH_SELECTION_DEFECT, 
    SAVE_SIZE, SAVE_COORDS,
    SORT_COORDS,
    SORT_NO_OWNED_DESC_COORDS,
    RESET_COORDS
)
from master_duel_deck_suggestion.tools.debugging import logger

data_dir = get_filepath(__file__, "../data")  
CARD_INFO_DATA_PATH = data_dir / "card_info.json"

search_region_coords = get_region_coords(SEARCH_COORDS)
select_region_coords = get_region_coords(SELECT_COORDS)
select_region_coords_delta = get_region_coords(SELECT_COORDS_DELTA)

title_region_size = get_region_size(TITLE_SIZE)
title_region_coords = get_region_coords(TITLE_COORDS)

select_detail_region_coords = get_region_coords(DETAIL_COORDS)
close_region_coords = get_region_coords(CLOSE_COORDS)

card_selection_region_size = get_region_size(CARD_SELECTION_SIZE)
card_selection_region_coords = get_region_coords(CARD_SELECTION_COORDS)

save_region_size = get_region_size(SAVE_SIZE)
save_region_coords = get_region_coords(SAVE_COORDS)

sort_region_coords = get_region_coords(SORT_COORDS)
sort_no_owned_region_coords = get_region_coords(SORT_NO_OWNED_DESC_COORDS)

reset_region_coords = get_region_coords(RESET_COORDS)

S_TIME = 0.5

def image_to_text_match(card):
    open_detail()
    
    image = take_title_screenshot(card)

    close_detail()
    
    name = normalize_str(card['name'])
    text = normalize_str(preprocess_and_ocr_image(image))

    if len(text) > 0 and (text == name or text in name): # also checks if text partially matches with name
       return True

    # log only when text does not match with name
    logger.debug(f"card name: {name}")
    logger.debug(f"extracted text: {text}")

    return False

def check_search_selection(card, repeat=0, dx=0, dy=0): # dx, dy -> movement along x-axis, y-axis
    if not repeat:
        time.sleep(2) # wait for results to load when searched
    
    if not search_selection_exists(dx, dy):
        logger.debug(f"{SEARCH_SELECTION_DEFECT}: {card['name']}")
        return False
    
    move_to_select(dx, dy)

    if image_to_text_match(card):
        return True
    else: 
        logger.debug(f"{TITLE_IMAGE_DEFECT}: {card['name']}")

    repeat += 1
    if repeat == 30: # max repeat limit 30. # horizontal limit 6, vertical limit 5 i.e 5 x 6 = 30
        logger.debug(f"{OUT_OF_BOUND_DEFECT}: {card['name']}")
        return False
    if repeat and repeat % 6 == 0:
        dx = 0
        dy = dy + select_region_coords_delta['y']
    else:
        dx = dx + select_region_coords_delta['x']

    return check_search_selection(card, repeat, dx, dy)

def search_selection_exists(dx, dy):
    selection_image = pyautogui.screenshot(region=(
        card_selection_region_coords['x'] + dx, 
        card_selection_region_coords['y'] + dy, 
        card_selection_region_size['width'], 
        card_selection_region_size['height']
    ))
    return vibrant_colors_exists(selection_image)
    
def get_card_owned_info(card_info):
    card_owned = []

    for card in card_info:
        move_to_search()
        type_name_enter(card)
        
        if check_search_selection(card):
            card_owned.append(card)

    return card_owned

def deck_window_exists():
    save_image = pyautogui.screenshot(region=(
        save_region_coords['x'], 
        save_region_coords['y'], 
        save_region_size['width'], 
        save_region_size['height']
    ))
    if normalize_str(preprocess_and_ocr_image(save_image)) == 'save':
        return True
    else:  
        print("switch to create new deck in masterduel before you proceed")
    return False

def take_title_screenshot(card):
    with pyautogui.screenshot(region=(title_region_coords['x'], title_region_coords['y'], title_region_size['width'], title_region_size['height'])) as screenshot:# might need to update based on screen resolution (default: 1920x1080)
        return screenshot

def type_name_enter(card):
    pyautogui.typewrite(unescape_ucode_with_space(card["name"]))
    pyautogui.press("enter")

def move_to_select(dx=0, dy=0):
    pyautogui.moveTo(select_region_coords['x'] + dx, select_region_coords['y'] + dy)
    pyautogui.click()
    
def move_to_search():
    pyautogui.moveTo(search_region_coords['x'], search_region_coords['y'])
    pyautogui.click()

def move_to_select_detail():
    pyautogui.moveTo(select_detail_region_coords['x'], select_detail_region_coords['y'])
    pyautogui.click()

def open_detail():
    move_to_select_detail() # open card detail
    time.sleep(S_TIME) # wait for detail window to open

def close_detail():
    pyautogui.moveTo(close_region_coords['x'], close_region_coords['y'])
    pyautogui.click()

def switch_window(title):
    handle = pygetwindow.getWindowsWithTitle(title)
    if handle:
        handle[0].activate()
        handle[0].maximize()
        time.sleep(S_TIME) # wait for window to switch
    else:
        print(f"{title} window does not exists")

def set_sort_filters():
    pyautogui.moveTo(sort_region_coords['x'], sort_region_coords['y'])
    pyautogui.click()
    time.sleep(S_TIME) # wait for window to open
    pyautogui.moveTo(sort_no_owned_region_coords['x'], sort_no_owned_region_coords['y'])
    pyautogui.click()
    time.sleep(S_TIME) # wait for window to close

def reset_all_filters():
    pyautogui.moveTo(reset_region_coords['x'], reset_region_coords['y'])
    pyautogui.click()
    time.sleep(S_TIME) # wait for reset to complete

def main():
    card_owned_info = []
    card_info = get_json_info(CARD_INFO_DATA_PATH)
    
    if card_info:
        switch_window('masterduel')
        
        if deck_window_exists():
            set_sort_filters()
            card_owned_info = get_card_owned_info(card_info)

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
