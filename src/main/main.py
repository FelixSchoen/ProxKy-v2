import getopt
import sys

from configuration.variables import SUPPORTED_MODES
from info.info import show_info, INFO_MODE


def main(argv):
    mode = ""
    deck = ""

    try:
        opts, args = getopt.getopt(argv, "m:d:", ["mode=", "deck="])
    except getopt.GetoptError:
        show_info("Invalid command line options", mode=INFO_MODE.error)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            mode = arg

            if mode not in SUPPORTED_MODES:
                show_info("Mode not supported", mode=INFO_MODE.error)
                return
        elif opt in ("-d", "--deck"):
            deck = arg
        else:
            show_info("Unknown command line option", mode=INFO_MODE.error)
            return

    if mode == "standard":
        print("Hi")
        # cards = process_decklist("data/decks/" + deck + ".txt")
        # process_cards(cards)
        # process_print(cards)

        # shutil.rmtree("data/memory")
    elif mode == "generate_id":
        print()
        # generate_all_ids()


if __name__ == '__main__':
    main(sys.argv[1:])
