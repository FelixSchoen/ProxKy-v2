import getopt
import sys
from time import sleep

from configuration.variables import SUPPORTED_MODES
from info.info import show_info, Info_Mode
from src.main.utils.id_generator import generate_ids


def main(argv):
    mode = ""
    deck = ""

    try:
        opts, args = getopt.getopt(argv, "m:d:", ["mode=", "deck="])
    except getopt.GetoptError:
        show_info("Invalid command line options", mode=Info_Mode.ERROR)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            mode = arg

            if mode not in SUPPORTED_MODES:
                show_info("Mode not supported", mode=Info_Mode.ERROR)
                return
        elif opt in ("-d", "--deck"):
            deck = arg
        else:
            show_info("Unknown command line option", mode=Info_Mode.ERROR)
            return

    if mode == "standard":
        if deck == "":
            show_info("Must provide decklist", mode=Info_Mode.ERROR)
            return
        print("Hi")
        # cards = process_decklist("data/decks/" + deck + ".txt")
        # process_cards(cards)
        # process_print(cards)

        # shutil.rmtree("data/memory")
    elif mode == "generate_id":
        show_info("Generating ID list...", end_line=False)
        generate_ids()
        show_info("Generated ID list", mode=Info_Mode.SUCCESS)


if __name__ == '__main__':
    main(sys.argv[1:])
