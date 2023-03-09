import json
import time

import pyautogui
import pygetwindow

from master_duel_deck_suggestion.scripts.helpers import (
    preprocess_and_ocr_image, 
    get_region_coords, 
    get_region_size, 
    get_filepath, 
    vibrant_colorfulness,
    get_json_file,
    write_to_file,
    normalize_str,
    replace_non_ascii_with_space
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

    FINISH_OWNED_SIZE,
    FINISH_OWNED_COORDS,

    TITLE_IMAGE_DEFECT,
    SEARCH_SELECTION_DEFECT, 
    OUT_OF_BOUND_DEFECT,

    FILTERED_CARD_INFO_JSON,
    CARD_OWNED_INFO_JSON,

    EXISTS_THRESHOLD
)
from master_duel_deck_suggestion.tools.debugging import (
    logger,
    title_image_defect_logger,
    search_selection_defect_logger,
    out_of_bound_defect_logger
)

data_dir = get_filepath(__file__, "../data")

FILTERED_CARD_INFO_JSON_PATH = data_dir / FILTERED_CARD_INFO_JSON
CARD_OWNED_INFO_JSON_PATH = data_dir / CARD_OWNED_INFO_JSON

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

finish_owned_region_size = get_region_size(FINISH_OWNED_SIZE)
finish_owned_region_coords = get_region_coords(FINISH_OWNED_COORDS)

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

def search_card_exists(card, repeat=0, dx=0, dy=0): # dx, dy -> movement along x-axis, y-axis 

    avg_std = search_selection_avg_std(dx, dy)

    if not avg_std > EXISTS_THRESHOLD:
        if not repeat:
            return False, SEARCH_SELECTION_DEFECT
        else:
            return False, TITLE_IMAGE_DEFECT
 
    move_to_select(dx, dy) # select card from search results

    if image_to_text_match(card):
        return True, None

    repeat += 1
    if repeat == 30: # max repeat limit 30. # horizontal limit 6, vertical limit 5 i.e 5 x 6 = 30
        out_of_bound_defect_logger.debug(f"{OUT_OF_BOUND_DEFECT}: {card.get('name')}")
        return False, OUT_OF_BOUND_DEFECT

    if repeat and repeat % 6 == 0:
        dx = 0
        dy = dy + select_region_coords_delta.get('y')
    else:
        dx = dx + select_region_coords_delta.get('x')
    
    card_exists, defect_type = search_card_exists(card, repeat, dx, dy)
    return card_exists, defect_type

def get_card_finish_owned_info(card):
    with pyautogui.screenshot(region=(
        finish_owned_region_coords.get('x'), 
        finish_owned_region_coords.get('y'), 
        finish_owned_region_size.get('width'), 
        finish_owned_region_size.get('height')
    )) as finish_owned_image:
        finish_owned = preprocess_and_ocr_image(finish_owned_image).strip()
        numbers = [int(x) if x.isdigit() else 0 for x in finish_owned.split('/')]
        while len(numbers) < 3:
            numbers.append(0)
        return numbers[:3] 
   
def get_card_owned_info(filtered_card_info):
    card_owned = []

    for card in filtered_card_info:
        move_to_search()
        type_name_enter(card)

        card_exists, defect_type = search_card_exists(card)

        if card_exists:
            basic_finish_owned, glossy_finish_owned, royal_finish_owned = get_card_finish_owned_info(card)
            card["basic_finish_owned"] = basic_finish_owned
            card["glossy_finish_owned"] = glossy_finish_owned
            card["royal_finish_owned"] = royal_finish_owned
            card_owned.append(card)
        else:
            card["basic_finish_owned"] = 0
            card["glossy_finish_owned"] = 0
            card["royal_finish_owned"] = 0
            card_owned.append(card)

            if defect_type == TITLE_IMAGE_DEFECT:
                title_image_defect_logger.debug(f"{TITLE_IMAGE_DEFECT}: {card.get('name')}")
            if defect_type == SEARCH_SELECTION_DEFECT:
                search_selection_defect_logger.debug(f"{SEARCH_SELECTION_DEFECT}: {card.get('name')}")
            if defect_type == OUT_OF_BOUND_DEFECT:
                out_of_bound_defect_logger.debug(f"{OUT_OF_BOUND_DEFECT}: {card.get('name')}")

    return card_owned

def search_selection_avg_std(dx, dy):
    with pyautogui.screenshot(region=(
        card_selection_region_coords.get('x') + dx, 
        card_selection_region_coords.get('y') + dy, 
        card_selection_region_size.get('width'), 
        card_selection_region_size.get('height')
    )) as selection_image:
        return vibrant_colorfulness(selection_image)

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
    name = replace_non_ascii_with_space(card.get('name'))
    pyautogui.write(name)
    pyautogui.press("enter")
    time.sleep(S_TIME + 1.5) # wait for search results to load

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
