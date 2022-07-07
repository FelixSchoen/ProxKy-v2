import math
import os
import re

import requests

from src.main.configuration.config import CONFIG_PRINT_REMINDER_TEXT, CONFIG_PRINT_FLAVOR_TEXT
from src.main.configuration.variables import Ids, Fonts, MANA_MAPPING, Regex, COLOR_MAPPING, Paths, IMAGE_TYPES, \
    Distances, CONVENTIONAL_DOUBLE_SIDED_LAYOUTS, BACKGROUND_COLOR_MAPPING, Id_Sets
from src.main.data.card import Card
from src.main.handler.indesign_handler import InDesignHandler
from src.main.handler.xml_handler import set_text_field, set_gradient, set_graphic, set_visibility, get_coordinates, \
    set_coordinates, set_transparency
from src.main.utils.info import show_info, Info_Mode
from src.main.utils.misc import split_string_along_regex, split_string_reminder, mm_to_pt, check_exists
from src.main.utils.mtg import sort_mana_array, get_card_types


def set_artwork(card: Card, id_set: dict, layout=None) -> None:
    """
    Sets the artwork of a card.
    :param card: Card to set the artwork for
    :param id_set: Which ID set to use
    :param layout: The layout of the parent card
    """
    show_info("Processing artwork...", prefix=card.name)

    identifier = str(card.collector_number)

    if layout in ["reversible_card"]:
        identifier += "a" if id_set == Id_Sets.ID_SET_FRONT else "b"

    filename = identifier + " - " + card.name
    path = Paths.ARTWORK + "/" + card.set.upper()
    image_type = "na"

    for possible_image_type in IMAGE_TYPES:
        if check_exists(path + "/" + filename + "." + possible_image_type):
            image_type = possible_image_type
            break

    if image_type == "na":
        if "art_crop" not in card.image_uris:
            show_info("No artwork on Scryfall", prefix=card.name, mode=Info_Mode.ERROR, end_line=True)
            return

        response = requests.get(card.image_uris["art_crop"])

        if response.status_code != 200:
            show_info("Could not download artwork", prefix=card.name, mode=Info_Mode.ERROR, end_line=True)
            return

        os.makedirs(Paths.ARTWORK_DOWNLOADED + "/" + card.set.upper(), exist_ok=True)
        with open(Paths.ARTWORK_DOWNLOADED + "/" + card.set.upper() + "/" + filename + ".jpg", "wb") as handler:
            path = Paths.ARTWORK_DOWNLOADED + "/" + card.set.upper()
            image_type = "jpg"
            handler.write(response.content)

    set_graphic(id_set[Ids.ARTWORK_O], id_set[Ids.SPREAD], path, filename, type_file=image_type, mode_scale="stretch")


def set_type_icon(card: Card, id_set: dict) -> None:
    """
    Sets the icon of a card.
    :param card: Card to set the icon for
    :param id_set: Which ID set to use
    """
    show_info("Processing card icon...", prefix=card.name)

    types = get_card_types(card)
    if "Legendary" in types:
        types.remove("Legendary")
    if "Basic" in types:
        types.remove("Basic")
    if "Token" in types:
        types.remove("Token")
    if "Snow" in types:
        types.remove("Snow")

    if len(types) != 1:
        card_type = "Multiple"
    else:
        card_type = types[0]

    set_graphic(id_set[Ids.TYPE_ICON_O], id_set[Ids.SPREAD], Paths.CARD_TYPES, card_type.lower())


def set_card_name(card: Card, id_set: dict, font_settings: dict = None) -> None:
    """
    Sets the name and title of a card.
    :param card: Card to set the name for
    :param id_set: Which ID set to use
    :param font_settings: Overrides the standard font settings
    """
    show_info("Processing card name...", prefix=card.name)

    content_dict = {"content": card.name}
    content_dict.update(Fonts.TITLE)
    if font_settings is not None:
        content_dict.update(font_settings)
    set_text_field(id_set[Ids.TITLE_T], [([content_dict], None)])

    # Check for e.g. split cards
    if Ids.NAME_T in id_set:
        content_dict = {"content": card.name}
        content_dict.update(Fonts.NAME)
        set_text_field(id_set[Ids.NAME_T], [([content_dict], {"justification": "CenterAlign"})])


