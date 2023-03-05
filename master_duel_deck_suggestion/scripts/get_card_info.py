# note: card images can be accessed from link using id i.e https://s3.duellinksmeta.com/cards/{id}_w140.webp
import requests
import json
from master_duel_deck_suggestion.scripts.helpers import get_filepath, makedirs, write_to_file
from master_duel_deck_suggestion.tools.debugging import logger

data_dir = get_filepath(__file__, "../data")
CARD_INFO_DATA_PATH = data_dir / "card_info.json"

makedirs(CARD_INFO_DATA_PATH)

def card_info(result=[], page=1):
    logger.debug(f"page: {page}")

    response = requests.get(f"https://www.masterduelmeta.com/api/v1/cards?cardSort=popRank&aggregate=search&page={page}&limit=2500")
    response.raise_for_status()
    responseJSON = response.json()

    if not responseJSON:
        return result
    
    page = page + 1
    result = result + responseJSON

    logger.debug(f"result size: {len(result)}")

    return card_info(result, page)

def main():
    write_to_file(CARD_INFO_DATA_PATH, json.dumps(card_info()))

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
