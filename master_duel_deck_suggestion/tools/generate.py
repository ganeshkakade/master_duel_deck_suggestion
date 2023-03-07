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

    FILTERED_CARD_INFO_JSON,
    SP_TITLE_FILTERED_CARD_INFO_JSON
)
from master_duel_deck_suggestion.tools.debugging import (
    logger,
    title_image_defect_logger,
    search_selection_defect_logger,
    out_of_bound_defect_logger
)

log_dir = get_filepath(__file__, "../logs")
data_dir = get_filepath(__file__, "../data") 

TITLE_IMAGE_DEFECT_LOG_PATH = log_dir / TITLE_IMAGE_DEFECT_LOG
SEARCH_SELECTION_DEFECT_LOG_PATH = log_dir / SEARCH_SELECTION_DEFECT_LOG
OUT_OF_BOUND_DEFECT_LOG_PATH = log_dir / OUT_OF_BOUND_DEFECT_LOG

FILTERED_CARD_INFO_JSON_PATH = data_dir / FILTERED_CARD_INFO_JSON
SP_TITLE_FILTERED_CARD_INFO_JSON_PATH = data_dir / SP_TITLE_FILTERED_CARD_INFO_JSON

def generate_dump_sp_title_filtered_card_info():
    filtered_card_info = get_json_file(FILTERED_CARD_INFO_JSON_PATH)
    if filtered_card_info:
        regex = re.compile(r'[^a-zA-Z0-9\s]+')
        sp_title_filtered_card_info = [o for o in filtered_card_info if regex.search(o.get("name"))]
        write_to_file(SP_TITLE_FILTERED_CARD_INFO_JSON_PATH, json.dumps(sp_title_filtered_card_info))

def generate_dump_debug_log():
    filtered_card_info = get_json_file(FILTERED_CARD_INFO_JSON_PATH)
    if filtered_card_info:
        truncate_file(TITLE_IMAGE_DEFECT_LOG_PATH)
        truncate_file(SEARCH_SELECTION_DEFECT_LOG_PATH)
        truncate_file(OUT_OF_BOUND_DEFECT_LOG_PATH)

        for card in filtered_card_info:
            title_image_defect_logger.debug(f"{TITLE_IMAGE_DEFECT}: {card['name']}")
            search_selection_defect_logger.debug(f"{SEARCH_SELECTION_DEFECT}: {card['name']}")
            out_of_bound_defect_logger.debug(f"{OUT_OF_BOUND_DEFECT}: {card['name']}")

def main():
    generate_dump_debug_log()
    generate_dump_sp_title_filtered_card_info()

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
