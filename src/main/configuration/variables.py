import json

import requests

from src.main.configuration.config import CONFIG_ROOT_FOLDER, API_URL
from src.main.utils.misc import mm_to_pt


class Distances:
    # Height of the modal plus the amount of distance between oracle and the modal box
    MODAL_HEIGHT = mm_to_pt(2.5 + 1.5)
    # Height of the Oracle Box
    ORACLE_HEIGHT = mm_to_pt(25.9)
    # Space between planeswalker text frames
    SPACE_PLANESWALKER = mm_to_pt(1.5)
    # How much to shift the elements for the basic layout
    LAYOUT_BASIC_SHIFT = mm_to_pt(29.9)
    # How much to enlarge the artwork in order to have it cover the entire card
    LAYOUT_FULL_ART_SHIFT = mm_to_pt(45.9)


class Fonts:
    MANA_COST = {"font": "KyMana", "size": "10", "style": "Regular", "leading": "8"}
    MANA_COST_ADVENTURE = {"font": "KyMana", "size": "7.5", "style": "Regular"}
    META = {"font": "Helvetica Now Var", "size": "4.5", "style": "Display"}
    MODAL = {"font": "Helvetica Now Var", "size": "5", "style": "Display"}
    NAME = {"font": "Helvetica Now Var", "size": "4.5", "style": "Display Bold"}
    ORACLE_REGULAR = {"font": "Plantin MT Pro", "size": "8", "style": "Regular"}
    ORACLE_KEYWORD = {"font": "Plantin MT Pro", "size": "8", "style": "Italic"}
    ORACLE_MANA = {"font": "KyMana", "size": "8", "style": "Regular"}
    ORACLE_REMINDER = {"font": "Plantin MT Pro", "size": "8", "style": "Italic"}
    ORACLE_FLAVOR = {"font": "Plantin MT Pro", "size": "8", "style": "Italic"}
    TITLE = {"font": "Beleren2016", "size": "8", "style": "Bold"}
    TITLE_ADVENTURE = {"font": "Beleren2016", "size": "6.5", "style": "Bold"}
    TYPE_LINE = {"font": "Helvetica Now Var", "size": "6", "style": "Display"}
    TYPE_LINE_ADVENTURE = {"font": "Helvetica Now Var", "size": "4.5", "style": "Display"}
    VALUE = {"font": "Beleren2016", "size": "10", "style": "Bold"}


class Ids:
    SPREAD = "id_spread"

    # Groups
    GROUP_NORMAL_O = "id_group_normal_o"
    GROUP_SPLIT_O = "id_group_split_o"
    GROUP_HEADER_O = "id_group_header_o"
    GROUP_BODY_O = "id_group_body_o"
    GROUP_PLANESWALKER_O = "id_group_planeswalker_o"
    GROUP_ADVENTURE_O = "id_group_adventure_o"
    GROUP_FOOTER_O = "id_group_footer_o"

    # Misc
    GRADIENTS_O = "id_gradients_o"

    # Header
    NAME_T = "id_name_t"
    TYPE_ICON_O = "id_type_icon_o"
    TITLE_T = "id_title_t"
    TYPE_LINE_T = "id_type_line_t"
    MANA_COST_T = "id_mana_cost_t"
    COLOR_INDICATOR_TOP_O = "id_color_indicator_top_o"

    # Body
    MODAL_T = "id_modal_t"
    MODAL_O = "id_modal_o"
    ORACLE_T = "id_oracle_t"
    ORACLE_O = "id_oracle_o"

    # Planeswalker
    PLANESWALKER_VALUE_T = "id_planeswalker_value_t"
    PLANESWALKER_VALUE_O = "id_planeswalker_value_o"
    PLANESWALKER_ORACLE_NUMBERED_T = "id_planeswalker_oracle_numbered_t"
    PLANESWALKER_ORACLE_NUMBERED_O = "id_planeswalker_oracle_numbered_o"
    PLANESWALKER_ORACLE_FINAL_T = "id_planeswalker_oracle_final_t"
    PLANESWALKER_ORACLE_FINAL_O = "id_planeswalker_oracle_final_o"

    # Adventure
    ADVENTURE_ORACLE_LEFT_T = "id_adventure_oracle_left_t"
    ADVENTURE_ORACLE_LEFT_O = "id_adventure_oracle_left_o"
    ADVENTURE_ORACLE_RIGHT_T = "id_adventure_oracle_right_t"
    ADVENTURE_ORACLE_RIGHT_O = "id_adventure_oracle_right_o"

    # Footer
    VALUE_T = "id_value_t"
    VALUE_O = "id_value_o"
    MASK_COLOR_INDICATOR_BOT_O = "id_mask_color_indicator_bot_o"
    COLOR_INDICATOR_BOT_O = "id_color_indicator_bot_o"
    ARTIST_INFORMATION_T = "id_artist_t"
    ARTIST_INFORMATION_O = "id_artist_o"
    COLLECTOR_INFORMATION_T = "id_collector_information_t"
    COLLECTOR_INFORMATION_O = "id_collector_information_o"

    # Artwork
    BACKDROP_O = "id_backdrop_o"
    ARTWORK_O = "id_artwork_o"

    PRINTING_FRAME_O = "pid_frame_o"


