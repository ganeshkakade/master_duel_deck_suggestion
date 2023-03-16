# Master Duel Deck Suggestion (Yu-Gi-Oh!)

## Introduction
Welcome to the Master Duel Deck Suggestion project! This tool helps suggest possible deck archetypes based on the cards you own in Yu-Gi-Oh! Master Duel. This way, you can have more fun playing with different deck types without spending any extra points or money.

## Features
- Suggests popular, different, or fun deck archetypes based on the cards you own in-game.
- Provides information on the missing cards and the points needed to build the standard deck of that archetype.
- Provides information on which extra cards you can dismantle for more points. It recommends keeping plain foil cards instead of glossy or royal cards in exchange for points

## Usage

### Prerequisites
- Install [Tesseract-OCR (version 5.3)].
- Replace the installation path of Tesseract-OCR in the ```scripts\helpers.py``` file for the variable ```pytesseract.tesseract_cmd``` or set the environment ```Path``` variable to the same.

### Important Note
- Some of the scripts require GUI automation to gather card ownership information, which takes approximately 12 hours to gather. When executing these scripts, ensure not to interfere with the user interface. In case of exiting those scripts before their completion, you could use the ```Win + L``` shortcut.
- This tool only works on Windows.

### Steps
1. Clone the repository.
2. Run the following command to install the necessary dependencies:
```python
python setup.py install 
```
3. Run the command to get all updated cards and decks information:
```python
python master_duel_deck_suggestion\scripts\get_card_info.py
python master_duel_deck_suggestion\scripts\get_deck_type_info.py
```
4. Manually open ```Yu-Gi-Oh! Master Duel``` application, go to ```Game Settings -> General```, set Resolution to ```1920 x 1080``` and View Mode to ```Full Screen Mode```. (if ```1920 x 1080``` resolution option not available then anything near to that should be fine). Then go to ```Decks```, select ```Create New Deck -> Create New```.
5. Run the following command to get all updated cards owned information using GUI automation:
```python
python master_duel_deck_suggestion\scripts\get_card_owned_info_all.py
```
6. Run the following command to get the report for deck type suggestion and dismantlable extra cards, which should create .xlsx report files in the ```data``` folder:
```python
python master_duel_deck_suggestion\scripts\get_report.py 
```

Overall, this can be a useful addition to your Yu-Gi-Oh! Master Duel gameplay experience by providing suggestions for new and exciting deck archetypes.


[Tesseract-OCR (version 5.3)]: <https://tesseract-ocr.github.io/tessdoc/Downloads.html/>
