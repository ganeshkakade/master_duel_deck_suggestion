from collections import deque
from master_duel_deck_suggestion.scripts.helpers import path_exists, get_filepath
from master_duel_deck_suggestion.scripts.constants import TITLE_IMAGE_DEFECT

log_dir = get_filepath(__file__, "../logs")
DEBUG_LOG_PATH = log_dir / "debug.log"
DEFECT_LOG_PATH = log_dir / "defect.log"

def main():
    if path_exists(DEBUG_LOG_PATH):
        with open(DEBUG_LOG_PATH) as debug_log:
            with open(DEFECT_LOG_PATH, 'w') as defect_log:
                
                previous_lines = deque(maxlen=3)
                
                for line in debug_log:
                    if TITLE_IMAGE_DEFECT in line:
                        for previous_line in list(previous_lines)[:-1]:
                            defect_log.write(previous_line)
                        defect_log.write('\n') # batching defects

                    previous_lines.append(line)
    else:
        print("debug.log file does not exist")

if __name__ == '__main__':
    main()
