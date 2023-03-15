# this experimental module may not provide accurate information about owned cards since scrolling is unreliable and limited upto first 30 cards only
import json

from master_duel_deck_suggestion.scripts.helpers import (
    write_to_file,
    get_filepath,
    preprocess_and_ocr_image,
    normalize_str,
    contains_non_alphanumeric,
    sequence_matcher_ratio
)
from master_duel_deck_suggestion.scripts.constants import (
    CARD_OWNED_INFO_JSON,

    EXISTS_THRESHOLD,

    TITLE_IMAGE_DEFECT,
    SEARCH_SELECTION_DEFECT,
    OUT_OF_BOUND_DEFECT
)
from master_duel_deck_suggestion.tools.debugging import (
    logger,
    title_image_defect_logger,
    search_selection_defect_logger,
    out_of_bound_defect_logger
)
from master_duel_deck_suggestion.scripts.get_card_owned_info import (
    search_selection_avg_std,
    take_title_screenshot,
    select_region_coords_delta,
    move_to_select,
    get_card_finish_owned_info,
    get_card_can_dismantle_info,
    open_detail,
    close_detail,
    ui_configured
)

data_dir = get_filepath(__file__, "../data")

CARD_OWNED_INFO_JSON_PATH = data_dir / CARD_OWNED_INFO_JSON

def extract_text_from_title():
    open_detail()
    image = take_title_screenshot()
    close_detail()
    return preprocess_and_ocr_image(image)

def card_exists(dx, dy):
    avg_std = search_selection_avg_std(dx, dy)
    return avg_std > EXISTS_THRESHOLD

def get_card(filtered_card_info, text):
    for card in filtered_card_info:
        card_name = card.get('name')
        name = normalize_str(card_name)
        text = normalize_str(text)

        if text and (text == name or text in name):
            return card
        if text and contains_non_alphanumeric(card_name) and sequence_matcher_ratio(text, name) >= 0.8:
            return card
    return {}

def update_card_owned(card_owned, card):
    for i in range(len(card_owned)):
        if card_owned[i].get('_id') == card.get('_id'):
            card_owned[i]['can_dismantle'] = card_owned[i].get('can_dismantle', 0) + card.get('can_dismantle', 0)
            return card_owned

    card_owned.append(card)
    return card_owned

def get_card_owned_info_via_scroll(filtered_card_info, card_owned=[], repeat=0, dx=0, dy=0):
    
    is_card_exists = card_exists(dx, dy)

    if not repeat and not is_card_exists:
        search_selection_defect_logger.debug(f"{SEARCH_SELECTION_DEFECT}: all cards")
        return card_owned

    if not is_card_exists:
        out_of_bound_defect_logger.debug(f"{OUT_OF_BOUND_DEFECT}: all cards")
        return card_owned

    move_to_select(dx, dy)

    text = extract_text_from_title()

    card = get_card(filtered_card_info, text)

    if card: 
       
        basic_finish_owned, glossy_finish_owned, royal_finish_owned = get_card_finish_owned_info()
        can_dismantle = get_card_can_dismantle_info()
       
        new_card = card.copy()

        new_card['basic_finish_owned'] = basic_finish_owned
        new_card['glossy_finish_owned'] = glossy_finish_owned
        new_card['royal_finish_owned'] = royal_finish_owned
        new_card['can_dismantle'] = can_dismantle

        card_owned = update_card_owned(card_owned, new_card)
    else:
         title_image_defect_logger.debug(f"{TITLE_IMAGE_DEFECT}: all cards[{text}]")

    repeat += 1
    if repeat and repeat % 6 == 0:
        dx = 0
        dy = dy + select_region_coords_delta.get('y')
    else:
        dx = dx + select_region_coords_delta.get('x')

    return get_card_owned_info_via_scroll(filtered_card_info, card_owned, repeat, dx, dy)

def main():
    filtered_card_info = ui_configured()
    
    if filtered_card_info:
        card_owned_info_via_scroll = get_card_owned_info_via_scroll(filtered_card_info)
        write_to_file(CARD_OWNED_INFO_JSON_PATH, json.dumps(card_owned_info_via_scroll))

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)