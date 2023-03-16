import xlsxwriter

from master_duel_deck_suggestion.scripts.helpers import (
    get_filepath,
    get_json_file,
    alnum_str
)
from master_duel_deck_suggestion.scripts.constants import (
    CARD_INFO_JSON,
    CARD_OWNED_INFO_JSON,
    FILTERED_DECK_TYPE_INFO_JSON,
    DISMANTLABLE_EXTRA_CARD_REPORT,
    DECK_TYPE_SUGGESTION_REPORT
)
from master_duel_deck_suggestion.tools.debugging import (
    logger
)

data_dir = get_filepath(__file__, "../data")

CARD_INFO_JSON_PATH = data_dir / CARD_INFO_JSON
CARD_OWNED_INFO_JSON_PATH = data_dir / CARD_OWNED_INFO_JSON
FILTERED_DECK_TYPE_INFO_JSON_PATH = data_dir / FILTERED_DECK_TYPE_INFO_JSON

DISMANTLABLE_EXTRA_CARD_REPORT_PATH = data_dir / DISMANTLABLE_EXTRA_CARD_REPORT
DECK_TYPE_SUGGESTION_REPORT_PATH = data_dir / DECK_TYPE_SUGGESTION_REPORT

def get_dismantlable_extra_card_report(card_info, card_owned_info):
    dismantlable_extra_card_workbook = xlsxwriter.Workbook(DISMANTLABLE_EXTRA_CARD_REPORT_PATH)

    ### dismantlable_extra_card_worksheet config
    dismantlable_extra_card_worksheet = dismantlable_extra_card_workbook.add_worksheet("Dismantlable Extra Cards")

    row = 0
    col = 0

    bold = dismantlable_extra_card_workbook.add_format({'bold': True})

    dismantlable_extra_card_worksheet.set_column(0, 0, 30)
    dismantlable_extra_card_worksheet.write(row, col, "Card Name", bold)
    dismantlable_extra_card_worksheet.write(row, col + 1, "Type", bold)
    dismantlable_extra_card_worksheet.write(row, col + 2, "Rarity", bold)
    dismantlable_extra_card_worksheet.write(row, col + 3, "Dismantlable Extras", bold)

    row += 1
    ### end

    for card in card_info:
        min_card = 3
        card_id = card.get('_id')
        card_name = card.get('name')
        card_type = card.get('type')
        card_rarity = card.get('rarity')
        card_ban_status = card.get('banStatus')
        if card_ban_status == "Limited 1":
            min_card = 1
        if card_ban_status == "Limited 2":
            min_card = 2
        extras = 0
        card_owned = next((c for c in card_owned_info if c.get('_id') == card_id), {})

        if card_owned:
            can_dismantle = card_owned.get('can_dismantle', 0)
            finish_owned = card_owned.get('basic_finish_owned', 0) + card_owned.get('glossy_finish_owned', 0) + card_owned.get('royal_finish_owned', 0)
            
            if finish_owned > min_card and can_dismantle > 0:
                if finish_owned - can_dismantle > min_card:
                    extras = can_dismantle
                else:
                    extras = finish_owned - min_card

        dismantlable_extra_card_worksheet.write(row, col, card_name)
        dismantlable_extra_card_worksheet.write(row, col + 1, card_type)
        dismantlable_extra_card_worksheet.write(row, col + 2, card_rarity)
        dismantlable_extra_card_worksheet.write(row, col + 3, extras)
        row += 1
    
    dismantlable_extra_card_worksheet.write(row, col, "Total", bold)
    dismantlable_extra_card_worksheet.write(row, col + 3, f"=SUM(D2:D{row})", bold)

    dismantlable_extra_card_workbook.close()