class Id_Names:
    # Groups
    GROUP_NORMAL = "Normal"
    GROUP_SPLIT = "Split"
    GROUP_SPLIT_TOP = "Split Top"
    GROUP_SPLIT_BOT = "Split Bot"
    GROUP_HEADER = "Header"
    GROUP_PLANESWALKER = "Layout Planeswalker"
    GROUP_ADVENTURE = "Layout Adventure"
    GROUP_FOOTER = "Footer"

    # Header
    NAME = "Name"
    TYPE_ICON = "Type Icon"
    TITLE = "Title"
    TYPE_LINE = "Type Line"
    MANA_COST = "Mana Cost"
    COLOR_INDICATOR_TOP = "Color Indicator Top"

    # Body
    MODAL = "Modal"
    ORACLE = "Oracle"

    # Planeswalker
    PLANESWALKER_VALUE_1 = "Planeswalker Value 1"
    PLANESWALKER_VALUE_2 = "Planeswalker Value 2"
    PLANESWALKER_VALUE_3 = "Planeswalker Value 3"
    PLANESWALKER_VALUE_4 = "Planeswalker Value 4"
    PLANESWALKER_ORACLE_1 = "Planeswalker Oracle 1"
    PLANESWALKER_ORACLE_2 = "Planeswalker Oracle 2"
    PLANESWALKER_ORACLE_3 = "Planeswalker Oracle 3"
    PLANESWALKER_ORACLE_4 = "Planeswalker Oracle 4"
    PLANESWALKER_ORACLE_FINAL = "Planeswalker Oracle"

    # Adventure
    ADVENTURE_TYPE_ICON = "Adventure Type Icon"
    ADVENTURE_TITLE = "Adventure Title"
    ADVENTURE_TYPE_LINE = "Adventure Type Line"
    ADVENTURE_MANA_COST = "Adventure Mana Cost"
    ADVENTURE_COLOR_INDICATOR = "Adventure Color Indicator"
    ADVENTURE_ORACLE_LEFT = "Adventure Oracle Left"
    ADVENTURE_ORACLE_RIGHT = "Adventure Oracle Right"

    # Footer
    VALUE = "Value"
    MASK_COLOR_INDICATOR_BOT = "Mask Color Indicator Bot"
    COLOR_INDICATOR_BOT = "Color Indicator Bot"
    ARTIST_INFORMATION = "Artist Information"
    COLLECTOR_INFORMATION = "Collector Information"

    BACKDROP = "Backdrop"
    ARTWORK = "Artwork"

    # Printing
    P_FRAME = "Frame"


