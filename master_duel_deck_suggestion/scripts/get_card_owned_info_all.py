
import json

from master_duel_deck_suggestion.tools.debugging import (
    logger
)
from master_duel_deck_suggestion.scripts.constants import (
    CARD_OWNED_INFO_JSON,
    EXISTS_THRESHOLD
)
from master_duel_deck_suggestion.scripts.helpers import (
    write_to_file,
    get_filepath
)
from master_duel_deck_suggestion.scripts.get_card_owned_info import (
    move_to_search,
    type_name_enter,
    search_selection_avg_std,
    move_to_select,
    image_to_text_match,
    select_region_coords_delta,
    get_card_finish_owned_info,
    get_card_can_dismantle_info,
    ui_configured
)

data_dir = get_filepath(__file__, "../data")

CARD_OWNED_INFO_JSON_PATH = data_dir / CARD_OWNED_INFO_JSON

def search_card_exists_all(card, repeat=0, dx=0, dy=0):
    avg_std = search_selection_avg_std(dx, dy)

    if not avg_std > EXISTS_THRESHOLD:
        return card

    move_to_select(dx, dy)

    if image_to_text_match(card):
        basic_finish_owned, glossy_finish_owned, royal_finish_owned = get_card_finish_owned_info()
        can_dismantle = get_card_can_dismantle_info()

        card["basic_finish_owned"] = basic_finish_owned
        card["glossy_finish_owned"] = glossy_finish_owned
        card["royal_finish_owned"] = royal_finish_owned
        card["can_dismantle"] = card["can_dismantle"] + can_dismantle

    repeat += 1
    if repeat == 30:
        return card

    if repeat and repeat % 6 == 0:
        dx = 0
        dy = dy + select_region_coords_delta.get('y')
    else:
        dx = dx + select_region_coords_delta.get('x')

    return search_card_exists_all(card, repeat, dx, dy)

def get_card_owned_info_all(filtered_card_info):
    card_owned = []

    for card in filtered_card_info:
        move_to_search()
        type_name_enter(card)

        new_card = card.copy()
        new_card["basic_finish_owned"] = 0
        new_card["glossy_finish_owned"] = 0
        new_card["royal_finish_owned"] = 0
        new_card["can_dismantle"] = 0

        new_card = search_card_exists_all(new_card)
        card_owned.append(new_card)

    return card_owned

def main():
    filtered_card_info = ui_configured()
    
    if filtered_card_info:
        card_owned_info = get_card_owned_info_all(filtered_card_info)
        write_to_file(CARD_OWNED_INFO_JSON_PATH, json.dumps(card_owned_info))

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)