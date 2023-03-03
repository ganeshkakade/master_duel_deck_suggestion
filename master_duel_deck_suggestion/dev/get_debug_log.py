import os
from collections import deque
from master_duel_deck_suggestion.scripts.helpers import safe_open
from master_duel_deck_suggestion.scripts.constants import TITLE_IMAGE_ERROR

file_dir = os.path.dirname(os.path.abspath(__file__))
DEBUG_LOG_PATH = os.path.join(file_dir, "../../debug.log")
DEFECT_LOG_PATH = os.path.join(file_dir, "../../defect.log")

def main():
    with safe_open(DEBUG_LOG_PATH) as debug_log:
        with safe_open(DEFECT_LOG_PATH, 'w') as defect_log:
            for line in debug_log:
                if TITLE_IMAGE_ERROR in line:
                    defect_log.write(line)

if __name__ == '__main__':
    main()