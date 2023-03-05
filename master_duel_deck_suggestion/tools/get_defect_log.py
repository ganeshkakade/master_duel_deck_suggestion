import json
from collections import deque
from pathlib import Path
from master_duel_deck_suggestion.scripts.helpers import path_exists, get_filepath, get_json_info, write_to_file, writelines_to_file, makedirs
from master_duel_deck_suggestion.scripts.constants import TITLE_IMAGE_DEFECT, SEARCH_RESULT_DEFECT, OUT_OF_BOUND_DEFECT

log_dir = get_filepath(__file__, "../logs")
data_dir = get_filepath(__file__, "../data")  

CARD_INFO_DATA_PATH = data_dir / "card_info.json"
DEBUG_LOG_PATH = log_dir / "debug.log"

TITLE_IMAGE_DEFECT_LOG_PATH = log_dir / "title_image_defect.log"
SEARCH_RESULT_DEFECT_LOG_PATH = log_dir / "search_result_defect.log"
OUT_OF_BOUND_DEFECT_LOG_PATH = log_dir / "out_of_bound_defect.log"

TITLE_IMAGE_DEFECT_JSON_PATH = log_dir / "title_image_defect.json"
SEARCH_RESULT_DEFECT_JSON_PATH = log_dir / "search_result_defect.json"
OUT_OF_BOUND_DEFECT_JSON_PATH = log_dir / "out_of_bound_defect.json"

makedirs(DEBUG_LOG_PATH)

def get_file_contents(file_path):
    if path_exists(file_path):
        with file_path.open() as file:
            return file.readlines()
    else:
        print(f"{file_path} file does not exists")

def process_defect_logs():
    card_info = get_json_info(CARD_INFO_DATA_PATH)
    if card_info:
        title_image_defect_lines = get_file_contents(TITLE_IMAGE_DEFECT_LOG_PATH)
        search_result_defect_lines = get_file_contents(SEARCH_RESULT_DEFECT_LOG_PATH)
        out_of_bound_defect_lines = get_file_contents(OUT_OF_BOUND_DEFECT_LOG_PATH)

        title_image_defect_json = []
        search_result_defect_json = []
        out_of_bound_defect_json = []

        for card in card_info:
            if title_image_defect_lines and any(card["name"] in line for line in title_image_defect_lines):
                title_image_defect_json.append(card)
            if search_result_defect_lines and any(card["name"] in line for line in search_result_defect_lines):
                search_result_defect_json.append(card)
            if out_of_bound_defect_lines and any(card["name"] in line for line in out_of_bound_defect_lines):
                out_of_bound_defect_json.append(card)

        write_to_file(TITLE_IMAGE_DEFECT_JSON_PATH, json.dumps(title_image_defect_json))
        write_to_file(SEARCH_RESULT_DEFECT_JSON_PATH, json.dumps(search_result_defect_json))
        write_to_file(OUT_OF_BOUND_DEFECT_JSON_PATH, json.dumps(out_of_bound_defect_json))

def process_debug_log():
    debug_lines = get_file_contents(DEBUG_LOG_PATH)
    if debug_lines:
        title_image_defect_lines = []
        search_result_defect_lines = []
        out_of_bound_defect_lines = []

        previous_lines = deque(maxlen=2)

        for line in debug_lines:
            if TITLE_IMAGE_DEFECT in line:
                title_image_defect_lines.extend(previous_lines)
                title_image_defect_lines.append(line)
                
            if SEARCH_RESULT_DEFECT in line:
                search_result_defect_lines.append(line)    

            if OUT_OF_BOUND_DEFECT in line:
                out_of_bound_defect_lines.append(line)

            previous_lines.append(line)

        writelines_to_file(TITLE_IMAGE_DEFECT_LOG_PATH, title_image_defect_lines) 
        writelines_to_file(SEARCH_RESULT_DEFECT_LOG_PATH, search_result_defect_lines)  
        writelines_to_file(OUT_OF_BOUND_DEFECT_LOG_PATH, out_of_bound_defect_lines) 

def main():
    process_debug_log()
    process_defect_logs()

if __name__ == '__main__':
    main()
