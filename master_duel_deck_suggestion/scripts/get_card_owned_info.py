import json
import time

import pyautogui
import pygetwindow

from master_duel_deck_suggestion.scripts.helpers import (
    preprocess_and_ocr_image, 
    get_region_coords, 
    get_region_size, 
    get_filepath, 
    vibrant_colors_exists,
    get_json_file,
    write_to_file,
    normalize_str
)
from master_duel_deck_suggestion.scripts.constants import (
    S_TIME,
    SEARCH_COORDS, 
    SELECT_COORDS, 
    SELECT_COORDS_DELTA,
    DETAIL_COORDS, 
    CLOSE_COORDS,
    RESET_COORDS,
    SORT_COORDS,
    SORT_NO_OWNED_DESC_COORDS,
    
    TITLE_SIZE,
    TITLE_COORDS, 

    CARD_SELECTION_SIZE, 
    CARD_SELECTION_COORDS, 

    SAVE_SIZE, 
    SAVE_COORDS,

    TITLE_IMAGE_DEFECT,
    SEARCH_SELECTION_DEFECT, 
    OUT_OF_BOUND_DEFECT,

    FILTERED_CARD_INFO_JSON
)
from master_duel_deck_suggestion.tools.debugging import (
    logger,
    title_image_defect_logger,
    search_selection_defect_logger,
    out_of_bound_defect_logger
)

data_dir = get_filepath(__file__, "../data")

FILTERED_CARD_INFO_JSON_PATH = data_dir / FILTERED_CARD_INFO_JSON

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

def image_to_text_match(card):
    open_detail()
    
    image = take_title_screenshot(card)
    name = normalize_str(card.get('name'))
    text = normalize_str(preprocess_and_ocr_image(image))

    close_detail()

    if text and (text == name or text in name): # checks for text partial match with name
       return True
    else:
        title_image_defect_logger.debug(f"card name: {name}")
        title_image_defect_logger.debug(f"extracted text: {text}")
        return False

def check_search_selection(card, repeat=0, dx=0, dy=0): # dx, dy -> movement along x-axis, y-axis
    if not repeat:
        time.sleep(2) # wait for search results to load
    
    if not search_selection_exists(dx, dy):
        search_selection_defect_logger.debug(f"{SEARCH_SELECTION_DEFECT}: {card.get('name')}")
        return False
    
    move_to_select(dx, dy) # select card from search results 

    if image_to_text_match(card):
        return True
    else:
        title_image_defect_logger.debug(f"{TITLE_IMAGE_DEFECT}: {card.get('name')}")

    repeat += 1
    if repeat == 30: # max repeat limit 30. # horizontal limit 6, vertical limit 5 i.e 5 x 6 = 30
        out_of_bound_defect_logger.debug(f"{OUT_OF_BOUND_DEFECT}: {card.get('name')}")
        return False

    if repeat and repeat % 6 == 0:
        dx = 0
        dy = dy + select_region_coords_delta.get('y')
    else:
        dx = dx + select_region_coords_delta.get('x')

    return check_search_selection(card, repeat, dx, dy)

def search_selection_exists(dx, dy):
    with pyautogui.screenshot(region=(
        card_selection_region_coords.get('x') + dx, 
        card_selection_region_coords.get('y') + dy, 
        card_selection_region_size.get('width'), 
        card_selection_region_size.get('height')
    )) as selection_image:
        return vibrant_colors_exists(selection_image)
    
def get_card_owned_info(filtered_card_info):
    card_owned = []

    for card in filtered_card_info:
        move_to_search()
        type_name_enter(card)
        
        if check_search_selection(card):
            # get more card owned info with preprocess and ocr
            card_owned.append(card)

    return card_owned

def deck_window_exists():
    with pyautogui.screenshot(region=(
        save_region_coords.get('x'), 
        save_region_coords.get('y'), 
        save_region_size.get('width'), 
        save_region_size.get('height')
    )) as save_image:
        if normalize_str(preprocess_and_ocr_image(save_image)) == 'save':
            return True
        else:  
            print("switch to create new deck in masterduel before you proceed")
            return False

def take_title_screenshot(card):
    with pyautogui.screenshot(region=(
        title_region_coords.get('x'), 
        title_region_coords.get('y'), 
        title_region_size.get('width'), 
        title_region_size.get('height')
    )) as screenshot: # based on default: 1920x1080 but should adjust acc. to screen resolution
        return screenshot

def type_name_enter(card):
    pyautogui.write(card.get('name'))
    pyautogui.press("enter")

def move_to_select(dx=0, dy=0):
    pyautogui.moveTo(select_region_coords.get('x') + dx, select_region_coords.get('y') + dy)
    pyautogui.click()
    
def move_to_search():
    pyautogui.moveTo(search_region_coords.get('x'), search_region_coords.get('y'))
    pyautogui.click()

def open_detail():
    pyautogui.moveTo(select_detail_region_coords.get('x'), select_detail_region_coords.get('y'))
    pyautogui.click()
    time.sleep(S_TIME) # wait for detail window to open

def close_detail():
    pyautogui.moveTo(close_region_coords.get('x'), close_region_coords.get('y'))
    pyautogui.click()
    time.sleep(S_TIME) # wait for detail window to close

def switch_window(title):
    handle = pygetwindow.getWindowsWithTitle(title)
    if handle:
        handle[0].activate()
        handle[0].maximize()
        time.sleep(S_TIME) # wait for switch to title window
    else:
        print(f"{title} window does not exists")

def set_sort_filters():
    pyautogui.moveTo(sort_region_coords.get('x'), sort_region_coords.get('y'))
    pyautogui.click()
    time.sleep(S_TIME) # wait for sort window to open
    pyautogui.moveTo(sort_no_owned_region_coords.get('x'), sort_no_owned_region_coords.get('y'))
    pyautogui.click()
    time.sleep(S_TIME) # wait for sort window to close

def reset_all_filters():
    pyautogui.moveTo(reset_region_coords.get('x'), reset_region_coords.get('y'))
    pyautogui.click()
    time.sleep(S_TIME) # wait for filter to reset

def main():
    filtered_card_info = get_json_file(FILTERED_CARD_INFO_JSON_PATH)
    
    if filtered_card_info:
        switch_window('masterduel')
        
        if deck_window_exists():
            set_sort_filters()
            card_owned_info = get_card_owned_info(filtered_card_info)
            write_to_file(CARD_OWNED_INFO_JSON_PATH, json.dumps(card_owned_info))

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
