import re
import json

from master_duel_deck_suggestion.scripts.helpers import (
    get_filepath, 
    get_json_file, 
    write_to_file, 
    truncate_file
)
from master_duel_deck_suggestion.scripts.constants import (
    TITLE_IMAGE_DEFECT,
    SEARCH_SELECTION_DEFECT, 
    OUT_OF_BOUND_DEFECT,

    TITLE_IMAGE_DEFECT_LOG,
    SEARCH_SELECTION_DEFECT_LOG,
    OUT_OF_BOUND_DEFECT_LOG,

    CARD_INFO_JSON,
    FILTERED_CARD_INFO_JSON,
    SP_TITLE_FILTERED_CARD_INFO_JSON,
    LIMITED_FILTERED_CARD_INFO_JSON,
    DIFF_CARD_INFO_JSON,

    EXISTS_THRESHOLD
)
from master_duel_deck_suggestion.tools.debugging import (
    logger,
    title_image_defect_logger,
    search_selection_defect_logger,
    out_of_bound_defect_logger
)
from master_duel_deck_suggestion.scripts.get_card_owned_info import (
    move_to_search,
    type_name_enter,
    search_selection_avg_std,
    switch_window,
    deck_window_exists,
    set_sort_filters
)

log_dir = get_filepath(__file__, "../logs")
data_dir = get_filepath(__file__, "../data") 

TITLE_IMAGE_DEFECT_LOG_PATH = log_dir / TITLE_IMAGE_DEFECT_LOG
SEARCH_SELECTION_DEFECT_LOG_PATH = log_dir / SEARCH_SELECTION_DEFECT_LOG
OUT_OF_BOUND_DEFECT_LOG_PATH = log_dir / OUT_OF_BOUND_DEFECT_LOG

CARD_INFO_JSON_PATH = data_dir / CARD_INFO_JSON
FILTERED_CARD_INFO_JSON_PATH = data_dir / FILTERED_CARD_INFO_JSON
SP_TITLE_FILTERED_CARD_INFO_JSON_PATH = data_dir / SP_TITLE_FILTERED_CARD_INFO_JSON
LIMITED_FILTERED_CARD_INFO_JSON_PATH = data_dir / LIMITED_FILTERED_CARD_INFO_JSON
DIFF_CARD_INFO_JSON_PATH = data_dir / DIFF_CARD_INFO_JSON

def dump_diff_filtered_card_info(json_filepath1, json_filepath2):
    card_info1 = get_json_file(json_filepath1)
    card_info2 = get_json_file(json_filepath2)
    if card_info1 and card_info2:
        set1 = set(o.get('_id') for o in card_info1)
        set2 = set(o.get('_id') for o in card_info2)

        diff = list(set1.symmetric_difference(set2))

        diff_card_info = [o for o in card_info1 + card_info2 if o.get('_id') in diff]
        write_to_file(DIFF_CARD_INFO_JSON_PATH, json.dumps(diff_card_info))

def dump_limited_filtered_card_info(json_filepath, i=None, n=None):
    card_info = get_json_file(json_filepath)
    if card_info:
        start = i if i is not None else 0
        end = (i + n) if (i is not None and n is not None) else None
        write_to_file(LIMITED_FILTERED_CARD_INFO_JSON_PATH, json.dumps(card_info[start:end]))
    else:
        truncate_file(LIMITED_FILTERED_CARD_INFO_JSON_PATH)

def dump_sp_title_filtered_card_info(json_filepath):
    card_info = get_json_file(json_filepath)
    if card_info:
        regex = re.compile(r'[^a-zA-Z0-9\s]+')
        sp_title_filtered_card_info = [o for o in card_info if regex.search(o.get("name"))]
        write_to_file(SP_TITLE_FILTERED_CARD_INFO_JSON_PATH, json.dumps(sp_title_filtered_card_info))

def dump_dummy_defects_log(json_filepath):
    card_info = get_json_file(json_filepath)
    if card_info:
        truncate_file(TITLE_IMAGE_DEFECT_LOG_PATH)
        truncate_file(SEARCH_SELECTION_DEFECT_LOG_PATH)
        truncate_file(OUT_OF_BOUND_DEFECT_LOG_PATH)

        for card in card_info:
            title_image_defect_logger.debug(f"{TITLE_IMAGE_DEFECT}: {card.get('name')}")
            search_selection_defect_logger.debug(f"{SEARCH_SELECTION_DEFECT}: {card.get('name')}")
            out_of_bound_defect_logger.debug(f"{OUT_OF_BOUND_DEFECT}: {card.get('name')}")

def dump_actual_search_selection_defect_log(json_filepath):
    card_info = get_json_file(json_filepath)
    if card_info:
        truncate_file(SEARCH_SELECTION_DEFECT_LOG_PATH)

        switch_window('masterduel')

        if deck_window_exists():
            set_sort_filters()
            for card in card_info:
                move_to_search()
                type_name_enter(card)
                if search_selection_avg_std(0, 0) < EXISTS_THRESHOLD:
                    search_selection_defect_logger.debug(f"{SEARCH_SELECTION_DEFECT}: {card.get('name')}")

def main():
    dump_dummy_defects_log(FILTERED_CARD_INFO_JSON_PATH)
    dump_sp_title_filtered_card_info(FILTERED_CARD_INFO_JSON_PATH)
    dump_limited_filtered_card_info(FILTERED_CARD_INFO_JSON_PATH, 0, 5)
    dump_diff_filtered_card_info(CARD_INFO_JSON_PATH, FILTERED_CARD_INFO_JSON_PATH)
   
    # dump_actual_search_selection_defect_log(FILTERED_CARD_INFO_JSON_PATH)

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
