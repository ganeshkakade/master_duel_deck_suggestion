import os
import pyautogui
import json
import pygetwindow
from PIL import Image
from pytesseract import pytesseract
import logging

# Create and configure logger
logging.basicConfig(filename="debug.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

path_to_tesseract = r"C:\Users\Username\AppData\Local\Tesseract-OCR\tesseract.exe" # tesseract.exe path

def text_to_image_match(name):
    image_path = f"./card_image_data/title_{name}.png"
    
    # Opening the image & storing it in an image object
    image = Image.open(image_path)
    
    # Providing the tesseract executable
    # location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract
    
    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(image).strip().lower()

    logger.debug(name)
    logger.debug(text)
    logger.debug(len(name))
    logger.debug(len(text))

    if(name == text or text in name):
       return True
    return False

def validate_select(name, repeat=0):
    take_title_screenshot(name)

    if(text_to_image_match(name) or repeat == 2): # max repeat limit 4 
        return True
    else:
        repeat = repeat + 1
        move_to_select(dx=85)
        validate_select(name, repeat)
    return False

def read_card_info_from_file():
    file = open('card_info_data.json')
    data = json.load(file)
    file.close()
    return data

def get_card_owned_info(card_info):
    card_owned = []

    for card in card_info:
        name = card.get("name").strip().lower()

        move_to_search()
        type_name_enter(name)
        move_to_select()

        if(validate_select(name)):
            take_screenshot(name) 
            # process more information from taken screenshot
        else:
            logger.debug(f"screenshot not taken. no image match found for the card name '{name}'")

    return card_owned

def take_title_screenshot(name):
    pyautogui.screenshot(f"./card_image_data/title_{name}.png", region=(82, 153, 330, 25)) # this need to change based on pc resolution. default 1920 x 1080

def take_screenshot(name):
    pyautogui.screenshot(f"./card_image_data/{name}.png")

def type_name_enter(name):
    pyautogui.typewrite(name)
    pyautogui.press("enter")

def move_to_select(x=1350, y=400, dx=0, dy=0):
    # move to searched card to select
    pyautogui.moveTo(x + dx, y + dy, duration = 1.5) # needs more time to load cards based on search
    pyautogui.click()
    
def move_to_search(x=1530, y=230):
    # move to search
    pyautogui.moveTo(x, y)
    pyautogui.click()

def switch_window():
    # switch to masterduel window
    handle = pygetwindow.getWindowsWithTitle('masterduel')[0]
    handle.activate()
    handle.maximize()

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == '__main__':
    card_owned_info = []
    card_info = read_card_info_from_file()

    create_dir("./card_image_data")
    create_dir("./card_match_data/")

    switch_window() 

    if(card_info): 
        card_owned_info = get_card_owned_info(card_info)
        logger.debug(card_owned_info)
