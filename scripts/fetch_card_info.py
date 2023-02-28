# note: card images can be accessed from link using id i.e https://s3.duellinksmeta.com/cards/{id}_w140.webp

import requests
import json
from helpers import logger, safe_open

def card_info(result=[], page=1):
    logger.debug(f"page: {page}")
    

    response = requests.get(f"https://www.masterduelmeta.com/api/v1/cards?cardSort=popRank&aggregate=search&page={page}&limit=2500")
    response.raise_for_status()
    responseJSON = response.json()

    if(not responseJSON):
        return result

    page = page + 1
    result = result + responseJSON

    logger.debug(f"result size: {len(result)}")

    return card_info(result, page)

if __name__ == '__main__':
    with safe_open("../data/card_info_data.json", "w") as json_file:
        json_file.write(json.dumps(card_info()))