def set_type_line(card: Card, id_set: dict, font_settings: dict = None) -> None:
    """
    Sets the type line of a card.
    :param card: Card to set the type line for
    :param id_set: Which ID set to use
    :param font_settings: Overrides the standard font settings
    """
    show_info("Processing type line...", prefix=card.name)
    content_dict = {"content": card.type_line.replace("—", "•")}
    content_dict.update(Fonts.TYPE_LINE)
    if font_settings is not None:
        content_dict.update(font_settings)
    set_text_field(id_set[Ids.TYPE_LINE_T], [([content_dict], None)])


def set_mana_cost(card: Card, id_set: dict, font_settings: dict = None) -> None:
    """
    Sets the mana cost of a card.
    :param card: Card to set the mana cost for
    :param id_set: Which ID set to use
    :param font_settings: Overrides the standard font settings
    """
    show_info("Processing mana cost...", prefix=card.name)

    content_dict = dict()
    content_dict.update(Fonts.MANA_COST)
    if font_settings is not None:
        content_dict.update(font_settings)

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
    show_info("Processing color indicator...", prefix=card.name)
    # Defines the amount of blur between borders of two colors
    distance = 0
    colors_to_apply = []

    if card.color_indicator is not None and len(card.color_indicator) > 0:
        colors_to_apply = card.color_indicator
    elif card.colors is not None and len(card.colors) > 0:
        colors_to_apply = card.colors
    elif "Land" in card.type_line:
        colors_to_apply = card.produced_mana
        if "C" in colors_to_apply:
            colors_to_apply.remove("C")

    if len(colors_to_apply) == 0:
        colors_to_apply.append("C")
    if len(colors_to_apply) == 1:
        colors_to_apply.append(colors_to_apply[0])

    sort_mana_array(colors_to_apply)
    internal_color_name_array = [COLOR_MAPPING[color] for color in colors_to_apply]

    for gradient_id in id_set[Ids.COLOR_INDICATOR_GRADIENTS_O]:
        set_gradient(gradient_id, internal_color_name_array, distance)


def set_background_indicator(card: Card, id_set: dict) -> None:
    """
    Sets the color of the background.
    :param card: Card to set the color of the background for
    :param id_set: Which ID set to use
    """
    show_info("Processing background color...", prefix=card.name)

    set_transparency(id_set[Ids.BACKDROP_O], id_set[Ids.SPREAD], 85)

    # Defines the amount of blur between borders of two colors
    distance = 15
    colors_to_apply = []

    if card.color_indicator is not None and len(card.color_indicator) > 0:
        colors_to_apply = card.color_indicator
    elif card.colors is not None and len(card.colors) > 0:
        colors_to_apply = card.colors
    elif "Land" in card.type_line:
        colors_to_apply = card.produced_mana

    if "C" in colors_to_apply:
        colors_to_apply.remove("C")

    if len(colors_to_apply) == 1:
        colors_to_apply.append(colors_to_apply[0])

    if len(colors_to_apply) == 2:
        sort_mana_array(colors_to_apply)
        internal_color_name_array = [BACKGROUND_COLOR_MAPPING[color] for color in colors_to_apply]

        gradient_id = id_set[Ids.BACKGROUND_COLOR_GRADIENTS_O]
        set_gradient(gradient_id, internal_color_name_array, distance)


def set_oracle_text(card: Card, id_set: dict, may_be_centered: bool = True) -> None:
    """
    Sets the oracle text of a card.
    :param card: Card to set the oracle text for
    :param id_set: Which ID set to use
    :param may_be_centered: Whether the text may be centered if it is below a certain amount of lines
    """
    show_info("Processing oracle text...", prefix=card.name)

    _oracle_text_handler(id_set[Ids.ORACLE_T], card.oracle_text, flavor=card.flavor_text,
                         force_justification="LeftAlign" if not may_be_centered else None)


def set_planeswalker_text(card: Card, id_set: dict) -> None:
    """
    Sets the planeswalker text of a card.
    :param card: Card to set the planeswalker text for
    :param id_set: Which ID set to use
    """
    show_info("Processing planeswalker text...", prefix=card.name)

    _planeswalker_text_handler(id_set, card.oracle_text, double_faced=card.layout in CONVENTIONAL_DOUBLE_SIDED_LAYOUTS)


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
        content = card.side.upper() + " • " + content

    content_dict = {"content": content}
    content_dict.update(Fonts.META)
    set_text_field(id_set[Ids.COLLECTOR_INFORMATION_T], [([content_dict], {"justification": "RightAlign"})])


