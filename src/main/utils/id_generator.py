import shutil
import zipfile
from xml.etree import ElementTree

from src.main.configuration.config import CONFIG_PATH_ID_FILE, CONFIG_FRONT_ID, CONFIG_BACK_ID, CONFIG_PRINT_FRONT_ID, \
    CONFIG_PRINT_BACK_ID
from src.main.configuration.variables import Paths, Id_Names, Ids


def generate_ids() -> None:
    """
    Automatically generates Ids of InDesign templates. This simply replaces manually searching for the entries.
    """
    open(CONFIG_PATH_ID_FILE, 'w').close()

    with zipfile.ZipFile(Paths.FILE_TEMPLATE, "r") as archive:
        archive.extractall(Paths.WORKING_MEMORY_CARD)
    with zipfile.ZipFile(Paths.FILE_PRINT, "r") as archive:
        archive.extractall(Paths.WORKING_MEMORY_PRINT)

    _fetch_ids("FRONT", CONFIG_FRONT_ID, Id_Names.GROUP_NORMAL)
    _fetch_ids("SPLIT_TOP_FRONT", CONFIG_FRONT_ID, Id_Names.GROUP_SPLIT_TOP, mode="split")
    _fetch_ids("SPLIT_BOT_FRONT", CONFIG_FRONT_ID, Id_Names.GROUP_SPLIT_BOT, mode="split")
    _fetch_ids("FRONT_ADVENTURE", CONFIG_FRONT_ID, Id_Names.GROUP_NORMAL, mode="adventure")
    _fetch_ids("BACK", CONFIG_BACK_ID, Id_Names.GROUP_NORMAL)
    _fetch_ids("PRINT_FRONT", CONFIG_PRINT_FRONT_ID, None, mode="printing")
    _fetch_ids("PRINT_BACK", CONFIG_PRINT_BACK_ID, None, mode="printing")

    shutil.rmtree(Paths.WORKING_MEMORY_CARD)
    shutil.rmtree(Paths.WORKING_MEMORY_PRINT)