class Id_Sets:
    ID_SET_FRONT = {
        "id_spread": "u119",
        "id_group_normal_o": "u539",
        "id_group_header_o": "u6e8",
        "id_group_footer_o": "u53d",
        "id_type_icon_o": "u72b",
        "id_title_t": "u716",
        "id_type_line_t": "u700",
        "id_mana_cost_t": "u6ea",
        "id_color_indicator_top_o": "u6e7",
        "id_gradients_o": ['ue3', 'ue2'],
        "id_oracle_t": "u6bc",
        "id_oracle_o": "u6ce",
        "id_color_indicator_bot_o": "u6ba",
        "id_value_t": "u555",
        "id_value_o": "u567",
        "id_artist_t": "u56c",
        "id_artist_o": "u57e",
        "id_collector_information_t": "u53f",
        "id_collector_information_o": "u551",
        "id_artwork_o": "u53b",
        "id_backdrop_o": "u53c",
        "id_group_split_o": "u120",
        "id_group_planeswalker_o": "u5f3",
        "id_group_adventure_o": "u582",
        "id_name_t": "u72f",
        "id_modal_t": "u6d2",
        "id_modal_o": "u6e4",
        "id_planeswalker_value_t": ['u6a5', 'u679', 'u64d', 'u621'],
        "id_planeswalker_value_o": ['u6b7', 'u68b', 'u65f', 'u633'],
        "id_planeswalker_oracle_numbered_t": ['u68f', 'u663', 'u637', 'u60b'],
        "id_planeswalker_oracle_numbered_o": ['u6a1', 'u675', 'u649', 'u61d'],
        "id_planeswalker_oracle_final_t": "u5f5",
        "id_planeswalker_oracle_final_o": "u607",
    }
    ID_SET_SPLIT_TOP_FRONT = {
        "id_spread": "u119",
        "id_group_normal_o": "u162c",
        "id_group_header_o": "u17f0",
        "id_group_footer_o": "u1630",
        "id_type_icon_o": "u1836",
        "id_title_t": "u1822",
        "id_type_line_t": "u180b",
        "id_mana_cost_t": "u17f4",
        "id_color_indicator_top_o": "u17ef",
        "id_gradients_o": ['ue1', 'ue2'],
        "id_oracle_t": "u17c4",
        "id_oracle_o": "u17c0",
        "id_color_indicator_bot_o": "u17bf",
        "id_value_t": "u164c",
        "id_value_o": "u1648",
        "id_artist_t": "u1663",
        "id_artist_o": "u1660",
        "id_collector_information_t": "u1634",
        "id_collector_information_o": "u1631",
        "id_artwork_o": "u162e",
        "id_backdrop_o": "u162f",
    }
    ID_SET_SPLIT_BOT_FRONT = {
        "id_spread": "u119",
        "id_group_normal_o": "u185c",
        "id_group_header_o": "u1a1f",
        "id_group_footer_o": "u1860",
        "id_type_icon_o": "u1a66",
        "id_title_t": "u1a52",
        "id_type_line_t": "u1a3b",
        "id_mana_cost_t": "u1a23",
        "id_color_indicator_top_o": "u1a1e",
        "id_gradients_o": ['u223c', 'u223f'],
        "id_oracle_t": "u19f3",
        "id_oracle_o": "u19f0",
        "id_color_indicator_bot_o": "u19ef",
        "id_value_t": "u187c",
        "id_value_o": "u1878",
        "id_artist_t": "u1893",
        "id_artist_o": "u1890",
        "id_collector_information_t": "u1864",
        "id_collector_information_o": "u1861",
        "id_artwork_o": "u185e",
        "id_backdrop_o": "u185f",
    }
    ID_SET_FRONT_ADVENTURE = {
        "id_spread": "u119",
        "id_type_icon_o": "u5f2",
        "id_title_t": "u5dd",
        "id_type_line_t": "u5c7",
        "id_mana_cost_t": "u5b1",
        "id_color_indicator_top_o": "u5af",
        "id_gradients_o": ['ue4', 'ue4'],
        "id_adventure_oracle_left_t": "u59a",
        "id_adventure_oracle_left_o": "u5ac",
        "id_adventure_oracle_right_t": "u584",
        "id_adventure_oracle_right_o": "u596",
    }
    ID_SET_BACK = {
        "id_spread": "u2240",
        "id_group_normal_o": "u2693",
        "id_group_header_o": "u2857",
        "id_group_footer_o": "u2697",
        "id_type_icon_o": "u289d",
        "id_title_t": "u2889",
        "id_type_line_t": "u2872",
        "id_mana_cost_t": "u285b",
        "id_color_indicator_top_o": "u2856",
        "id_gradients_o": ['u28ba', 'u2914'],
        "id_oracle_t": "u282b",
        "id_oracle_o": "u2828",
        "id_color_indicator_bot_o": "u2827",
        "id_value_t": "u26b3",
        "id_value_o": "u26af",
        "id_artist_t": "u26ca",
        "id_artist_o": "u26c7",
        "id_collector_information_t": "u269b",
        "id_collector_information_o": "u2698",
        "id_artwork_o": "u2695",
        "id_backdrop_o": "u2696",
        "id_group_split_o": "u2246",
        "id_group_planeswalker_o": "u2755",
        "id_group_adventure_o": "u26df",
        "id_name_t": "u28a3",
        "id_modal_t": "u2842",
        "id_modal_o": "u283f",
        "id_planeswalker_value_t": ['u2813', 'u27e5', 'u27b7', 'u2788'],
        "id_planeswalker_value_o": ['u2810', 'u27e2', 'u27b4', 'u2785'],
        "id_planeswalker_oracle_numbered_t": ['u27fc', 'u27ce', 'u27a0', 'u2771'],
        "id_planeswalker_oracle_numbered_o": ['u27f9', 'u27cb', 'u279c', 'u276d'],
        "id_planeswalker_oracle_final_t": "u2759",
        "id_planeswalker_oracle_final_o": "u2756",
    }
    ID_SET_PRINT_FRONT = {
        "id_spread": "ue9",
        "pid_frame_o": ['u101', 'u100', 'uff', 'ufe', 'ufd', 'ufc', 'ufb', 'ufa'],
    }
    ID_SET_PRINT_BACK = {
        "id_spread": "u102",
        "pid_frame_o": ['u10f', 'u10e', 'u10d', 'u10c', 'u10b', 'u10a', 'u109', 'u108'],
    }


