# Master Duel Deck Suggestions (Yu-Gi-Oh!)

## Get all possible types of Master Duel deck suggestions based on the cards you own in-game

### Features
- Suggests whether it's possible to build different, popular, or fun deck archetypes played by other users using the cards you own. This way, you can have more fun playing other decks without spending any extra points or money.
- Provides information on which cards you don't own in order to build the standard deck of that archetype from the suggestions.
- Provides information on whether you can dismantle extra cards for more UR/SR/R/N points (ignoring the rarity of cards. Some might want to keep rather plain foil cards than royal/rare cards for exchange of points).

### Keep in mind
- Before running the scripts, make sure to install the required dependencies for the Python libraries used in scripts.
- Additionally, install Tesseract-OCR and take note of its installation path. Need to replace that path in ```fetch_card_owned_info.py``` file.
- To run the .py files, use Python and follow the steps provided to obtain the results.
- Keep in mind that some of the scripts may require GUI automation to gather cards information. When executing these scripts, make sure not to interfere with the UI.
- Keep in mind that the process may take a while to gather and process all the required data. Moreover, it's important to note that this tool is only supported on Windows.

### Steps
1. Run ```fetch_card_info.py``` to get all updated cards information in ```card_info_data.json``` file.
2. Manually open ```Yu-Gi-Oh! Master Duel``` application, go to ```Game Settings -> General```, set Resolution to 1920 x 1080 and View Mode to Window Mode. (Set PC screen resolution to 1920 x 1080 otherwise changes might need to be made within code for accuracy).
3. Go to ```Decks```, select ```Create New Deck -> Create New```, and set Sort filter to ```Number Owned``` in descending order.
4. Run ```fetch_card_owned_info.py``` to get information on all cards owned by you, which will help suggest possible decks to build.

[masterduelmeta.com]: <https://www.masterduelmeta.com/>
