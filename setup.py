from setuptools import setup, find_packages

setup(
    name = 'master_duel_deck_suggestion',
    version = '1.0.0',
    description = 'Master Duel Deck Suggestion Based on Cards You Own In-Game',
    author = 'Ganesh Kakade',
    author_email = '',
    packages = find_packages(),
    install_requires = [
        'requests >= 2.28.0',
        'pyautogui >= 0.9.0',
        'pygetwindow',
        'xlsxwriter >= 3.0.0',
        'numpy >= 1.24.0',
        'pytesseract >= 0.3.0',
        'pillow >= 9.4.0',
        'opencv-python >= 4.7.0',
    ],
)