import os
import re
import shutil
import zipfile
from pathlib import Path

from proxky.main.configuration.variables import Regex, SUPPORTED_LAYOUTS, Paths, Id_Sets, \
    CONVENTIONAL_DOUBLE_SIDED_LAYOUTS, Ids, Fonts, DOUBLE_SIDED_LAYOUTS
from proxky.main.data.card import Card
from proxky.main.data.fetcher import Fetcher
from proxky.main.handler.card_data_handler import set_card_name, set_type_line, set_mana_cost, set_value, set_artist, \
    set_collector_information, set_oracle_text, set_color_indicator, set_type_icon, set_artwork, set_planeswalker_text, \
    set_modal
from proxky.main.handler.card_layout_handler import layout_single_faced, layout_double_faced, layout_split, \
    layout_basic, \
    layout_adventure, layout_transparent_body_art, layout_planeswalker
from proxky.main.handler.indesign_handler import _InDesignHandler
from proxky.main.handler.xml_handler import set_pdf, set_text_field, set_indd
from proxky.main.misc.enumerations import ProcessMode
from proxky.main.misc.logging import get_logger, format_message_cardname
from proxky.main.misc.mtg import get_clean_name, get_card_types, Type
from proxky.main.misc.util import divide_into_chunks, check_artwork_card_exists

LOGGER = get_logger()


def parse_card_list(list_path: Path) -> [dict]:
    """
    Parses a list of card names and flags, and returns a list of dictionary containing necessary information.
    :param list_path: Path to the decklist
    :return: The parsed data
    """
    card_list = []

    with open(list_path) as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == "#" or line.isspace():
                continue

            dictionary = dict()
            options = dict()
            match = re.match(Regex.CARD_ENTRY, line)

            dictionary["options"] = options
            dictionary["amount"] = match.group("amount")
            dictionary["name"] = match.group("name")

            option_string = match.group("flags")

            if option_string is not None:
                specified_options = option_string[2:-1].split(", ")

                for option in specified_options:
                    option_match = re.match(Regex.CARD_OPTIONS, option)
                    if option_match.group("type") in ["set", "id", "cn"]:
                        dictionary[option_match.group("type")] = option_match.group("id")
                    else:
                        options[option_match.group("type")] = option_match.group("id")

            fetcher = Fetcher.get_standard_fetcher()
            fetched_card = fetcher.fetch_card(dictionary)

            if fetched_card is None:
                LOGGER.error(f"Could not fetch {dictionary['name']}")
                continue

            # Check if local artwork exists
            if not check_artwork_card_exists(fetched_card) \
                    and any(check_artwork_card_exists(card_print) for card_print in fetched_card.prints) \
                    and not any(key in dictionary for key in ["set", "id", "cn"]):
                card_with_artwork = next(
                    card_print for card_print in fetched_card.prints if check_artwork_card_exists(card_print))
                dictionary["set"] = None
                dictionary["cn"] = None
                dictionary["id"] = card_with_artwork.id
                fetched_card = fetcher.fetch_card(dictionary)

            dictionary["card"] = fetched_card
            card_list.append(dictionary)

    return card_list


