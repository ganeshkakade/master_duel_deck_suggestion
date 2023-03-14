import json

import requests

from master_duel_deck_suggestion.scripts.helpers import get_filepath, makedirs, write_to_file
from master_duel_deck_suggestion.scripts.constants import DECK_TYPE_INFO_JSON, FILTERED_DECK_TYPE_INFO_JSON
from master_duel_deck_suggestion.tools.debugging import logger

data_dir = get_filepath(__file__, "../data")
DECK_TYPE_INFO_JSON_PATH = data_dir / DECK_TYPE_INFO_JSON
FILTERED_DECK_TYPE_INFO_JSON_PATH = data_dir / FILTERED_DECK_TYPE_INFO_JSON

makedirs(data_dir)

def get_deck_type_info(result=[]):
    response = requests.get(f"https://www.masterduelmeta.com/api/v1/deck-types?limit=2500")
    response.raise_for_status()
    responseJSON = response.json()

    if not responseJSON:
        return result

    result = result + responseJSON

    logger.debug(f"result size: {len(result)}")

    return result

def filter_deck_type_info(deck_type_info):
    filtered_deck_type_info = [o for o in deck_type_info if (not o.get('deckBreakdown').get('cards') == [])]
    return filtered_deck_type_info

def main():
    deck_type_info = get_deck_type_info()
    write_to_file(DECK_TYPE_INFO_JSON_PATH, json.dumps(deck_type_info))

    filtered_deck_type_info = filter_deck_type_info(deck_type_info)
    write_to_file(FILTERED_DECK_TYPE_INFO_JSON_PATH, json.dumps(filtered_deck_type_info))

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
