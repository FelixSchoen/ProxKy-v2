import argparse
import logging
import sys

from src.main.handler.indesign_handler import InDesignHandler
from src.main.pipeline import parse_card_list, process_card, process_print
from src.main.utils.id_generator import generate_ids
from src.main.utils.info import show_info, Info_Mode


def main(argv):
    config()
    args = parse_arguments()

    deck = args.deck

    if args.mode == "standard":
        if deck is None:
            deck = input("Please enter a deck name: ")

        card_entries = parse_card_list("data/decks/" + deck + ".txt")
        indesign_handler = InDesignHandler()

        for card_entry in card_entries:
            process_card(card_entry["card"], options=card_entry.get("options"), indesign_handler=indesign_handler)

        if not args.no_print:
            process_print(card_entries)
    elif args.mode == "generate_id":
        show_info("Generating ID list...")
        generate_ids()
        show_info("Generated ID list", mode=Info_Mode.SUCCESS, end_line=True)
    elif args.mode == "debug":
        pass
    else:
        show_info("Unknown mode", mode=Info_Mode.ERROR, end_line=True)


def parse_arguments():
    """
    Parses the program arguments.
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Proxy generator for Magic: The Gathering")

    parser.add_argument("mode", choices=["standard", "generate_id", "debug"],
                        help="Mode of operation of the program")
    parser.add_argument("--deck", "-d", nargs="?",
                        help="List of cards to parse, if not provided user will be prompted for list of cards at "
                             "runtime")
    parser.add_argument("--no_print", "-np", action="store_true", help="Disables generation of the print templates")

    args = parser.parse_args()
    return args


def config() -> None:
    """
    Configures certain aspects of the program, e.g., the logging module.
    """
    format = "[%(levelname)s] %(asctime)s: %(message)s"
    logging.basicConfig(format=format)


if __name__ == '__main__':
    main(sys.argv[1:])
