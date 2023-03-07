# note: card images can be accessed from link using id i.e https://s3.duellinksmeta.com/cards/{id}_w140.webp
import json

import requests

from master_duel_deck_suggestion.scripts.helpers import get_filepath, makedirs, write_to_file
from master_duel_deck_suggestion.scripts.constants import CARD_INFO_JSON, FILTERED_CARD_INFO_JSON
from master_duel_deck_suggestion.tools.debugging import logger

data_dir = get_filepath(__file__, "../data")
CARD_INFO_DATA_PATH = data_dir / CARD_INFO_JSON
FILTERED_CARD_INFO_DATA_PATH = data_dir / FILTERED_CARD_INFO_JSON

makedirs(data_dir)

def get_card_info(result=[], page=1):
    logger.debug(f"page: {page}")

    response = requests.get(f"https://www.masterduelmeta.com/api/v1/cards?cardSort=popRank&aggregate=search&page={page}&limit=2500")
    response.raise_for_status()
    responseJSON = response.json()

    if not responseJSON:
        return result
    
    page = page + 1
    result = result + responseJSON

    logger.debug(f"result size: {len(result)}")

    return get_card_info(result, page)

def filter_card_info(card_info):
    filtered_card_info = [o for o in card_info if (not o.get("obtain") == []) and (not o.get("banStatus") == "Forbidden") and (not o.get("alternateArt") == True)]
    return filtered_card_info

def main():
    card_info = get_card_info()
    write_to_file(CARD_INFO_DATA_PATH, json.dumps(card_info))

    filtered_card_info = filter_card_info(card_info)
    write_to_file(FILTERED_CARD_INFO_DATA_PATH, json.dumps(filtered_card_info))

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
