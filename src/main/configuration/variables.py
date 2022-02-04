import json

import requests

from src.main.configuration.config import CONFIG_ROOT_FOLDER, API_URL


class Fonts:
    TITLE = {"font": "Beleren2016", "size": "8", "style": "Bold"}


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
        "id_spread": "uce",
        "id_group_normal_o": "u505",
        "id_group_header_o": "u3f9",
        "id_group_footer_o": "u3fa",
        "id_type_icon_o": "u17b",
        "id_title_t": "u158",
        "id_type_line_t": "u1c1",
        "id_mana_cost_t": "u1a7",
        "id_color_indicator_top_o": "u2ed",
        "id_gradients_o": ['u105f', 'u1057'],
        "id_oracle_t": "u1da",
        "id_oracle_o": "u1ec",
        "id_color_indicator_bot_o": "u2836",
        "id_value_t": "u23f",
        "id_value_o": "u251",
        "id_artist_t": "u20c",
        "id_artist_o": "u209",
        "id_collector_information_t": "u229",
        "id_collector_information_o": "u225",
        "id_artwork_o": "u14d",
        "id_backdrop_o": "u12f5",
        "id_group_split_o": "u1835",
        "id_group_planeswalker_o": "u4ea",
        "id_group_adventure_o": "u3db",
        "id_name_t": "u3047",
        "id_modal_t": "u3fe",
        "id_modal_o": "u3fb",
        "id_planeswalker_value_t": ['u41b', 'u469', 'u497', 'u4ca'],
        "id_planeswalker_value_o": ['u42d', 'u466', 'u494', 'u4c7'],
        "id_planeswalker_oracle_numbered_t": ['u436', 'u452', 'u480', 'u4b3'],
        "id_planeswalker_oracle_numbered_o": ['u432', 'u44f', 'u47d', 'u4b0'],
        "id_planeswalker_oracle_final_t": "u4ef",
        "id_planeswalker_oracle_final_o": "u4ec",
    }
    ID_SET_SPLIT_TOP_FRONT = {
        "id_spread": "uce",
        "id_group_normal_o": "u152c",
        "id_group_header_o": "u16ef",
        "id_group_footer_o": "u1531",
        "id_type_icon_o": "u1736",
        "id_title_t": "u1722",
        "id_type_line_t": "u170b",
        "id_mana_cost_t": "u16f4",
        "id_color_indicator_top_o": "u16f0",
        "id_gradients_o": ['u1055', 'u1057'],
        "id_oracle_t": "u16c4",
        "id_oracle_o": "u16c1",
        "id_color_indicator_bot_o": "u1560",
        "id_value_t": "u1564",
        "id_value_o": "u1561",
        "id_artist_t": "u154c",
        "id_artist_o": "u1549",
        "id_collector_information_t": "u1535",
        "id_collector_information_o": "u1532",
        "id_artwork_o": "u152f",
        "id_backdrop_o": "u1530",
    }
    ID_SET_SPLIT_BOT_FRONT = {
        "id_spread": "uce",
        "id_group_normal_o": "u1768",
        "id_group_header_o": "u17e2",
        "id_group_footer_o": "u176c",
        "id_type_icon_o": "u182a",
        "id_title_t": "u1816",
        "id_type_line_t": "u17fe",
        "id_mana_cost_t": "u17e7",
        "id_color_indicator_top_o": "u17e3",
        "id_gradients_o": ['u1055', 'u1057'],
        "id_oracle_t": "u17b7",
        "id_oracle_o": "u17b4",
        "id_color_indicator_bot_o": "u179b",
        "id_value_t": "u179f",
        "id_value_o": "u179c",
        "id_artist_t": "u1787",
        "id_artist_o": "u1784",
        "id_collector_information_t": "u1770",
        "id_collector_information_o": "u176d",
        "id_artwork_o": "u176a",
        "id_backdrop_o": "u176b",
    }
    ID_SET_FRONT_ADVENTURE = {
        "id_spread": "uce",
        "id_type_icon_o": "u3d8",
        "id_title_t": "u3c4",
        "id_type_line_t": "u3ad",
        "id_mana_cost_t": "u396",
        "id_color_indicator_top_o": "u3df",
        "id_gradients_o": ['u2068', 'u2068'],
        "id_adventure_oracle_left_t": "u1065",
        "id_adventure_oracle_left_o": "u1062",
        "id_adventure_oracle_right_t": "u107e",
        "id_adventure_oracle_right_o": "u107b",
    }
    ID_SET_BACK = {
        "id_spread": "u4122",
        "id_group_normal_o": "u42b3",
        "id_group_header_o": "u4477",
        "id_group_footer_o": "u42b7",
        "id_type_icon_o": "u44be",
        "id_title_t": "u44aa",
        "id_type_line_t": "u4493",
        "id_mana_cost_t": "u447c",
        "id_color_indicator_top_o": "u4476",
        "id_gradients_o": ['u44e2', 'u44e5'],
        "id_oracle_t": "u444b",
        "id_oracle_o": "u4448",
        "id_color_indicator_bot_o": "u4447",
        "id_value_t": "u42d3",
        "id_value_o": "u42cf",
        "id_artist_t": "u42ea",
        "id_artist_o": "u42e7",
        "id_collector_information_t": "u42bb",
        "id_collector_information_o": "u42b8",
        "id_artwork_o": "u42b5",
        "id_backdrop_o": "u42b6",
        "id_group_split_o": "u4128",
        "id_group_planeswalker_o": "u4376",
        "id_group_adventure_o": "u42ff",
        "id_name_t": "u44c4",
        "id_modal_t": "u4462",
        "id_modal_o": "u445f",
        "id_planeswalker_value_t": ['u4433', 'u4405', 'u43d7', 'u43a9'],
        "id_planeswalker_value_o": ['u4430', 'u4402', 'u43d4', 'u43a6'],
        "id_planeswalker_oracle_numbered_t": ['u441c', 'u43ee', 'u43c0', 'u4392'],
        "id_planeswalker_oracle_numbered_o": ['u4419', 'u43eb', 'u43bd', 'u438f'],
        "id_planeswalker_oracle_final_t": "u437b",
        "id_planeswalker_oracle_final_o": "u4377",
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
    F_TEMPLATE = TEMPLATES + "/ProxKy.idml"
    F_PRINT = TEMPLATES + "/Print.idml"
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

    TEMPLATE_MANA = [([MANA], "font", ("KyMana", ""))]
    TEMPLATE_REGULAR = TEMPLATE_MANA.copy()
    TEMPLATE_REGULAR.append(
        ([r" ?\(.+\)"], "type", "reminder"))
    TEMPLATE_ORACLE = TEMPLATE_REGULAR.copy()
    TEMPLATE_ORACLE.append(
        (Magic.KEYWORDS, "font", ("Plantin MT Pro", "Italic")))
    TEMPLATE_PLANESWALKER = [([r"[\+|−]?(?:\d+|X): "], "type", "loyalty")]
    TEMPLATE_FLAVOR = [([r"\*(?:.)+\*"], "type", "normal")]

    LEVELER = r"[\"LEVEL [\d]+(-[\d]+|\+)\\n([\d]+|\*)/([\d]+|\*)\"]"
    NEWLINE = r"\n"

    CARD_ENTRY = r"^(?P<amount>\d+) (?P<name>.+?)(?P<flags> \[.+\])?$"
    CARD_OPTIONS = r"(?P<type>(?:.)+): (?P<id>(?:.)+)"
    CARD_NAME = r"^(?P<set>.+) - (?P<name>.+?)$"


# Supported Actions
SUPPORTED_LAYOUTS = ["normal", "modal_dfc", "transform", "split", "flip", "adventure", "class", "saga", "meld",
                     "token", "double_faced_token", "emblem"]
DOUBLE_SIDED_LAYOUTS = ["modal_dfc", "transform", "meld", "double_faced_token"]
SUPPORTED_MODES = ["standard", "generate_id"]

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