def process_card(card: Card, options: dict = None, indesign_handler: _InDesignHandler = None) -> None:
    """
    Handles processing of given card, like inserting information and adjusting layouts.
    :param card: The card to process
    :param options: Additional options
    :param indesign_handler: InDesign handler for converting a card to indd
    """
    LOGGER.info(format_message_cardname(card.name, "Processing..."))

    if card.layout not in SUPPORTED_LAYOUTS:
        LOGGER.error(format_message_cardname(card.name, f"Layout not supported: {card.layout}"))
        return

    # Setup folders
    path_folder = Paths.DOCUMENTS + "/" + card.set.upper()
    path_file = path_folder + "/" + card.collector_number + " - " + get_clean_name(card.name)
    path_file_extension = path_file + ".idml"

    # Extract XML file
    os.makedirs(path_folder, exist_ok=True)
    with zipfile.ZipFile(Paths.FILE_TEMPLATE, "r") as archive:
        archive.extractall(Paths.WORKING_MEMORY_CARD)

    # Layouts
    if card.layout not in DOUBLE_SIDED_LAYOUTS:
        layout_single_faced(Id_Sets.ID_SET_BACK)

    # Options
    if options is None:
        options = dict()

    if "tba" in options:
        if options["tba"] in ["front", "both"]:
            layout_transparent_body_art(Id_Sets.ID_SET_FRONT)
        if options["tba"] in ["back", "both"]:
            layout_transparent_body_art(Id_Sets.ID_SET_BACK)

    # Processing
    if card.layout in ["normal", "class", "saga", "leveler"]:
        process_face(card, Id_Sets.ID_SET_FRONT)
    elif card.layout in CONVENTIONAL_DOUBLE_SIDED_LAYOUTS:
        layout_double_faced([Id_Sets.ID_SET_FRONT, Id_Sets.ID_SET_BACK])
        set_modal(card, [Id_Sets.ID_SET_FRONT, Id_Sets.ID_SET_BACK])
        process_face(card.card_faces[0], Id_Sets.ID_SET_FRONT)
        process_face(card.card_faces[1], Id_Sets.ID_SET_BACK)
    elif card.layout in ["split", "flip"]:
        layout_split(Id_Sets.ID_SET_FRONT)
        process_face(card.card_faces[0], Id_Sets.ID_SET_SPLIT_TOP_FRONT)
        process_face(card.card_faces[1], Id_Sets.ID_SET_SPLIT_BOT_FRONT)
    elif card.layout in ["adventure"]:
        layout_adventure(Id_Sets.ID_SET_FRONT)

        id_adventure_right = Id_Sets.ID_SET_FRONT.copy()
        id_adventure_right[Ids.ORACLE_T] = Id_Sets.ID_SET_FRONT_ADVENTURE[Ids.ADVENTURE_ORACLE_RIGHT_T]
        id_adventure_right[Ids.ORACLE_O] = Id_Sets.ID_SET_FRONT_ADVENTURE[Ids.ADVENTURE_ORACLE_RIGHT_O]

        id_adventure_left = Id_Sets.ID_SET_FRONT_ADVENTURE.copy()
        id_adventure_left[Ids.ORACLE_T] = id_adventure_left[Ids.ADVENTURE_ORACLE_LEFT_T]

        process_face(card.card_faces[0], id_adventure_right)
        process_face(card.card_faces[1], id_adventure_left, mode=ProcessMode.ADVENTURE)
    elif card.layout in ["token", "emblem"]:
        if card.oracle_text is None or len(card.oracle_text) == 0:
            layout_basic(Id_Sets.ID_SET_FRONT)
        process_face(card, Id_Sets.ID_SET_FRONT)
    elif card.layout in ["reversible_card"]:
        process_face(card.card_faces[0], Id_Sets.ID_SET_FRONT, mode=ProcessMode.REVERSIBLE)
        process_face(card.card_faces[1], Id_Sets.ID_SET_BACK, mode=ProcessMode.REVERSIBLE)

    # Packaging
    shutil.make_archive(path_file, "zip", Paths.WORKING_MEMORY_CARD)
    try:
        os.remove(path_file_extension)
    except OSError:
        pass
    os.rename(path_file + ".zip", path_file + ".idml")
    shutil.rmtree(Paths.WORKING_MEMORY_CARD)

    # Convert to indd
    indesign_handler.generate_indd(card)

    LOGGER.info(format_message_cardname(card.name, "Successfully processed"))


def process_face(card: Card, id_set: dict, mode: str = None) -> None:
    """
    Fills the given face with all the necessary information, e.g. title, oracle text, ...
    :param card: Card object containing the information
    :param id_set: Which id set to use
    :param mode: Specifies which special mode (e.g., adventure) to use
    """
    card_types = get_card_types(card)

    # Layouts
    if Type.BASIC.value in card_types:
        layout_basic(id_set)
    if Type.PLANESWALKER.value in card_types:
        layout_planeswalker(id_set)

    # Common Attributes
    if Ids.ARTWORK_O in id_set:
        layout = None
        if mode == ProcessMode.REVERSIBLE:
            layout = "reversible_card"
        set_artwork(card, id_set, layout)

    set_type_icon(card, id_set)
    set_card_name(card, id_set, font_settings=Fonts.TITLE_ADVENTURE if mode == ProcessMode.ADVENTURE else dict())
    set_type_line(card, id_set, font_settings=Fonts.TYPE_LINE_ADVENTURE if mode == ProcessMode.ADVENTURE else None)
    set_mana_cost(card, id_set, font_settings=Fonts.MANA_COST_ADVENTURE if mode == ProcessMode.ADVENTURE else None)
    set_color_indicator(card, id_set)
    # set_background_indicator(card, id_set)

    if Type.PLANESWALKER.value in card_types:
        set_planeswalker_text(card, id_set)
    else:
        set_oracle_text(card, id_set, may_be_centered=card.layout not in ["adventure"])
    if Ids.VALUE_T in id_set:
        set_value(card, id_set)
    if Ids.ARTIST_INFORMATION_T in id_set:
        set_artist(card, id_set)
    if Ids.COLLECTOR_INFORMATION_T in id_set:
        set_collector_information(card, id_set)


