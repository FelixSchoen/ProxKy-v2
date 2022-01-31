from src.main.configuration.config import CONFIG_ROOT_FOLDER


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
    WORKING_MEMORY = MAIN + "/Working Memory"


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


# Supported Actions
SUPPORTED_LAYOUTS = ["normal", "modal_dfc", "transform", "split", "flip", "adventure", "class", "saga", "meld",
                     "token", "double_faced_token", "emblem"]
DOUBLE_SIDED_LAYOUTS = ["modal_dfc", "transform", "meld", "double_faced_token"]
SUPPORTED_MODES = ["standard", "generate_ids"]
