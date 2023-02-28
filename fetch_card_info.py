import requests
import json

# note: card image can be fetched with link using id as https://s3.duellinksmeta.com/cards/{id}_w140.webp

def card_info(result=[], page=0):
    response = requests.get(f"https://www.masterduelmeta.com/api/v1/cards?page={page}&limit=3000")
    response.raise_for_status()
    responseJSON = response.json()

    if(not responseJSON):
        return json.dumps(result)
    else:
        page = page + 1
        result = result + responseJSON
        card_info(result, page)
    return json.dumps(result)       

if __name__ == '__main__':
    jsonFile = open("card_info_data.json", "w")
    jsonFile.write(card_info())
    jsonFile.close()