def process_print(card_entries: [dict]) -> None:
    """
    Handles the printing of the card given in the list.
    :param card_entries: A list containing dictionaries containing information about the cards to print
    """
    cards_to_print = []

    # Determine which cards to print how often
    for card_entry in card_entries:
        card = card_entry["card"]
        options = card_entry["options"]
        if options is None:
            options = dict()

        for i in range(0, int(card_entry["amount"])):
            if card.layout in DOUBLE_SIDED_LAYOUTS or options.get("back", None) == "stock":
                cards_to_print.insert(0, card_entry)
            else:
                cards_to_print.append(card_entry)

    os.makedirs(Paths.PRINT, exist_ok=True)

    # Delete old files
    for filename in os.listdir(Paths.PRINT):
        file_path = os.path.join(Paths.PRINT, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            LOGGER.error(f"Could not delete file: {e}")
            return

    pages = list(divide_into_chunks(cards_to_print, 8))
    for i, page in enumerate(pages):
        target_file_path = Paths.PRINT + "/page_" + str(i + 1).zfill(2)
        target_file_path_extension = target_file_path + ".idml"

        # Extract print template
        os.makedirs(Paths.PRINT, exist_ok=True)
        with zipfile.ZipFile(Paths.FILE_PRINT, "r") as archive:
            archive.extractall(Paths.WORKING_MEMORY_PRINT)

        # Set cards
        for j, card_entry in enumerate(page):
            card = card_entry["card"]
            options = card_entry["options"]
            if options is None:
                options = dict()
            clean_name = card.collector_number + " - " + get_clean_name(card.name)

            set_indd(Id_Sets.ID_SET_PRINT_FRONT[Ids.PRINTING_FRAME_O][j], Id_Sets.ID_SET_PRINT_FRONT[Ids.SPREAD],
                     Paths.DOCUMENTS + "/" + card.set.upper(), clean_name, root_path=Paths.WORKING_MEMORY_PRINT)

            if card.layout in DOUBLE_SIDED_LAYOUTS:
                set_indd(Id_Sets.ID_SET_PRINT_BACK[Ids.PRINTING_FRAME_O][j], Id_Sets.ID_SET_PRINT_BACK[Ids.SPREAD],
                         Paths.DOCUMENTS + "/" + card.set.upper(), clean_name, root_path=Paths.WORKING_MEMORY_PRINT,
                         page=2)
            elif options.get("back", None) == "stock":
                set_pdf(Id_Sets.ID_SET_PRINT_BACK[Ids.PRINTING_FRAME_O][j], Id_Sets.ID_SET_PRINT_BACK[Ids.SPREAD],
                        Paths.TEMPLATES, "Back", root_path=Paths.WORKING_MEMORY_PRINT)

        # Set page indicator
        content_dict = {"content": f"Page {i + 1:02d}/{len(pages):02d}"}
        set_text_field(Id_Sets.ID_SET_PRINT_FRONT[Ids.PRINTING_PAGE_INDICATOR_T],
                       [([content_dict], {"justification": "RightAlign"})], root_path=Paths.WORKING_MEMORY_PRINT)

        shutil.make_archive(target_file_path, "zip", Paths.WORKING_MEMORY_PRINT)
        try:
            os.remove(target_file_path_extension)
        except OSError:
            pass
        os.rename(target_file_path + ".zip", target_file_path + ".idml")
        shutil.rmtree(Paths.WORKING_MEMORY_PRINT)