def _fetch_ids(name, spread, root_element, mode="standard") -> None:
    """
    :param name: Name of the ID set to generate
    :param spread: Which spread to check the Ids on
    :param root_element: Root XML to search in, e.g. for split use only the split element as root
    :param mode: Which mode to generate Ids for, e.g. different treatment for split and double-sided cards
    :return: None
    For the names, each entry consists of a string to match in the actual document, the internal ID to match it to, a
    boolean that states whether it is a text box or not or a component to extract.
    """
    tree, base_tree = None, None

    if mode != "printing":
        tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread + ".xml")
        base_tree = tree
        if root_element is not None:
            tree = tree.find(".//*[@Name='" + root_element + "']")
    else:
        tree = ElementTree.parse(Paths.WORKING_MEMORY_PRINT + "/Spreads/Spread_" + spread + ".xml")

    # Ids base case
    names_base = [
        # Groups
        (Id_Names.GROUP_NORMAL, Ids.GROUP_NORMAL_O, "root"),
        (Id_Names.GROUP_HEADER, Ids.GROUP_HEADER_O),
        (Id_Names.GROUP_FOOTER, Ids.GROUP_FOOTER_O),

        # Header
        (Id_Names.TYPE_ICON, Ids.TYPE_ICON_O),
        (Id_Names.TITLE, Ids.TITLE_T, "ParentStory"),
        (Id_Names.TYPE_LINE, Ids.TYPE_LINE_T, "ParentStory"),
        (Id_Names.MANA_COST, Ids.MANA_COST_T, "ParentStory"),
        (Id_Names.COLOR_INDICATOR_TOP, Ids.COLOR_INDICATOR_TOP_O),
        (Id_Names.COLOR_INDICATOR_TOP, Ids.GRADIENTS_O, "FillColor"),
        (Id_Names.COLOR_INDICATOR_BOT, Ids.GRADIENTS_O, "FillColor"),

        # Body
        (Id_Names.ORACLE, Ids.ORACLE_T, "ParentStory"),
        (Id_Names.ORACLE, Ids.ORACLE_O),

        # Footer
        (Id_Names.COLOR_INDICATOR_BOT, Ids.COLOR_INDICATOR_BOT_O),
        (Id_Names.VALUE, Ids.VALUE_T, "ParentStory"),
        (Id_Names.VALUE, Ids.VALUE_O),
        (Id_Names.ARTIST_INFORMATION, Ids.ARTIST_INFORMATION_T, "ParentStory"),
        (Id_Names.ARTIST_INFORMATION, Ids.ARTIST_INFORMATION_O),
        (Id_Names.COLLECTOR_INFORMATION, Ids.COLLECTOR_INFORMATION_T, "ParentStory"),
        (Id_Names.COLLECTOR_INFORMATION, Ids.COLLECTOR_INFORMATION_O),
        (Id_Names.ARTWORK, Ids.ARTWORK_O),
        (Id_Names.BACKDROP, Ids.BACKDROP_O),
    ]

    # Ids to add for standard cards
    names_standard = [
        # Groups
        (Id_Names.GROUP_SPLIT, Ids.GROUP_SPLIT_O, "base_tree"),
        (Id_Names.GROUP_PLANESWALKER, Ids.GROUP_PLANESWALKER_O),
        (Id_Names.GROUP_ADVENTURE, Ids.GROUP_ADVENTURE_O),

        (Id_Names.NAME, Ids.NAME_T, "ParentStory"),
        (Id_Names.MODAL, Ids.MODAL_T, "ParentStory"),
        (Id_Names.MODAL, Ids.MODAL_O),

        (Id_Names.PLANESWALKER_VALUE_1, Ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (Id_Names.PLANESWALKER_VALUE_2, Ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (Id_Names.PLANESWALKER_VALUE_3, Ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (Id_Names.PLANESWALKER_VALUE_4, Ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (Id_Names.PLANESWALKER_VALUE_1, Ids.PLANESWALKER_VALUE_O),
        (Id_Names.PLANESWALKER_VALUE_2, Ids.PLANESWALKER_VALUE_O),
        (Id_Names.PLANESWALKER_VALUE_3, Ids.PLANESWALKER_VALUE_O),
        (Id_Names.PLANESWALKER_VALUE_4, Ids.PLANESWALKER_VALUE_O),
        (Id_Names.PLANESWALKER_ORACLE_1, Ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (Id_Names.PLANESWALKER_ORACLE_2, Ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (Id_Names.PLANESWALKER_ORACLE_3, Ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (Id_Names.PLANESWALKER_ORACLE_4, Ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (Id_Names.PLANESWALKER_ORACLE_1, Ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (Id_Names.PLANESWALKER_ORACLE_2, Ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (Id_Names.PLANESWALKER_ORACLE_3, Ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (Id_Names.PLANESWALKER_ORACLE_4, Ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (Id_Names.PLANESWALKER_ORACLE_FINAL, Ids.PLANESWALKER_ORACLE_FINAL_T, "ParentStory"),
        (Id_Names.PLANESWALKER_ORACLE_FINAL, Ids.PLANESWALKER_ORACLE_FINAL_O),

        # (Id_Names.MASK_COLOR_INDICATOR_BOT, Ids.MASK_COLOR_INDICATOR_BOT_O),
    ]

    # Ids to add for adventure cards
    names_adventure = [(Id_Names.ADVENTURE_TYPE_ICON, Ids.TYPE_ICON_O),
                       (Id_Names.ADVENTURE_TITLE, Ids.TITLE_T, "ParentStory"),
                       (Id_Names.ADVENTURE_TYPE_LINE, Ids.TYPE_LINE_T, "ParentStory"),
                       (Id_Names.ADVENTURE_MANA_COST, Ids.MANA_COST_T, "ParentStory"),
                       (Id_Names.ADVENTURE_COLOR_INDICATOR, Ids.COLOR_INDICATOR_TOP_O),
                       (Id_Names.ADVENTURE_COLOR_INDICATOR, Ids.GRADIENTS_O, "FillColor"),
                       # A bit hacky
                       (Id_Names.ADVENTURE_COLOR_INDICATOR, Ids.GRADIENTS_O, "FillColor"),
                       (Id_Names.ADVENTURE_ORACLE_LEFT, Ids.ADVENTURE_ORACLE_LEFT_T, "ParentStory"),
                       (Id_Names.ADVENTURE_ORACLE_LEFT, Ids.ADVENTURE_ORACLE_LEFT_O),
                       (Id_Names.ADVENTURE_ORACLE_RIGHT, Ids.ADVENTURE_ORACLE_RIGHT_T, "ParentStory"),
                       (Id_Names.ADVENTURE_ORACLE_RIGHT, Ids.ADVENTURE_ORACLE_RIGHT_O)
                       ]

    # Ids to use for printing
    names_printing = [
        (Id_Names.P_FRAME + " 1", Ids.PRINTING_FRAME_O),
        (Id_Names.P_FRAME + " 2", Ids.PRINTING_FRAME_O),
        (Id_Names.P_FRAME + " 3", Ids.PRINTING_FRAME_O),
        (Id_Names.P_FRAME + " 4", Ids.PRINTING_FRAME_O),
        (Id_Names.P_FRAME + " 5", Ids.PRINTING_FRAME_O),
        (Id_Names.P_FRAME + " 6", Ids.PRINTING_FRAME_O),
        (Id_Names.P_FRAME + " 7", Ids.PRINTING_FRAME_O),
        (Id_Names.P_FRAME + " 8", Ids.PRINTING_FRAME_O),
    ]

    names = names_base

    # Modes
    if mode == "standard":
        names.extend(names_standard)
    elif mode == "adventure":
        names = names_adventure
    elif mode == "printing":
        names = names_printing

    with open(CONFIG_PATH_ID_FILE, "a") as f:
        print("ID_SET_" + name + " = {", file=f)
        print("\"" + Ids.SPREAD + "\": " + "\"" + spread + "\",", file=f)

        entries = []

        for name in names:
            name_to_search_for = name[0]

            element = tree.find(".//*[@Name='" + name_to_search_for + "']")

            # Text box
            if len(name) > 2:
                # Get ID of root element
                if name[2] == "root":
                    to_add = "\"" + tree.attrib["Self"] + "\","
                # Get ID of element outside of current tree
                elif name[2] == "base_tree":
                    element = base_tree.find(".//*[@Name='" + name_to_search_for + "']")
                    to_add = "\"" + element.attrib["Self"] + "\","
                elif name[2] == "FillColor":
                    to_add = "\"" + element.attrib[name[2]].split("/")[1] + "\","
                else:
                    to_add = "\"" + element.attrib[name[2]] + "\","
            else:
                to_add = "\"" + element.attrib["Self"] + "\","

            entries.append(("\"" + name[1] + "\"", to_add))

        duplicates = dict()

        # Count occurrences
        for name in names:
            if name[1] not in duplicates:
                duplicates[name[1]] = 0
            duplicates[name[1]] += 1

        # Print non-duplicates
        carry = []
        previous_entry = ""
        for i, entry in enumerate(entries):
            key = entry[0].replace("\"", "")

            if len(carry) > 1 and entry[0] != previous_entry:
                print(previous_entry + ": " + str(carry) + ",", file=f)
                carry = []

            if duplicates[key] <= 1:
                print(entry[0] + ": " + entry[1], file=f)
            else:
                previous_entry = entry[0]
                carry.append(entry[1].split(",")[0].replace("\"", ""))

            if i == len(entries) - 1 and len(carry) > 1:
                print(previous_entry + ": " + str(carry) + ",", file=f)

        print("}", file=f)
