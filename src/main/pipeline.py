import os
import re
import shutil
import zipfile
from time import sleep

from src.main.configuration.variables import Regex, SUPPORTED_LAYOUTS, Paths, Id_Sets
from src.main.data.card import Card
from src.main.info.info import show_info, Info_Mode
from src.main.utils.mtg import get_clean_name
from src.main.utils.card_data_modifier import set_card_name


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

    # TODO Adjust layouts

    # TODO Fill
    process_face(card, Id_Sets.ID_SET_FRONT)

    shutil.make_archive(path_file, "zip", Paths.WORKING_MEMORY_CARD)
    try:
        os.remove(path_file_extension)
    except OSError:
        pass
    os.rename(path_file + ".zip", path_file + ".idml")

    show_info("Successfully processed", prefix=card.name, mode=Info_Mode.SUCCESS, end_line=True)


def process_face(card: Card, id_set: dict) -> None:
    # Card Name
    set_card_name(card, id_set)