def get_deck_type_suggestion_report(card_info, card_owned_info):
    deck_type_info = get_json_file(FILTERED_DECK_TYPE_INFO_JSON_PATH)
    if deck_type_info:
        deck_type_suggestion_workbook = xlsxwriter.Workbook(DECK_TYPE_SUGGESTION_REPORT_PATH)

        ### deck_type_suggestion_worksheet config
        deck_type_suggestion_worksheet = deck_type_suggestion_workbook.add_worksheet("Deck Type Suggestion")

        row = 0
        col = 0

        bold = deck_type_suggestion_workbook.add_format({'bold': True})

        deck_type_suggestion_worksheet.set_column(0, 0, 15)
        deck_type_suggestion_worksheet.write(row, col, "Deck Name", bold)
        deck_type_suggestion_worksheet.write(row, col + 1, "Power", bold)
        deck_type_suggestion_worksheet.write(row, col + 2, "Avg Main Size", bold)
        deck_type_suggestion_worksheet.write(row, col + 3, "% Owned", bold) # UR, SR, R, N Need should be 0 for 100% Owned
        deck_type_suggestion_worksheet.write(row, col + 4, "UR Need", bold)
        deck_type_suggestion_worksheet.write(row, col + 5, "SR Need", bold)
        deck_type_suggestion_worksheet.write(row, col + 6, "R Need", bold)
        deck_type_suggestion_worksheet.write(row, col + 7, "N Need", bold)

        row += 1
        ### end

        for deck in deck_type_info:
            deck_name = deck.get('name')
            deck_power = deck.get('power')
            deck_breakdown = deck.get('deckBreakdown')
            deck_avg_main_size = deck_breakdown.get('avgMainSize')

            deck_cards = deck_breakdown.get('cards')
            filtered_deck_cards = [deck_card for deck_card in deck_cards if deck_card.get('aboveThresh') and deck_card.get('per') and deck_card.get('at')]
            
            total_card_need_ur_count = 0
            total_card_need_sr_count = 0
            total_card_need_r_count = 0
            total_card_need_n_count = 0
            total_card_owned_count = 0
            total_card_required_count = 0
            craft_point = 30

            ### deck_type_worksheet config
            deck_type_worksheet = deck_type_suggestion_workbook.add_worksheet(alnum_str(deck_name))

            deck_type_row = 0
            deck_type_col = 0

            deck_type_worksheet.set_column(0, 0, 30)
            deck_type_worksheet.write(deck_type_row, deck_type_col, "Card Name", bold)
            deck_type_worksheet.write(deck_type_row, deck_type_col + 1, "Type", bold)
            deck_type_worksheet.write(deck_type_row, deck_type_col + 2, "Rarity", bold)
            deck_type_worksheet.write(deck_type_row, deck_type_col + 3, "Size", bold)
            deck_type_worksheet.write(deck_type_row, deck_type_col + 4, "Need", bold)

            deck_type_row += 1
            ### end

            for deck_card in filtered_deck_cards:
                card_id = deck_card.get('card')
                card_required_count = deck_card.get('at')
                total_card_required_count = total_card_required_count + card_required_count

                card = next((c for c in card_info if c.get('_id') == card_id), {})
                card_owned = next((c for c in card_owned_info if c.get('_id') == card_id), {})

                card_name = card.get('name')
                card_type = card.get('type')
                card_rarity = card.get('rarity')
                card_owned_count = 0

                if card_owned:
                    card_owned_count = card_owned['basic_finish_owned'] + card_owned['glossy_finish_owned'] + card_owned['royal_finish_owned']
                    
                diff = card_required_count - card_owned_count
                if diff > 0:
                    if card_rarity == "UR":
                            total_card_need_ur_count = total_card_need_ur_count + diff
                    if card_rarity == "SR":
                            total_card_need_sr_count = total_card_need_sr_count + diff
                    if card_rarity == "R":
                            total_card_need_r_count = total_card_need_r_count + diff
                    if card_rarity == "N":
                            total_card_need_n_count  = total_card_need_n_count + diff
                else:
                    total_card_owned_count = total_card_owned_count + card_required_count

                deck_type_worksheet.write(deck_type_row, deck_type_col, card_name)
                deck_type_worksheet.write(deck_type_row, deck_type_col + 1, card_type)
                deck_type_worksheet.write(deck_type_row, deck_type_col + 2, card_rarity)
                deck_type_worksheet.write(deck_type_row, deck_type_col + 3, card_required_count)
                deck_type_worksheet.write(deck_type_row, deck_type_col + 4, diff if diff > 0 else 0)
                deck_type_row += 1

            card_owned_percent = round(total_card_owned_count * 100 / total_card_required_count, 0)
            card_need_ur_value = total_card_need_ur_count * craft_point
            card_need_sr_value = total_card_need_sr_count * craft_point
            card_need_r_value = total_card_need_r_count * craft_point
            card_need_n_value = total_card_need_n_count * craft_point

            deck_type_suggestion_worksheet.write(row, col, deck_name)
            deck_type_suggestion_worksheet.write(row, col + 1, deck_power)
            deck_type_suggestion_worksheet.write(row, col + 2, deck_avg_main_size)
            deck_type_suggestion_worksheet.write(row, col + 3, card_owned_percent)
            deck_type_suggestion_worksheet.write(row, col + 4, card_need_ur_value)
            deck_type_suggestion_worksheet.write(row, col + 5, card_need_sr_value)
            deck_type_suggestion_worksheet.write(row, col + 6, card_need_r_value)
            deck_type_suggestion_worksheet.write(row, col + 7, card_need_n_value)
            row += 1

        deck_type_suggestion_workbook.close()

def main():
    card_info = get_json_file(CARD_INFO_JSON_PATH)
    card_owned_info = get_json_file(CARD_OWNED_INFO_JSON_PATH)

    if card_info and card_owned_info:
        get_dismantlable_extra_card_report(card_info, card_owned_info)
        get_deck_type_suggestion_report(card_info, card_owned_info)

if __name__ == '__main__':
    try:
      main()
    except Exception as e:
      logger.exception(e)