def set_modal(card: Card, id_sets: [dict]) -> None:
    """
    Sets the modal of a card
    :param card: Card to set the modal for
    :param id_sets: Which ID sets to use
    """
    show_info("Processing modal...", prefix=card.name)
    for i, id_set in enumerate(id_sets):
        face = card.card_faces[(i + 1) % 2]

        if card.layout == "modal_dfc":
            type_display = "MODAL"
        elif card.layout == "transform":
            type_display = "TRANSFORM"
        elif card.layout == "meld":
            type_display = "MELD"
        elif card.layout == "double_faced_token":
            type_display = "FLIP"
        else:
            raise NotImplementedError

        line_to_insert = type_display + " — " + face.type_line.replace("—", "•")

        supertypes = face.type_line.split("—")[0].split(" ")
        supertypes = list(filter(lambda item: item.strip(), supertypes))
        if len(supertypes) == 1:
            line_to_insert = line_to_insert.replace("Creature • ", "")

        if len(face.mana_cost) > 0:
            line_to_insert += " • " + face.mana_cost
        if "Land" in face.type_line:
            match = re.search(Regex.ADD_MANA, face.oracle_text)
            if match:
                line_to_insert += " • " + match.group("match")

        line_to_insert = "{◄}\t" + line_to_insert + "\t{►}"

        line_split = split_string_along_regex(line_to_insert, Regex.TEMPLATE_MANA)
        content = []
        for element in line_split:
            content_dict = {"content": element[0]}
            if element[1] == "normal":
                content_dict.update(Fonts.MODAL)
            elif element[1] == "mana":
                mana_match = re.search(Regex.MANA, element[0])
                mana_array = MANA_MAPPING[mana_match.group("match")]

                content_dict["content"] = "".join(mana_array)
                content_dict.update(Fonts.ORACLE_MANA)
                content_dict["size"] = Fonts.MODAL["size"]
            content.append(content_dict)

        data = [(content, {"tablist": [("CenterAlign", str(mm_to_pt(26.75))),
                                       ("RightAlign", str(mm_to_pt(53.5)))]})]
        set_text_field(id_set[Ids.MODAL_T], data)


