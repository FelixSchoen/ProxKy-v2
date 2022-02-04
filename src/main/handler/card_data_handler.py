import math
import re

from src.main.configuration.config import CONFIG_PRINT_REMINDER_TEXT, CONFIG_PRINT_FLAVOR_TEXT
from src.main.configuration.variables import Ids, Fonts, MANA_MAPPING, Regex, COLOR_MAPPING
from src.main.data.card import Card
from src.main.info.info import show_info
from src.main.handler.xml_handler import set_text_field, set_gradient
from src.main.utils.misc import split_string_along_regex, split_string_reminder, mm_to_pt
from src.main.utils.mtg import sort_mana_array


def set_card_name(card: Card, id_set: dict) -> None:
    """
    Sets the name and title of a card.
    :param card: Card to set the name for
    :param id_set: Which ID set to use
    """
    show_info("Processing card name...", prefix=card.name)
    content_dict = {"content": card.name}
    content_dict.update(Fonts.TITLE)
    set_text_field(id_set[Ids.TITLE_T], [([content_dict], None)])


def set_type_line(card: Card, id_set: dict) -> None:
    """
    Sets the type line of a card.
    :param card: Card to set the type line for
    :param id_set: Which ID set to use
    """
    show_info("Processing type line...", prefix=card.name)
    content_dict = {"content": card.type_line.replace("—", "•")}
    content_dict.update(Fonts.TYPE_LINE)
    set_text_field(id_set[Ids.TYPE_LINE_T], [([content_dict], None)])


def set_mana_cost(card: Card, id_set: dict) -> None:
    """
    Sets the mana cost of a card.
    :param card: Card to set the mana cost for
    :param id_set: Which ID set to use
    """
    show_info("Processing mana cost...", prefix=card.name)

    content_dict = dict()
    content_dict.update(Fonts.MANA_COST)

    mana = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))
    content = "".join([MANA_MAPPING["{" + m + "}"] for m in mana])
    content_dict["content"] = content
    if len(content) > 5:
        cutoff_point = math.floor(len(content) / 2)
        content_dict["content"] = content[:cutoff_point] + "\n" + content[cutoff_point:]
        content_dict["size"] = "8"

    set_text_field(id_set[Ids.MANA_COST_T], [([content_dict], {"justification": "RightAlign"})])


def set_color_indicator(card: Card, id_set: dict) -> None:
    """
    Sets the color indicators of a card.
    :param card: Card to set the color indicators for
    :param id_set: Which ID set to use
    """
    # Defines the amount of blur between borders of two colors
    distance = 0
    colors_to_apply = []

    if card.color_indicator is not None and len(card.color_indicator) > 0:
        colors_to_apply = card.color_indicator
    elif card.colors is not None and len(card.colors) > 0:
        colors_to_apply = card.colors
    elif "Land" in card.type_line:
        colors_to_apply = card.produced_mana
        colors_to_apply.remove("C")

    if len(colors_to_apply) == 0:
        colors_to_apply.append("C")
    if len(colors_to_apply) == 1:
        colors_to_apply.append(colors_to_apply[0])

    sort_mana_array(colors_to_apply)
    internal_color_name_array = [COLOR_MAPPING[color] for color in colors_to_apply]

    for gradient_id in id_set[Ids.GRADIENTS_O]:
        set_gradient(gradient_id, internal_color_name_array, distance)


def set_oracle_text(card: Card, id_set: dict) -> None:
    show_info("Processing oracle text...", prefix=card.name)

    _oracle_text_handler(id_set[Ids.ORACLE_T], card.oracle_text, flavor=card.flavor_text)


def set_value(card: Card, id_set: dict) -> None:
    """
    Sets the value of a card, i.e., eiher the power / toughness, or for planeswalkers the loyalty.
    :param card: Card to set the value for
    :param id_set: Which ID set to use
    """
    show_info("Processing value...", prefix=card.name)

    content_dict = dict()
    content_dict.update(Fonts.VALUE)

    if card.power is not None and card.toughness is not None:
        content = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            content = content.replace(" ", "")
        content_dict["content"] = content
    if card.loyalty is not None:
        content_dict["content"] = card.loyalty

    set_text_field(id_set[Ids.VALUE_T], [([content_dict], {"justification": "CenterAlign"})])


