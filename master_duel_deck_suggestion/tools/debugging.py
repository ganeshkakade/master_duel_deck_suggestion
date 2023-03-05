import logging

from master_duel_deck_suggestion.scripts.helpers import makedirs, get_filepath

log_dir = get_filepath(__file__, "../logs")
DEBUG_LOG_PATH = log_dir / "debug.log"

makedirs(DEBUG_LOG_PATH)

# create and configure logger
logging.basicConfig(filename=DEBUG_LOG_PATH,
                    format="%(asctime)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger()
