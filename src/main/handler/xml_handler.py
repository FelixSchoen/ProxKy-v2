from xml.etree import ElementTree

from src.main.configuration.variables import Paths, Regex
from src.main.utils.misc import split_string_along_regex


def set_text_field(frame_id: str, data: [([dict], dict)]) -> None:
    """
    Sets the entire content of a text field, overriding any and all previous values.
    :param frame_id: Frame of the field to set
    :param data: Data to write, in the following format: A list of paragraphs, with a dictionary specifying the
    paragraph options. Each paragraph has a list of dictionaries containing information about the text to set,
    and its properties.
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Stories/Story_" + frame_id + ".xml")
    story_element = tree.find(".//Story[1]")
    original_paragraph_element = story_element.find(".ParagraphStyleRange[1]")
    story_element.remove(original_paragraph_element)

    for paragraph in data:
        paragraph_element = ElementTree.Element("ParagraphStyleRange")
        story_element.append(paragraph_element)
        paragraph_properties_element = ElementTree.Element("Properties")
        paragraph_element.append(paragraph_properties_element)

        paragraph_dict = paragraph[1] if paragraph[1] is not None else dict()

        if "applied_style" in paragraph_dict:
            pass
        else:
            paragraph_element.set("AppliedParagraphStyle", "ParagraphStyle/$ID/NormalParagraphStyle")
        if "justification" in paragraph_dict:
            paragraph_element.set("Justification", paragraph_dict["justification"])
        if "space_before" in paragraph_dict:
            paragraph_element.set("SpaceBefore", paragraph_dict["space_before"])
        if "spacing" in paragraph_dict:
            spacing_element = ElementTree.Element("SameParaStyleSpacing")
            paragraph_properties_element.append(spacing_element)

            spacing_element.set("type", "unit")
            spacing_element.text = paragraph_dict["spacing"]

        if len(list(paragraph_properties_element)) == 0:
            paragraph_element.remove(paragraph_properties_element)

        for character_dict in paragraph[0]:
            character_element = ElementTree.Element("CharacterStyleRange")
            paragraph_element.append(character_element)
            character_properties_element = ElementTree.Element("Properties")
            character_element.append(character_properties_element)

            if "applied_style" in character_dict:
                pass
            else:
                character_element.set("AppliedCharacterStyle", "CharacterStyle/$ID/[No character style]")

            if "leading" in character_dict:
                leading_element = ElementTree.Element("Leading")
                character_properties_element.append(leading_element)

                leading_element.set("type", "unit")
                leading_element.text = character_dict.get("leading")
            if "font" in character_dict:
                applied_font_element = ElementTree.Element("AppliedFont")
                character_properties_element.append(applied_font_element)

                applied_font_element.set("type", "string")
                applied_font_element.text = character_dict.get("font")
            if "style" in character_dict and character_dict.get("style").lower() != "regular":
                character_element.set("FontStyle", character_dict.get("style"))
            if "size" in character_dict:
                character_element.set("PointSize", character_dict.get("size"))
            if "content" in character_dict:
                content = character_dict.get("content")
                content_split = split_string_along_regex(content, Regex.TEMPLATE_BREAK)

                for split in content_split:
                    if split[1] == "normal":
                        content_element = ElementTree.Element("Content")
                        character_element.append(content_element)
                        content_element.text = split[0]
                    else:
                        content_element = ElementTree.Element("Br")
                        character_element.append(content_element)

    tree.write(Paths.WORKING_MEMORY_CARD + "/Stories/Story_" + frame_id + ".xml")


def set_gradient(gradient_id: str, colors: [str], distance: float = 0) -> None:
    """
    Applies a gradient of the given color names to the element, equally spaced.
    :param gradient_id: ID of the gradient
    :param colors: Internal color names to apply
    :param distance: Fade distance between two colors
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Resources/Graphic.xml")
    gradient = tree.find(".//Gradient[@Self='Gradient/" + gradient_id + "']")

    # Remove previous stops
    for gradient_stop in gradient.findall(".//GradientStop"):
        gradient.remove(gradient_stop)

    # Add new colors
    for i, color in enumerate(colors):
        # Calculate positions of stops
        position = i * 100 / (len(colors))
        position_next = (i + 1) * 100 / (len(colors))

        # Left boundary
        position_adjusted = position
        if i > 0:
            position_adjusted += distance
        gradient_stop = ElementTree.Element("GradientStop")
        gradient_stop.set("StopColor", "Color/" + color)
        gradient_stop.set("Location", str(position_adjusted))
        gradient.append(gradient_stop)

        # Right boundary
        position_adjusted = position_next
        if i < len(colors) - 1:
            position_adjusted -= distance
        gradient_stop = ElementTree.Element("GradientStop")
        gradient_stop.set("StopColor", "Color/" + color)
        gradient_stop.set("Location", str(position_adjusted))
        gradient.append(gradient_stop)

    tree.write(Paths.WORKING_MEMORY_CARD + "/Resources/Graphic.xml")