def set_artist(card: Card, id_set: dict) -> None:
    """
    Sets the artist of a card
    :param card: Card to set the artist for
    :param id_set: Which ID set to use
    """
    show_info("Processing artist...", prefix=card.name)
    content_dict = {"content": card.artist}
    content_dict.update(Fonts.META)
    set_text_field(id_set[Ids.ARTIST_INFORMATION_T], [([content_dict], None)])


def set_collector_information(card: Card, id_set: dict) -> None:
    """
    Sets the collector information of a card
    :param card: Card to set the collector information for
    :param id_set: Which ID set to use
    """
    show_info("Processing collector information...", prefix=card.name)

    content = card.collector_number.zfill(3) + " • " + card.set.upper() + " • " + card.rarity.upper()[0]
    if card.side is not None:
        content = card.side.value.upper() + " • " + content

    content_dict = {"content": content}
    content_dict.update(Fonts.META)
    set_text_field(id_set[Ids.COLLECTOR_INFORMATION_T], [([content_dict], {"justification": "RightAlign"})])


def _oracle_text_handler(frame_id: str, main: str, flavor: str = None,
                         regex_template: str = Regex.TEMPLATE_ORACLE) -> None:
    """
    Handles formatting of an oracle text box. Handles reminder and flavor text, and mana formatting.
    :param frame_id: Text frame of the oracle
    :param main: Main (rule) text
    :param flavor: Optional flavor text
    :param regex_template: Which parser to use
    """
    main_split = split_string_along_regex(main, regex_template)
    flavor_split = []

    # Split main text and reminder text
    if CONFIG_PRINT_REMINDER_TEXT:
        main_split = split_string_reminder(main_split)
    else:
        main_split = filter(lambda el: el[1] != "reminder", main_split)

    # Clean and split flavor text
    if CONFIG_PRINT_FLAVOR_TEXT and flavor is not None:
        flavor_cleaned = flavor.replace("\n", " ")
        flavor_split_preliminary = split_string_along_regex(flavor_cleaned, Regex.TEMPLATE_FLAVOR,
                                                            standard_identifier="flavor")
        for entry in flavor_split_preliminary:
            flavor_split.append((entry[0].replace("*", ""), entry[1]))

    # Remove initial and trailing newlines for main and flavor arrays
    for split in [main_split, flavor_split]:
        if len(split) > 0 and split[0][0].startswith("\n"):
            split[0] = (split[0][0][None or 1:], split[0][1])
        if len(split) > 0 and split[-1][0].endswith("\n"):
            split[-1] = (split[-1][0][:-2 or None], split[-1][1])
        split[:] = filter(lambda part: len(part[0]) > 0, split)

    # Add newline between main and flavor text
    if CONFIG_PRINT_FLAVOR_TEXT:
        if len(main_split) > 0 and len(flavor_split) > 0:
            # Note: Necessary to add to main_split not flavor_split, otherwise new paragraph is opened!
            main_split.append(("\n", "flavor"))

    content_main = []
    content_flavor = []

    # Create content dictionaries from entries
    for split, content in [(main_split, content_main), (flavor_split, content_flavor)]:
        for element in split:
            content_dict = {"content": element[0]}
            if element[1] == "normal":
                content_dict.update(Fonts.ORACLE_REGULAR)
            elif element[1] == "mana":
                mana_match = re.search(Regex.MANA, element[0])
                mana_array = MANA_MAPPING[mana_match.group("match")]

                content_dict["content"] = "".join(mana_array)
                content_dict.update(Fonts.ORACLE_MANA)
            elif element[1] == "reminder":
                content_dict.update(Fonts.ORACLE_REMINDER)
            elif element[1] == "flavor":
                content_dict.update(Fonts.ORACLE_FLAVOR)
            content.append(content_dict)

    set_text_field(frame_id, [(content_main, {"spacing": str(mm_to_pt(0.75))}),
                              (content_flavor, {"space_before": str(mm_to_pt(1.5))})])
