import xlsxwriter

from master_duel_deck_suggestion.scripts.helpers import (
    get_filepath,
    get_json_file
)
from master_duel_deck_suggestion.scripts.constants import (
    CARD_OWNED_INFO_JSON,
    DECK_TYPE_INFO_JSON,
    DISMANTLABLE_EXTRA_CARD_REPORT,
    DECK_TYPE_SUGGESTION_REPORT
)
from master_duel_deck_suggestion.tools.debugging import (
    logger
)

data_dir = get_filepath(__file__, "../data")

CARD_OWNED_INFO_JSON_PATH = data_dir / CARD_OWNED_INFO_JSON
DECK_TYPE_INFO_JSON_PATH = data_dir / DECK_TYPE_INFO_JSON

DISMANTLABLE_EXTRA_CARD_REPORT_PATH = data_dir / DISMANTLABLE_EXTRA_CARD_REPORT
DECK_TYPE_SUGGESTION_REPORT_PATH = data_dir / DECK_TYPE_SUGGESTION_REPORT

def get_dismantlable_extra_card_report(card_owned_info):
    dismantlable_extra_card_workbook = xlsxwriter.Workbook(DISMANTLABLE_EXTRA_CARD_REPORT_PATH)
    dismantlable_extra_card_worksheet = dismantlable_extra_card_workbook.add_worksheet("Dismantlable Extra Cards")

    row = 0
    col = 0
    min_card = 3

    bold = dismantlable_extra_card_workbook.add_format({'bold': True})

    dismantlable_extra_card_worksheet.set_column(0, 0, 30)
    dismantlable_extra_card_worksheet.write(row, col, "Card Name", bold)
    dismantlable_extra_card_worksheet.write(row, col + 1, "Extras", bold)

    row += 1

    for card in card_owned_info:
        can_dismantle = card.get('can_dismantle')
        if can_dismantle > min_card:
            dismantlable_extra_card_worksheet.write(row, col, card.get('name'))
            dismantlable_extra_card_worksheet.write(row, col + 1, can_dismantle - min_card)
            row += 1
    
    dismantlable_extra_card_worksheet.write(row, col, "Total", bold)
    dismantlable_extra_card_worksheet.write(row, col + 1, f"=SUM(B2:B{row})", bold)

    dismantlable_extra_card_workbook.close()

def get_deck_type_suggestion_report(card_owned_info):
    deck_type_info = get_json_file(DECK_TYPE_INFO_JSON_PATH)
    if deck_type_info:
        deck_type_suggestion_workbook = xlsxwriter.Workbook(DECK_TYPE_SUGGESTION_REPORT_PATH)
        deck_type_suggestion_worksheet = deck_type_suggestion_workbook.add_worksheet("Deck Type Suggestions")

        row = 0
        col = 0

        bold = deck_type_suggestion_workbook.add_format({'bold': True})

        deck_type_suggestion_worksheet.set_column(0, 0, 15)
        deck_type_suggestion_worksheet.write(row, col, "Deck Name", bold)
        deck_type_suggestion_worksheet.write(row, col + 1, "% Owned", bold)
        deck_type_suggestion_worksheet.write(row, col + 2, "UR Need", bold)
        deck_type_suggestion_worksheet.write(row, col + 3, "SR Need", bold)
        deck_type_suggestion_worksheet.write(row, col + 4, "R Need", bold)
        deck_type_suggestion_worksheet.write(row, col + 5, "N Need", bold)

        row += 1

        for deck in deck_type_info:
            deck_type_suggestion_worksheet.write(row, col, deck.get('name'))
            deck_type_suggestion_worksheet.write(row, col + 1, 0)
            deck_type_suggestion_worksheet.write(row, col + 2, 0)
            deck_type_suggestion_worksheet.write(row, col + 3, 0)
            deck_type_suggestion_worksheet.write(row, col + 4, 0)
            deck_type_suggestion_worksheet.write(row, col + 5, 0)
            row += 1
    
        deck_type_suggestion_workbook.close()

def main():
    card_owned_info = get_json_file(CARD_OWNED_INFO_JSON_PATH)
    if card_owned_info:
        get_dismantlable_extra_card_report(card_owned_info)
        get_deck_type_suggestion_report(card_owned_info)

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