def _oracle_text_handler(frame_id: str, main: str, flavor: str = None, regex_template: str = Regex.TEMPLATE_ORACLE,
                         force_justification: str = None, force_font: dict = None) -> int:
    """
    Handles formatting of an oracle text box. Handles reminder and flavor text, and mana formatting.
    :param frame_id: Text frame of the oracle
    :param main: Main (rule) text
    :param flavor: Optional flavor text
    :param regex_template: Which parser to use
    :return Number of lines set
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
            split[-1] = (split[-1][0][:-1 or None], split[-1][1])
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
            elif element[1] == "keyword":
                content_dict.update(Fonts.ORACLE_KEYWORD)
            elif element[1] == "reminder":
                content_dict.update(Fonts.ORACLE_REMINDER)
            elif element[1] == "flavor":
                content_dict.update(Fonts.ORACLE_FLAVOR)
            if force_font is not None:
                content_dict.update(force_font)
            content.append(content_dict)

    id_handler = InDesignHandler()
    data = [(content_main, {"spacing": str(mm_to_pt(0.75))}),
            (content_flavor, {"space_before": str(mm_to_pt(1.5))})]
    lines = id_handler.get_text_lines(data)

    justification = "LeftAlign" if force_justification is None else force_justification
    if force_justification is None and lines <= 2:
        justification = "CenterAlign"

    data = [(content_main, {"justification": justification, "spacing": str(mm_to_pt(0.75))})]
    if flavor is not None and len(flavor) > 0:
        data.append((content_flavor, {"justification": justification, "space_before": str(mm_to_pt(1.5))}))

    set_text_field(frame_id, data)

    return lines


def _planeswalker_text_handler(id_set: dict, main: str, double_faced: bool = False,
                               regex_template: str = Regex.TEMPLATE_PLANESWALKER) -> None:
    planeswalker_split = split_string_along_regex(main, regex_template)
    if "\n" in planeswalker_split[-1][0]:
        # Split up last entry
        loyalty_oracle_combined = planeswalker_split.pop()
        loyalty_oracle_split = split_string_along_regex(loyalty_oracle_combined[0], Regex.TEMPLATE_BREAK)
        planeswalker_split.append(loyalty_oracle_split[0])

        # Concatenate trailing part
        trailing = ""
        for trailing_tuple in loyalty_oracle_split[2:]:
            trailing += trailing_tuple[0]
        planeswalker_split.append((trailing, "normal"))

    # Get amount of abilities
    amount_abilities = sum(x[1] == "loyalty" for x in planeswalker_split)
    if amount_abilities > 4:
        raise NotImplementedError("Too many abilities")

    # Check if we have an additional leading or trailing box
    flag_leading_text = planeswalker_split[0][1] != "loyalty"
    flag_trailing_text = planeswalker_split[-2][1] != "loyalty"
    set_visibility(id_set[Ids.ORACLE_O], id_set[Ids.SPREAD], flag_leading_text)

    # Array of lines, saves how many lines each entry has
    amount_boxes = (amount_abilities + (1 if flag_leading_text else 0) + (1 if flag_trailing_text else 0))
    lines = [0] * amount_boxes

    for i in range(0, amount_boxes):
        # Leading
        if i == 0 and flag_leading_text:
            lines[0] = _oracle_text_handler(id_set[Ids.ORACLE_T], planeswalker_split[0][0],
                                            force_justification="LeftAlign")
        # Planeswalker Oracle
        elif int(flag_leading_text) <= i < amount_boxes - int(flag_trailing_text):
            index_planeswalker = i - int(flag_leading_text)
            text_loyalty = planeswalker_split[2 * (i - flag_leading_text) + flag_leading_text][0]
            text_oracle = planeswalker_split[2 * (i - flag_leading_text) + 1 + flag_leading_text][0]
            _oracle_text_handler(id_set[Ids.PLANESWALKER_VALUE_T][index_planeswalker], text_loyalty,
                                 force_justification="RightAlign")
            lines[i] = _oracle_text_handler(id_set[Ids.PLANESWALKER_ORACLE_NUMBERED_T][index_planeswalker], text_oracle,
                                            force_justification="LeftAlign")
        # Trailing
        else:
            lines[i] = _oracle_text_handler(id_set[Ids.PLANESWALKER_ORACLE_FINAL_T], planeswalker_split[-1][0],
                                            force_justification="LeftAlign")

    height_budget = Distances.ORACLE_HEIGHT
    if double_faced:
        height_budget += Distances.MODAL_HEIGHT
    height_budget -= Distances.SPACE_PLANESWALKER * (amount_boxes - 1)

    for i in range(0, amount_boxes):
        shift_modal = double_faced * Distances.MODAL_HEIGHT
        shift_previous_boxes = (i * Distances.SPACE_PLANESWALKER) + (
                (sum(lines[:i]) / sum(lines)) * height_budget)
        shift_sum = shift_modal + shift_previous_boxes

        # Leading
        if i == 0 and flag_leading_text:
            object_ids = [id_set[Ids.ORACLE_O]]
        # Planeswalker Oracle
        elif int(flag_leading_text) <= i < amount_boxes - int(flag_trailing_text):
            index_planeswalker = i - int(flag_leading_text)
            object_ids = [id_set[Ids.PLANESWALKER_VALUE_O][index_planeswalker],
                          id_set[Ids.PLANESWALKER_ORACLE_NUMBERED_O][index_planeswalker]]
        # Trailing
        else:
            object_ids = [id_set[Ids.PLANESWALKER_ORACLE_FINAL_O]]

        for object_id in object_ids:
            coordinates = get_coordinates(object_id, id_set[Ids.SPREAD])
            set_coordinates(object_id, id_set[Ids.SPREAD], [(coordinates[0][0], coordinates[0][1] + shift_sum),
                                                            (coordinates[1][0], coordinates[1][1] + shift_sum),
                                                            (coordinates[0][0], coordinates[0][1] + shift_sum + (
                                                                    (lines[i] / sum(lines)) * height_budget)),
                                                            (coordinates[1][0], coordinates[1][1] + shift_sum + (
                                                                    (lines[i] / sum(lines)) * height_budget))])
            set_visibility(object_id, id_set[Ids.SPREAD], True)
