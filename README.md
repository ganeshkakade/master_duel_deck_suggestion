# Master Duel Deck Suggestions (Yu-Gi-Oh!)

## Get all possible types of Master Duel deck suggestions based on the cards you own in-game.

### Features
- Suggests whether it is possible to build different types of decks using the cards you own, so you can have more fun playing other decks without spending extra points or money.
- Provides information on which cards you don't own in order to build the standard deck of that archetype from the suggestions.
- Provides information on whether you can dismantle extra cards for more UR/SR/R/N points (ignore the rarity of cards. Some might want to keep rather plain foil cards than royal/rare cards for exchange of points).

### What it does:
- Updates the Yu-Gi-Oh! Master Duel cards' information from [masterduelmeta.com] for reference.
- Obtains information about the cards owned by you in-game using gui automation.
- Gets information about different/fun/unique/popular deck archetypes played by users in the past/present.
- Creates suggestions for possible deck types based on the cards you own.


### Keep in mind
- Before running the scripts, make sure to install the required dependencies for the Python libraries used in scripts.
- Additionally, install Tesseract-OCR and take note of its installation path. Need to replace that path in ```fetch_card_owned_info.py``` file
- To run the .py files, use Python and follow the steps provided to obtain the results.
- Keep in mind that some of the scripts may require GUI automation to gather cards information. When executing these scripts, make sure not to interfere with the UI.
- Please note that the process may take some time to fetch all the required information

### Steps
1. Run ```fetch_card_info.py``` to get all updated cards information in ```card_info_data.json file```.
2. Manually open ```Yu-Gi-Oh! Master Duel``` application, go to ```Game Settings -> General```, set Resolution to ```1920 x 1080 and View Mode to Window Mode. (Set PC screen resolution to 1920 x 1080 otherwise changes need to be made within code for precision).
3. Go to ```Decks```, select ```Create New Deck -> Create New```, and set Sort filter to ```Number Owned``` in descending order.
4. Run ```fetch_card_owned_info.py``` to get information on all cards owned by you, which will help suggest possible decks to build.

[masterduelmeta.com]: <https://www.masterduelmeta.com/>