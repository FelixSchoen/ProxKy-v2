import argparse
from pathlib import Path

from proxky.handler.indesign_handler import InDesignHandler
from proxky.misc.enumerations import InfoMode
from proxky.misc.id_generator import generate_ids
from proxky.misc.logging import get_logger
from proxky.main.pipeline import parse_card_list, process_card, process_print

LOGGER = get_logger()


def main():
    args = parse_arguments()

    if args.command == "generate":
        deck_identifier = args.deck

        if deck_identifier is None:
            deck_identifier = input("Please enter the path to your decklist: ")

        LOGGER.info("Retrieving card information...")
        fetched_cards = parse_card_list(Path(__file__).parent.parent.parent.joinpath(deck_identifier))

        indesign_handler = InDesignHandler()

        LOGGER.info("Processing cards...")
        for card_entry in fetched_cards:
            process_card(card_entry["card"], options=card_entry.get("options"), indesign_handler=indesign_handler)
        LOGGER.info("Successfully processed cards")

        LOGGER.info("Processing print...")
        if not args.disable_print:
            process_print(fetched_cards)
            LOGGER.info("Successfully processed print")

        return
    elif args.mode == "internal":
        LOGGER.info("Generating ID list...")
        generate_ids()
        LOGGER.info("Generated ID list", mode=InfoMode.SUCCESS, end_line=True)
    else:
        LOGGER.info("Unknown mode", mode=InfoMode.ERROR, end_line=True)


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command", required=True)

    # Generate
    parser_generate = subparser.add_parser("generate")
    parser_generate.add_argument("--deck", "-d",
                                 type=str,
                                 help="Specify a decklist for which proxies will be created. If not provided user will be prompted for decklist at runtime.")
    parser_generate.add_argument("--disable-print", help="Disables generation of print templates")

    # Internal
    parser_internal = subparser.add_parser("internal")
    parser_internal.add_argument("--generate-ids")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
