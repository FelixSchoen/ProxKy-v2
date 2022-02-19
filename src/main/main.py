import getopt
import logging
import sys

from configuration.variables import SUPPORTED_MODES
from src.main.handler.indesign_handler import InDesignHandler
from src.main.pipeline import parse_card_list, process_card, process_print
from src.main.utils.id_generator import generate_ids
from src.main.utils.info import show_info, Info_Mode


def main(argv):
    config()

    mode = ""
    deck = ""

    try:
        opts, args = getopt.getopt(argv, "m:d:", ["mode=", "deck="])
    except getopt.GetoptError:
        show_info("Invalid command line options", mode=Info_Mode.ERROR, end_line=True)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            mode = arg

            if mode not in SUPPORTED_MODES:
                show_info("Mode not supported", mode=Info_Mode.ERROR, end_line=True)
                return
        elif opt in ("-d", "--deck"):
            deck = arg
        else:
            show_info("Unknown command line option", mode=Info_Mode.ERROR, end_line=True)
            return

    if mode == "standard":
        if deck == "":
            deck = input("Please enter a deck name: ")
        card_entries = parse_card_list("data/decks/" + deck + ".txt")
        indesign_handler = InDesignHandler()
        for card_entry in card_entries:
            process_card(card_entry["card"], options=card_entry.get("options"), indesign_handler=indesign_handler)
        process_print(card_entries)
    elif mode == "generate_id":
        show_info("Generating ID list...")
        generate_ids()
        show_info("Generated ID list", mode=Info_Mode.SUCCESS, end_line=True)
    elif mode == "debug":
        pass
    else:
        show_info("Unknown mode", mode=Info_Mode.ERROR, end_line=True)


def config() -> None:
    """
    Configures certain aspects of the program, e.g., the logging module.
    """
    format = "[%(levelname)s] %(asctime)s: %(message)s"
    logging.basicConfig(format=format)


if __name__ == '__main__':
    main(sys.argv[1:])
