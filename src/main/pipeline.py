import os
import re
import shutil
import zipfile

from src.main.configuration.variables import Regex, SUPPORTED_LAYOUTS, Paths, Id_Sets, DOUBLE_SIDED_LAYOUTS, Ids, Fonts
from src.main.data.card import Card
from src.main.handler.card_layout_handler import layout_single_faced, layout_double_faced, layout_split, layout_basic, \
    layout_adventure, layout_transparent_body_art
from src.main.info.info import show_info, Info_Mode
from src.main.utils.mtg import get_clean_name, get_card_types
from src.main.handler.card_data_handler import set_card_name, set_type_line, set_mana_cost, set_value, set_artist, \
    set_collector_information, set_oracle_text, set_color_indicator, set_type_icon, set_artwork, set_planeswalker_text, \
    set_modal


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

            card_list.append(dictionary)

        return card_list


def process_card(card: Card, options: dict = None) -> None:
    """
    Handles processing of given card, like inserting information and adjusting layouts.
    :param card: The card to process
    :param options: Additional options
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
    with zipfile.ZipFile(Paths.F_TEMPLATE, "r") as archive:
        archive.extractall(Paths.WORKING_MEMORY_CARD)

    # Layouts
    if card.layout not in DOUBLE_SIDED_LAYOUTS:
        layout_single_faced(Id_Sets.ID_SET_BACK)
    if "Basic" in get_card_types(card):
        layout_basic(Id_Sets.ID_SET_FRONT)

    # Options
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
        process_face(card.card_faces[1], id_adventure_left, mode="adventure")
    elif card.layout in ["token", "emblem"]:
        if card.oracle_text is None or len(card.oracle_text) == 0:
            layout_basic(Id_Sets.ID_SET_FRONT)
        process_face(card, Id_Sets.ID_SET_FRONT)

    # Packaging
    shutil.make_archive(path_file, "zip", Paths.WORKING_MEMORY_CARD)
    try:
        os.remove(path_file_extension)
    except OSError:
        pass
    os.rename(path_file + ".zip", path_file + ".idml")

    show_info("Successfully processed", prefix=card.name, mode=Info_Mode.SUCCESS, end_line=True)


def process_face(card: Card, id_set: dict, mode: str = None) -> None:
    """
    Fills the given face with all the necessary information, e.g. title, oracle text, ...
    :param card: Card object containing the information
    :param id_set: Which id set to use
    :param mode: Specifies which special mode (e.g., adventure) to use
    """
    type_line = get_card_types(card)

    # Common Attributes
    if Ids.ARTWORK_O in id_set:
        set_artwork(card, id_set)

    set_type_icon(card, id_set)
    set_card_name(card, id_set, font_settings=Fonts.TITLE_ADVENTURE if mode == "adventure" else dict())
    set_type_line(card, id_set, font_settings=Fonts.TYPE_LINE_ADVENTURE if mode == "adventure" else None)
    set_mana_cost(card, id_set, font_settings=Fonts.MANA_COST_ADVENTURE if mode == "adventure" else None)
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