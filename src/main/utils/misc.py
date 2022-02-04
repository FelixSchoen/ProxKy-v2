import math
import re

from src.main.configuration.variables import Regex


def mm_to_pt(mm: float) -> float:
    return (1 / (1 / 72 * 25.4)) * mm


def split_string_along_regex(string, matchers: ([str], str), standard_identifier="normal"):
    """
    Splits a string according to some rules given by the matcher element. Matchers element consists of regex to match,
    and moniker to assign. If the initial string matches one of the regex elements, it will be assigned the fitting moniker.
    :param string: String to split up
    :param matchers: Regex matcher, defines how the string will be split up
    :param standard_identifier: Which identifier to assign for parts of the next where no regex matches
    :return: The split-up string
    """
    # Build list of all available regex
    all_regex = []
    for pair in matchers:
        for regex in pair[0]:
            all_regex.append(regex)
    all_regex = list(dict.fromkeys(all_regex))

    working_string = string
    result = []

    while len(working_string) > 0:
        current_span = [math.inf, 0]
        current_regex = ""

        # Check which regex matches first, disregard regex that matches after already found ones
        for regex in all_regex:
            pattern = re.compile(regex)
            matches = list(pattern.finditer(working_string))
            if len(matches) > 0 and matches[0].span()[0] < current_span[0]:
                current_span = matches[0].span()
                current_regex = regex
                if current_span[0] == 0:
                    break

        # If no regex matched we are dealing with a normal string
        if current_span[0] == math.inf:
            result.append((working_string, standard_identifier))
            working_string = ""
        else:
            # Split into two parts
            part_one = working_string[:current_span[0]]
            part_two = working_string[current_span[0]:]

            # Everything before match is normal, remove it first
            rectifier = 0
            if current_span[0] > 0:
                result.append((part_one, standard_identifier))
                rectifier = len(part_one)

            part_one = part_two[:current_span[1] - rectifier]
            part_two = part_two[current_span[1] - rectifier:]

            # Search which regex matched and add to result
            for pair in matchers:
                if current_regex in pair[0]:
                    result.append((part_one, pair[1]))
                    working_string = part_two
                    break

    return result


def split_string_reminder(reminder_array):
    text_array = []

    for element in reminder_array:
        if element[1] != "reminder":
            text_array.append(element)
        else:
            reminder_split = split_string_along_regex(element[0], Regex.TEMPLATE_MANA,
                                                      standard_identifier="reminder")
            text_array.extend(reminder_split)

    return text_array
