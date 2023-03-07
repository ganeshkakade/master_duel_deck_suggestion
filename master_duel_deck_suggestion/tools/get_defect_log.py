import re
import json

from master_duel_deck_suggestion.scripts.helpers import (
    path_exists, 
    get_filepath, 
    get_json_file, 
    write_to_file, 
    get_log_file,
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
    SP_TITLE_FILTERED_CARD_INFO_JSON,
    TITLE_IMAGE_DEFECT_JSON,
    SEARCH_SELECTION_DEFECT_JSON,
    OUT_OF_BOUND_DEFECT_JSON
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
TITLE_IMAGE_DEFECT_JSON_PATH = log_dir / TITLE_IMAGE_DEFECT_JSON
SEARCH_SELECTION_DEFECT_JSON_PATH = log_dir / SEARCH_SELECTION_DEFECT_JSON
OUT_OF_BOUND_DEFECT_JSON_PATH = log_dir / OUT_OF_BOUND_DEFECT_JSON

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

def process_defect_logs():
    filtered_card_info = get_json_file(FILTERED_CARD_INFO_JSON_PATH)
    if filtered_card_info:
        title_image_defect_lines = get_log_file(TITLE_IMAGE_DEFECT_LOG_PATH)
        search_selection_defect_lines = get_log_file(SEARCH_SELECTION_DEFECT_LOG_PATH)
        out_of_bound_defect_lines = get_log_file(OUT_OF_BOUND_DEFECT_LOG_PATH)

        title_image_defect_json = []
        search_selection_defect_json = []
        out_of_bound_defect_json = []

        for card in filtered_card_info:
            name = card["name"]
            if title_image_defect_lines and any(name in line for line in title_image_defect_lines):
                title_image_defect_json.append(card)
            if search_selection_defect_lines and any(name in line for line in search_selection_defect_lines):
                search_selection_defect_json.append(card)
            if out_of_bound_defect_lines and any(name in line for line in out_of_bound_defect_lines):
                out_of_bound_defect_json.append(card)

        if path_exists(TITLE_IMAGE_DEFECT_LOG_PATH):
            write_to_file(TITLE_IMAGE_DEFECT_JSON_PATH, json.dumps(title_image_defect_json))
        if path_exists(SEARCH_SELECTION_DEFECT_LOG_PATH):
            write_to_file(SEARCH_SELECTION_DEFECT_JSON_PATH, json.dumps(search_selection_defect_json))
        if(path_exists(OUT_OF_BOUND_DEFECT_LOG_PATH)):
            write_to_file(OUT_OF_BOUND_DEFECT_JSON_PATH, json.dumps(out_of_bound_defect_json))

def main():
    process_defect_logs()
    # generate_dump_debug_log()
    # generate_dump_sp_title_filtered_card_info()

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