class Paths:
    MAIN = CONFIG_ROOT_FOLDER
    ARTWORK = MAIN + "/Artwork"
    ARTWORK_DOWNLOADED = MAIN + "/Artwork (Downloaded)"
    DOCUMENTS = MAIN + "/Documents"
    PDF = MAIN + "/PDF"
    PRINT = MAIN + "/Print"
    RESOURCES = MAIN + "/Resources"
    ICONS = RESOURCES + "/Icons"
    CARD_TYPES = ICONS + "/Card Types"
    TEMPLATES = RESOURCES + "/Templates"
    FILE_TEMPLATE = TEMPLATES + "/ProxKy.idml"
    FILE_PRINT = TEMPLATES + "/Print.idml"
    _WORKING_MEMORY = MAIN + "/Working Memory"
    WORKING_MEMORY_CARD = _WORKING_MEMORY + "/Card"
    WORKING_MEMORY_PRINT = _WORKING_MEMORY + "/Print"


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Faces:
    FRONT = "front"
    BACK = "back"


class Magic:
    MANA_TYPES = ["W", "U", "B", "R", "G", "C"]
    KEYWORDS = json.loads(requests.get(API_URL + "/catalog/ability-words").text)["data"]


class Regex:
    MANA = r"(?P<match>{(?P<mana>[A-Z0-9\/◄►]+)})"
    ADD_MANA = r"(?P<match>(?P<req>(?:{[A-Z0-9\/]+})+)+: Add (?P<prod>(?:{(?:[A-Z0-9\/]+)})+))"

    TEMPLATE_MANA = [([MANA], "mana")]
    TEMPLATE_REGULAR = TEMPLATE_MANA.copy()
    TEMPLATE_REGULAR.append(
        ([r" ?\(.+\)"], "reminder"))
    TEMPLATE_ORACLE = TEMPLATE_REGULAR.copy()
    TEMPLATE_ORACLE.append(
        (Magic.KEYWORDS, "keyword"))
    TEMPLATE_PLANESWALKER = [([r"[\+|−]?(?:\d+|X): "], "loyalty")]
    TEMPLATE_FLAVOR = [([r"\*(?:.)+\*"], "normal")]
    TEMPLATE_BREAK = [("\n", "break")]

    LEVELER = r"[\"LEVEL [\d]+(-[\d]+|\+)\\n([\d]+|\*)/([\d]+|\*)\"]"
    NEWLINE = r"\n"

    CARD_ENTRY = r"^(?P<amount>\d+) (?P<name>.+?)(?P<flags> \[.+\])?$"
    CARD_OPTIONS = r"(?P<type>(?:.)+): (?P<id>(?:.)+)"
    CARD_NAME = r"^(?P<set>.+) - (?P<name>.+?)$"


