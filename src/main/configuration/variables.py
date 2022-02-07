import json

import requests

from src.main.configuration.config import CONFIG_ROOT_FOLDER, API_URL
from src.main.utils.misc import mm_to_pt


class Distances:
    # Height of the modal plus the amount of distance between oracle and the modal box
    MODAL_HEIGHT = 11.33858267717
    # Coordinates of the Oracle Box, in order to distribute planeswalker boxes
    ORACLE_TOP = -29.55631007189999
    ORACLE_BOT = ORACLE_TOP + 74.83464566929
    # Space between planeswalker text frames
    SPACE_PLANESWALKER = mm_to_pt(1.5)
    # How much to shift the elements for the basic layout
    LAYOUT_BASIC_SHIFT = mm_to_pt(30.15)
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
        "id_spread": "u11c",
        "id_group_normal_o": "u29a",
        "id_group_header_o": "u449",
        "id_group_footer_o": "u29e",
        "id_type_icon_o": "u48c",
        "id_title_t": "u477",
        "id_type_line_t": "u461",
        "id_mana_cost_t": "u44b",
        "id_color_indicator_top_o": "u448",
        "id_gradients_o": ['ue9', 'ue8'],
        "id_oracle_t": "u41d",
        "id_oracle_o": "u42f",
        "id_color_indicator_bot_o": "u41b",
        "id_value_t": "u2b6",
        "id_value_o": "u2c8",
        "id_artist_t": "u2cd",
        "id_artist_o": "u2df",
        "id_collector_information_t": "u2a0",
        "id_collector_information_o": "u2b2",
        "id_artwork_o": "u29c",
        "id_backdrop_o": "u29d",
        "id_group_split_o": "u1d35",
        "id_group_planeswalker_o": "u354",
        "id_group_adventure_o": "u2e3",
        "id_name_t": "u490",
        "id_modal_t": "u433",
        "id_modal_o": "u445",
        "id_planeswalker_value_t": ['u406', 'u3da', 'u3ae', 'u382'],
        "id_planeswalker_value_o": ['u418', 'u3ec', 'u3c0', 'u394'],
        "id_planeswalker_oracle_numbered_t": ['u3f0', 'u3c4', 'u398', 'u36c'],
        "id_planeswalker_oracle_numbered_o": ['u402', 'u3d6', 'u3aa', 'u37e'],
        "id_planeswalker_oracle_final_t": "u356",
        "id_planeswalker_oracle_final_o": "u368",
    }
    ID_SET_SPLIT_TOP_FRONT = {
        "id_spread": "u11c",
        "id_group_normal_o": "u189e",
        "id_group_header_o": "u1a62",
        "id_group_footer_o": "u18a2",
        "id_type_icon_o": "u1aa9",
        "id_title_t": "u1a95",
        "id_type_line_t": "u1a7e",
        "id_mana_cost_t": "u1a66",
        "id_color_indicator_top_o": "u1a60",
        "id_gradients_o": ['u1d14', 'u1d2e'],
        "id_oracle_t": "u1a35",
        "id_oracle_o": "u1a32",
        "id_color_indicator_bot_o": "u1a31",
        "id_value_t": "u18be",
        "id_value_o": "u18ba",
        "id_artist_t": "u18d5",
        "id_artist_o": "u18d2",
        "id_collector_information_t": "u18a6",
        "id_collector_information_o": "u18a3",
        "id_artwork_o": "u18a0",
        "id_backdrop_o": "u18a1",
    }
    ID_SET_SPLIT_BOT_FRONT = {
        "id_spread": "u11c",
        "id_group_normal_o": "u1adf",
        "id_group_header_o": "u1ca3",
        "id_group_footer_o": "u1ae3",
        "id_type_icon_o": "u1ce9",
        "id_title_t": "u1cd5",
        "id_type_line_t": "u1cbe",
        "id_mana_cost_t": "u1ca7",
        "id_color_indicator_top_o": "u1ca2",
        "id_gradients_o": ['u1d31', 'u1d34'],
        "id_oracle_t": "u1c77",
        "id_oracle_o": "u1c74",
        "id_color_indicator_bot_o": "u1c73",
        "id_value_t": "u1aff",
        "id_value_o": "u1afb",
        "id_artist_t": "u1b16",
        "id_artist_o": "u1b13",
        "id_collector_information_t": "u1ae7",
        "id_collector_information_o": "u1ae4",
        "id_artwork_o": "u1ae1",
        "id_backdrop_o": "u1ae2",
    }
    ID_SET_FRONT_ADVENTURE = {
        "id_spread": "u11c",
        "id_type_icon_o": "u353",
        "id_title_t": "u33e",
        "id_type_line_t": "u328",
        "id_mana_cost_t": "u312",
        "id_color_indicator_top_o": "u310",
        "id_gradients_o": ['uea', 'uea'],
        "id_adventure_oracle_left_t": "u2fb",
        "id_adventure_oracle_left_o": "u30d",
        "id_adventure_oracle_right_t": "u2e5",
        "id_adventure_oracle_right_o": "u2f7",
    }
    ID_SET_BACK = {
        "id_spread": "u1d36",
        "id_group_normal_o": "u218a",
        "id_group_header_o": "u234d",
        "id_group_footer_o": "u218e",
        "id_type_icon_o": "u2395",
        "id_title_t": "u2381",
        "id_type_line_t": "u2369",
        "id_mana_cost_t": "u2351",
        "id_color_indicator_top_o": "u234c",
        "id_gradients_o": ['u23b3', 'u23b5'],
        "id_oracle_t": "u2321",
        "id_oracle_o": "u231e",
        "id_color_indicator_bot_o": "u231d",
        "id_value_t": "u21aa",
        "id_value_o": "u21a6",
        "id_artist_t": "u21c1",
        "id_artist_o": "u21be",
        "id_collector_information_t": "u2192",
        "id_collector_information_o": "u218f",
        "id_artwork_o": "u218c",
        "id_backdrop_o": "u218d",
        "id_group_split_o": "u1d3c",
        "id_group_planeswalker_o": "u224d",
        "id_group_adventure_o": "u21d6",
        "id_name_t": "u239b",
        "id_modal_t": "u2338",
        "id_modal_o": "u2335",
        "id_planeswalker_value_t": ['u2309', 'u22db', 'u22ad', 'u227f'],
        "id_planeswalker_value_o": ['u2306', 'u22d8', 'u22aa', 'u227c'],
        "id_planeswalker_oracle_numbered_t": ['u22f2', 'u22c4', 'u2296', 'u2268'],
        "id_planeswalker_oracle_numbered_o": ['u22ef', 'u22c1', 'u2293', 'u2265'],
        "id_planeswalker_oracle_final_t": "u2251",
        "id_planeswalker_oracle_final_o": "u224e",
    }
    ID_SET_PRINT_FRONT = {
        "id_spread": "ue7",
        "pid_frame_o": ['uf5', 'u114', 'u115', 'u119', 'u118', 'u117', 'u11c', 'u11b'],
    }
    ID_SET_PRINT_BACK = {
        "id_spread": "u16c",
        "pid_frame_o": ['u17d', 'u17c', 'u17b', 'u17a', 'u179', 'u178', 'u177', 'u176'],
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
                     "token", "double_faced_token", "emblem"]
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
