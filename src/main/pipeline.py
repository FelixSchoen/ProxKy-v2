import os
import re
import shutil
import zipfile

from src.main.configuration.variables import Regex, SUPPORTED_LAYOUTS, Paths, Id_Sets, DOUBLE_SIDED_LAYOUTS, Ids, Fonts
from src.main.data.card import Card
from src.main.data.fetcher import Fetcher
from src.main.handler.card_data_handler import set_card_name, set_type_line, set_mana_cost, set_value, set_artist, \
    set_collector_information, set_oracle_text, set_color_indicator, set_type_icon, set_artwork, set_planeswalker_text, \
    set_modal
from src.main.handler.card_layout_handler import layout_single_faced, layout_double_faced, layout_split, layout_basic, \
    layout_adventure, layout_transparent_body_art, layout_planeswalker
from src.main.handler.indesign_handler import _InDesignHandler
from src.main.handler.xml_handler import set_pdf
from src.main.utils.info import show_info, Info_Mode
from src.main.utils.misc import divide_into_chunks
from src.main.utils.mtg import get_clean_name, get_card_types


class Process_Mode:
    ADVENTURE = "adventure"
    REVERSIBLE = "reversible"


def parse_card_list(list_path: str) -> [dict]:
    """
    Parses a list of card names and flags, and returns a list of dictionary containing necessary information.
    :param list_path: Path to the decklist
    :return: The parsed data
    """
    show_info("Processing card list...")
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
                    if option_match.group("type") in ["set", "id", "cnr"]:
                        dictionary[option_match.group("type")] = option_match.group("id")
                    else:
                        options[option_match.group("type")] = option_match.group("id")

            fetcher = Fetcher.get_standard_fetcher()
            fetched_card = fetcher.fetch_card(dictionary)
            dictionary["card"] = fetched_card

            if fetched_card is not None:
                card_list.append(dictionary)
            else:
                show_info("Could not fetch card", prefix=dictionary["name"], mode=Info_Mode.ERROR, end_line=True)

    show_info("Successfully processed card list", end_line=True)
    return card_list


def process_card(card: Card, options: dict = None, indesign_handler: _InDesignHandler = None) -> None:
    """
    Handles processing of given card, like inserting information and adjusting layouts.
    :param card: The card to process
    :param options: Additional options
    :param indesign_handler: InDesign handler for converting a card to PDF
    """
    if card.layout not in SUPPORTED_LAYOUTS:
        show_info("Layout not supported", prefix=card.name, mode=Info_Mode.ERROR, end_line=True)
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
    if card.layout not in DOUBLE_SIDED_LAYOUTS and card.layout not in ["reversible_card"]:
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
    if card.layout in ["normal", "class", "saga"]:
        process_face(card, Id_Sets.ID_SET_FRONT)
    elif card.layout in DOUBLE_SIDED_LAYOUTS:
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
        process_face(card.card_faces[1], id_adventure_left, mode=Process_Mode.ADVENTURE)
    elif card.layout in ["token", "emblem"]:
        if card.oracle_text is None or len(card.oracle_text) == 0:
            layout_basic(Id_Sets.ID_SET_FRONT)
        process_face(card, Id_Sets.ID_SET_FRONT)
    elif card.layout in "reversible_card":
        process_face(card.card_faces[0], Id_Sets.ID_SET_FRONT, mode=Process_Mode.REVERSIBLE)
        process_face(card.card_faces[1], Id_Sets.ID_SET_BACK, mode=Process_Mode.REVERSIBLE)

    # Packaging
    shutil.make_archive(path_file, "zip", Paths.WORKING_MEMORY_CARD)
    try:
        os.remove(path_file_extension)
    except OSError:
        pass
    os.rename(path_file + ".zip", path_file + ".idml")
    shutil.rmtree(Paths.WORKING_MEMORY_CARD)

    # Convert to PDF
    show_info("Processing PDF...", prefix=card.name)
    indesign_handler.generate_pdf(card)

    show_info("Successfully processed", prefix=card.name, mode=Info_Mode.SUCCESS, end_line=True)


def process_face(card: Card, id_set: dict, mode: str = None) -> None:
    """
    Fills the given face with all the necessary information, e.g. title, oracle text, ...
    :param card: Card object containing the information
    :param id_set: Which id set to use
    :param mode: Specifies which special mode (e.g., adventure) to use
    """
    type_line = get_card_types(card)

    # Layouts
    if "Basic" in type_line:
        layout_basic(id_set)
    if "Planeswalker" in type_line:
        layout_planeswalker(id_set)

    # Common Attributes
    if Ids.ARTWORK_O in id_set:
        if mode == Process_Mode.REVERSIBLE:
            card_identifier = card.collector_number
            card_identifier += "a" if id_set == Id_Sets.ID_SET_FRONT else "b"
            set_artwork(card, id_set, card_identifier=card_identifier)
        else:
            set_artwork(card, id_set)

    set_type_icon(card, id_set)
    set_card_name(card, id_set, font_settings=Fonts.TITLE_ADVENTURE if mode == Process_Mode.ADVENTURE else dict())
    set_type_line(card, id_set, font_settings=Fonts.TYPE_LINE_ADVENTURE if mode == Process_Mode.ADVENTURE else None)
    set_mana_cost(card, id_set, font_settings=Fonts.MANA_COST_ADVENTURE if mode == Process_Mode.ADVENTURE else None)
    set_color_indicator(card, id_set)

    if "Planeswalker" in type_line:
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
        for i in range(0, int(card_entry["amount"])):
            if card.layout in DOUBLE_SIDED_LAYOUTS:
                cards_to_print.insert(0, card)
            else:
                cards_to_print.append(card)

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
            show_info("Could not delete file, error: {}".format(e), mode=Info_Mode.ERROR)
            return

    for i, page in enumerate(list(divide_into_chunks(cards_to_print, 8))):
        show_info("Processing print...")

        target_file_path = Paths.PRINT + "/page_" + str(i + 1).zfill(2)
        target_file_path_extension = target_file_path + ".idml"

        # Extract print template
        os.makedirs(Paths.PRINT, exist_ok=True)
        with zipfile.ZipFile(Paths.FILE_PRINT, "r") as archive:
            archive.extractall(Paths.WORKING_MEMORY_PRINT)

        for j, card in enumerate(page):
            clean_name = card.collector_number + " - " + get_clean_name(card.name)

            set_pdf(Id_Sets.ID_SET_PRINT_FRONT[Ids.PRINTING_FRAME_O][j], Id_Sets.ID_SET_PRINT_FRONT[Ids.SPREAD],
                    Paths.PDF + "/" + card.set.upper(), clean_name)

            if card.layout in DOUBLE_SIDED_LAYOUTS:
                set_pdf(Id_Sets.ID_SET_PRINT_BACK[Ids.PRINTING_FRAME_O][j], Id_Sets.ID_SET_PRINT_BACK[Ids.SPREAD],
                        Paths.PDF + "/" + card.set.upper(), clean_name, page=2)

        shutil.make_archive(target_file_path, "zip", Paths.WORKING_MEMORY_PRINT)
        try:
            os.remove(target_file_path_extension)
        except OSError:
            pass
        os.rename(target_file_path + ".zip", target_file_path + ".idml")
        shutil.rmtree(Paths.WORKING_MEMORY_PRINT)

    show_info("Successfully processed print", end_line=True)