# Supported Actions
SUPPORTED_LAYOUTS = ["normal", "modal_dfc", "transform", "split", "flip", "adventure", "class", "saga", "meld",
                     "token", "double_faced_token", "emblem", "reversible_card"]
DOUBLE_SIDED_LAYOUTS = ["modal_dfc", "transform", "meld", "double_faced_token"]
SUPPORTED_MODES = ["standard", "generate_id", "debug"]

# Image types to consider
IMAGE_TYPES = ["png", "jpg", "jpeg"]

# Mappings
MANA_MAPPING = {
    "{T}": "T",
    "{W}": "W",
    "{W/U}": "",
    "{W/B}": "",
    "{W/P}": "",
    "{2/W}": "",
    "{U}": "U",
    "{U/B}": "",
    "{U/R}": "",
    "{U/P}": "",
    "{2/U}": "",
    "{G/U/P}": "",
    "{B}": "B",
    "{B/R}": "",
    "{B/G}": "",
    "{B/P}": "",
    "{2/B}": "",
    "{R}": "R",
    "{R/G}": "",
    "{R/W}": "",
    "{R/P}": "",
    "{2/R}": "",
    "{G}": "G",
    "{G/W}": "",
    "{G/U}": "",
    "{G/P}": "",
    "{2/G}": "",
    "{C}": "C",
    "{P}": "P",
    "{0}": "0",
    "{1}": "1",
    "{2}": "2",
    "{3}": "3",
    "{4}": "4",
    "{5}": "5",
    "{6}": "6",
    "{7}": "7",
    "{8}": "8",
    "{9}": "9",
    "{10}": "",
    "{11}": "",
    "{12}": "",
    "{13}": "",
    "{14}": "",
    "{15}": "",
    "{16}": "",
    "{17}": "",
    "{18}": "",
    "{19}": "",
    "{20}": "",
    "{S}": "S",
    "{X}": "X",
    "{E}": "E",
    "{►}": "►",
    "{◄}": "◄",
}
COLOR_MAPPING = {
    "C": "Magic Grey",
    "W": "Magic White",
    "U": "Magic Blue",
    "B": "Magic Black",
    "R": "Magic Red",
    "G": "Magic Green"
}

# Array containing exactly those text frames that will be resized
RESIZE_INFORMATION = \
    {"resize": [
        [Id_Names.ORACLE],
        [Id_Names.PLANESWALKER_ORACLE_1, Id_Names.PLANESWALKER_ORACLE_2,
         Id_Names.PLANESWALKER_ORACLE_3, Id_Names.PLANESWALKER_ORACLE_4],
        [Id_Names.PLANESWALKER_ORACLE_FINAL],
        [Id_Names.ADVENTURE_ORACLE_LEFT],
        [Id_Names.ADVENTURE_ORACLE_RIGHT]
    ],
        "condense": [
            [Id_Names.ARTIST_INFORMATION],
            [Id_Names.COLLECTOR_INFORMATION],
        ]}
