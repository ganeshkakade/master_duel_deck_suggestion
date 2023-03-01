# note: card images can be accessed from link using id i.e https://s3.duellinksmeta.com/cards/{id}_w140.webp

import requests
import json
from helpers import logger, safe_open
from constants import CARD_INFO_DATA_PATH
# import time
# import timing

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
    with safe_open(CARD_INFO_DATA_PATH, 'w') as json_file:
        json_file.write(json.dumps(card_info(), indent=4))

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
