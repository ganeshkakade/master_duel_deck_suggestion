from setuptools import setup, find_packages

setup(
    name = 'master_duel_deck_suggestion',
    version = '1.0.0',
    description = 'Master Duel Deck Suggestion Based on Cards You Own In-Game',
    author = 'Ganesh Kakade',
    author_email = '',
    packages = find_packages(),
    install_requires = [
        'requests',
        'pyautogui',
        'pygetwindow',
        'xlsxwriter',
        'numpy',
        'pytesseract',
        'pillow',
        'opencv-python',
    ],
)