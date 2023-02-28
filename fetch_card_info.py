import requests
from json import dumps

# note: card images can be accessed from link using id i.e https://s3.duellinksmeta.com/cards/{id}_w140.webp

def card_info(result=[], page=1):
    response = requests.get(f"https://www.masterduelmeta.com/api/v1/cards?cardSort=popRank&aggregate=search&page={page}&limit=2500")
    response.raise_for_status()
    responseJSON = response.json()

    if(not responseJSON):
        return result
    
    page = page + 1
    result = result + responseJSON
    return card_info(result, page)

if __name__ == '__main__':
    with open("card_info_data.json", "w") as json_file:
        json_file.write(dumps(card_info()))
