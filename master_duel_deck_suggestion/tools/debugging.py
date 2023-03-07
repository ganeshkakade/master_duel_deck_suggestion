import logging

from master_duel_deck_suggestion.scripts.helpers import makedirs, get_filepath
from master_duel_deck_suggestion.scripts.constants import (
    DEBUG_LOG,
    TITLE_IMAGE_DEFECT_LOG,
    SEARCH_SELECTION_DEFECT_LOG,
    OUT_OF_BOUND_DEFECT_LOG,
    FILE_CONFIG
)

log_dir = get_filepath(__file__, "../logs")

makedirs(log_dir)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(DEBUG_LOG)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_dir / DEBUG_LOG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

title_image_defect_logger = logging.getLogger(TITLE_IMAGE_DEFECT_LOG)
title_image_defect_logger.setLevel(logging.DEBUG)
title_image_defect_file_handler = logging.FileHandler(log_dir / TITLE_IMAGE_DEFECT_LOG, **FILE_CONFIG)
title_image_defect_file_handler.setFormatter(formatter)
title_image_defect_logger.addHandler(title_image_defect_file_handler)

search_selection_defect_logger = logging.getLogger(SEARCH_SELECTION_DEFECT_LOG)
search_selection_defect_logger.setLevel(logging.DEBUG)
search_selection_defect_file_handler = logging.FileHandler(log_dir / SEARCH_SELECTION_DEFECT_LOG, **FILE_CONFIG)
search_selection_defect_file_handler.setFormatter(formatter)
search_selection_defect_logger.addHandler(search_selection_defect_file_handler)

out_of_bound_defect_logger = logging.getLogger(OUT_OF_BOUND_DEFECT_LOG)
out_of_bound_defect_logger.setLevel(logging.DEBUG)
out_of_bound_defect_file_handler = logging.FileHandler(log_dir / OUT_OF_BOUND_DEFECT_LOG, **FILE_CONFIG)
out_of_bound_defect_file_handler.setFormatter(formatter)
out_of_bound_defect_logger.addHandler(out_of_bound_defect_file_handler)
