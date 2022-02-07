from src.main.configuration.variables import Magic


def get_clean_name(card_name: str) -> str:
    """
    Returns a cleaned-up version of the card name, not containing illegal characters.
    :param card_name: The card name to clean up
    :return: The clean name
    """
    return card_name.replace("//", "--")


def get_color_array(colors: [str]) -> [str]:
    """
    Converts an array of different values to an array containing MTG colors of the input, where each color occurs at
    most once. The array is sorted according to the MTG color chart.
    :param colors: Array containing different mana amounts
    :return: Array containing sorted mana types of input array
    """
    final_array = []
    for entry in colors:
        if entry in Magic.MANA_TYPES and entry not in final_array:
            final_array.append(entry)
    sort_mana_array(final_array)
    return final_array


def get_card_types(card) -> [str]:
    """
    Returns the types of the card in an array
    :param card: The card to obtain the types for
    :return: The types of the card
    """
    types = card.type_line.split("—")
    types = list(filter(None, types[0].split(" ")))
    return types


def sort_mana_array(mana_array: [str]) -> [str]:
    """
    :param mana_array: Unsorted mana array
    :return: Mana array sorted according to MTG color chart
    """
    mana_array.sort(key=lambda x: Magic.MANA_TYPES.index(x))
