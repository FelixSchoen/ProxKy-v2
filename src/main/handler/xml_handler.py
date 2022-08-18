from xml.etree import ElementTree

from PIL import Image  # Pillow

from src.main.configuration.variables import Paths, Regex, IMAGE_TYPES
from src.main.misc.util import split_string_along_regex, mm_to_pt


def set_text_field(frame_id: str, data: [([dict], dict)], root_path: str = None) -> None:
    """
    Sets the entire content of a text field, overriding any and all previous values.
    :param frame_id: Frame of the field to set
    :param data: Data to write, in the following format: A list of paragraphs, with a dictionary specifying the
    paragraph options. Each paragraph has a list of dictionaries containing information about the text to set,
    and its properties.
    :param root_path: Path to the working memory folder
    """
    if root_path is None:
        root_path = Paths.WORKING_MEMORY_CARD

    tree = ElementTree.parse(root_path + "/Stories/Story_" + frame_id + ".xml")
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
        if "hyphenation" in paragraph_dict:
            pass
        else:
            paragraph_element.set("Hyphenation", "false")
        if "justification" in paragraph_dict:
            paragraph_element.set("Justification", paragraph_dict["justification"])
        if "tablist" in paragraph_dict:
            tablist = ElementTree.Element("TabList")
            paragraph_properties_element.append(tablist)
            tablist.set("type", "list")
            for tab in paragraph_dict["tablist"]:
                list_item = ElementTree.Element("ListItem")
                tablist.append(list_item)
                list_item.set("type", "record")

                alignment = ElementTree.Element("Alignment")
                list_item.append(alignment)
                alignment.set("type", "enumeration")
                alignment.text = tab[0]

                alignment_character = ElementTree.Element("AlignmentCharacter")
                list_item.append(alignment_character)
                alignment_character.set("type", "string")
                alignment_character.text = "."

                leader = ElementTree.Element("Leader")
                list_item.append(leader)
                leader.set("type", "string")

                position = ElementTree.Element("Position")
                list_item.append(position)
                position.set("type", "unit")
                position.text = tab[1]
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

    tree.write(root_path + "/Stories/Story_" + frame_id + ".xml")


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


def set_graphic(frame_id: str, spread_id: str, path: str, filename: str, type_file: str = "svg",
                mode_scale: str = "fit", mode_align: str = "center") -> None:
    """
    Fills the given frame with the provided graphic
    :param frame_id: Image frame of the graphic
    :param spread_id: Spread where the image frame occurs
    :param path: Path to the file
    :param filename: Name of the file
    :param type_file: Extension of the file
    :param mode_scale: Whether to fit (align with larger side) or stretch (align with smaller side) the image
    :param mode_align: Where to align the image vertically if it is oversized
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")
    frame = tree.find(".//Rectangle[@Self='" + frame_id + "']")
    coordinates = _get_coordinates(frame)

    # Size of the container
    size_box_x = abs(coordinates[1][0] - coordinates[0][0])
    size_box_y = abs(coordinates[2][1] - coordinates[1][1])

    # Bounding box defined in the file
    if type_file == "svg":
        graphic = ElementTree.Element("SVG")
        bounding_box = _get_bounding_box(path, filename)
    elif type_file in IMAGE_TYPES:
        graphic = ElementTree.Element("Image")
        with Image.open(path + "/" + filename + "." + type_file) as img:
            bounding_box = img.size
    else:
        raise NotImplementedError

    # Factor to scale the graphic by to fit in the container
    factor_x = size_box_x / bounding_box[0]
    factor_y = size_box_y / bounding_box[1]

    factor = None
    if mode_scale == "stretch":
        if min(factor_x, factor_y) * size_box_x >= bounding_box[0] \
                and min(factor_x, factor_y) * size_box_y >= bounding_box[1]:
            factor = min(factor_x, factor_y)
        else:
            factor = max(factor_x, factor_y)
    if mode_scale == "fit":
        if min(factor_x, factor_y) * size_box_x <= bounding_box[0] \
                and min(factor_x, factor_y) * size_box_y <= bounding_box[1]:
            factor = min(factor_x, factor_y)
        else:
            factor = max(factor_x, factor_y)
    elif mode_scale == "fit_x":
        if factor_x * bounding_box[1] >= size_box_y:
            factor = factor_x
        else:
            factor = factor_y
    elif mode_scale == "fit_y":
        if factor_y * bounding_box[0] >= size_box_x:
            factor = factor_y
        else:
            factor = factor_x

    # Final size of the scaled graphic
    size_insert_x = bounding_box[0] * factor
    size_insert_y = bounding_box[1] * factor

    # Distance to move graphic by to fit into center of container
    graphic_position_x = (size_box_x - size_insert_x) / 2 + coordinates[0][0]
    graphic_position_y = coordinates[0][1]
    if mode_align == "center":
        graphic_position_y = coordinates[0][1] + (size_box_y - size_insert_y) / 2

    graphic.set("ItemTransform",
                str(factor) + " 0 0 " + str(factor) + " " + str(graphic_position_x) + " " + str(graphic_position_y))
    properties = ElementTree.Element("Properties")
    graphic.append(properties)

    # Important to keep all 4 elements, otherwise sizing does not get applied
    graphic_bounds = ElementTree.Element("GraphicBounds")
    properties.append(graphic_bounds)
    graphic_bounds.set("Left", str(0))
    graphic_bounds.set("Top", str(0))
    graphic_bounds.set("Right", str(bounding_box[0]))
    graphic_bounds.set("Bottom", str(bounding_box[1]))

    link = ElementTree.Element("Link")
    graphic.append(link)
    link.set("LinkResourceURI", "file:" + path + "/" + filename + "." + type_file)

    frame.append(graphic)
    tree.write(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")


def set_pdf(frame_id: str, spread_id: str, path: str, filename: str, root_path: str = None, page: int = 1) -> None:
    """
    Adds a link to a PDF file to the given frame.
    :param frame_id: The frame where the PDF should be embedded
    :param spread_id: The spread where the frame occurs
    :param path: Path to the PDF
    :param filename: Filename of the PDF
    :param root_path: Path to the working memory folder
    :param page: Which page of the PDF to use
    """
    if root_path is None:
        root_path = Paths.WORKING_MEMORY_PRINT

    tree = ElementTree.parse(root_path + "/Spreads/Spread_" + spread_id + ".xml")
    rectangle = tree.find(".//Rectangle[@Self='" + frame_id + "']")

    pdf = ElementTree.Element("PDF")
    pdf.set("ItemTransform", f"1 0 0 1 -{mm_to_pt(27.5)} -{mm_to_pt(229.9)}")
    pdf_attribute = ElementTree.Element("PDFAttribute")
    pdf_attribute.set("PageNumber", str(page))
    link = ElementTree.Element("Link")
    link.set("LinkResourceURI", "file:" + path + "/" + filename + ".pdf")

    rectangle.append(pdf)
    pdf.append(pdf_attribute)
    pdf.append(link)

    tree.write(root_path + "/Spreads/Spread_" + spread_id + ".xml")


def set_indd(frame_id: str, spread_id: str, path: str, filename: str, root_path: str = None, page: int = 1) -> None:
    """
    Adds a link to an indd file to the given frame.
    :param frame_id: The frame where the indd should be embedded
    :param spread_id: The spread where the frame occurs
    :param path: Path to the indd
    :param filename: Filename of the indd
    :param root_path: Path to the working memory folder
    :param page: Which page of the indd use
    """
    if root_path is None:
        root_path = Paths.WORKING_MEMORY_PRINT

    tree = ElementTree.parse(root_path + "/Spreads/Spread_" + spread_id + ".xml")
    rectangle = tree.find(".//Rectangle[@Self='" + frame_id + "']")

    imported_page = ElementTree.Element("ImportedPage")
    imported_page.set("PageNumber", str(page))
    imported_page.set("ImportedPageCrop", "CropBleed")
    imported_page.set("ItemTransform", f"1 0 0 1 -{mm_to_pt(27.5)} -{mm_to_pt(229.9)}")
    link = ElementTree.Element("Link")
    link.set("LinkResourceURI", "file:" + path + "/" + filename + ".indd")

    rectangle.append(imported_page)
    imported_page.append(link)

    tree.write(root_path + "/Spreads/Spread_" + spread_id + ".xml")


def set_visibility(object_id: str, spread_id: str, visible) -> None:
    """
    Change the visibility of the given object
    :param object_id: ID of the object
    :param spread_id: Spread where the object occurs
    :param visible: Whether the object should be visible or not
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")
    xml_object = tree.find(".//*[@Self='" + object_id + "']")
    xml_object.set("Visible", "true" if visible else "false")
    tree.write(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")


def set_coordinates(object_id: str, spread_id: str,
                    coordinates: [(float, float), (float, float), (float, float), (float, float)]) -> None:
    """
    Adjusts the coordinates of the given object.
    :param object_id: Object to change the coordinates for
    :param spread_id: Spread where to object occurs
    :param coordinates: The new coordinates of the object
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")
    xml_object = tree.find(".//*[@Self='" + object_id + "']")

    top_left = xml_object.find(".//PathPointType[1]")
    top_right = xml_object.find(".//PathPointType[4]")
    bottom_left = xml_object.find(".//PathPointType[2]")
    bottom_right = xml_object.find(".//PathPointType[3]")

    for i, point in enumerate([top_left, top_right, bottom_left, bottom_right]):
        point.attrib.pop("Anchor")
        point.attrib.pop("LeftDirection")
        point.attrib.pop("RightDirection")

        coordinate = str(coordinates[i][0]) + " " + str(coordinates[i][1])

        point.set("Anchor", coordinate)
        point.set("LeftDirection", coordinate)
        point.set("RightDirection", coordinate)

    tree.write(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")


def set_transparency(object_id: str, spread_id: str, opacity: float, mode: str = "Fill") -> None:
    """
    Adjusts the transparency of the given object.
    :param object_id: Object to change the transparency for
    :param spread_id: Spread where the object occurs
    :param opacity: The transparency to set
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")
    xml_object = tree.find(".//*[@Self='" + object_id + "']")

    transparency = ElementTree.Element(mode + "TransparencySetting")
    blending = ElementTree.Element("BlendingSetting")
    blending.set("Opacity", str(opacity))
    transparency.append(blending)
    xml_object.append(transparency)

    tree.write(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")


def move(object_id: str, spread_id: str,
         move_by: (int, int)) -> None:
    """
    Moves an object by modifying its "ItemTransform" record.
    :param object_id: Object to move
    :param spread_id: Spread where the object occurs
    :param move_by: Adjustments in x and y direction
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")
    xml_object = tree.find(".//*[@Self='" + object_id + "']")

    coordinates = xml_object.attrib["ItemTransform"].split(" ")
    xml_object.set("ItemTransform",
                   coordinates[0] + " " + coordinates[1] + " " + coordinates[2] + " " + coordinates[3] + " " +
                   str(float(coordinates[4]) + move_by[0]) + " " + str(float(coordinates[5]) + move_by[1]))

    tree.write(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")


def get_coordinates(object_id: str, spread_id: str) -> ((int, int), (int, int), (int, int), (int, int)):
    """
    Obtains the coordinates of an object.
    :param object_id: Object to obtain the coordinates for
    :param spread_id: Spread where the object occurs
    :return: Coordinates of the corner points of the object, in the order top left, top right, bottom left, bottom right
    """
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + spread_id + ".xml")
    xml_object = tree.find(".//*[@Self='" + object_id + "']")
    return _get_coordinates(xml_object)


def _get_coordinates(element):
    point_top_left = element.find(".//PathPointType[1]")
    point_bottom_left = element.find(".//PathPointType[2]")
    point_top_right = element.find(".//PathPointType[4]")
    point_bottom_right = element.find(".//PathPointType[3]")

    values = point_top_left.attrib["Anchor"].split(" ")
    coordinates_top_left = float(values[0]), float(values[1])

    values = point_bottom_left.attrib["Anchor"].split(" ")
    coordinates_bottom_left = float(values[0]), float(values[1])

    values = point_top_right.attrib["Anchor"].split(" ")
    coordinates_top_right = float(values[0]), float(values[1])

    values = point_bottom_right.attrib["Anchor"].split(" ")
    coordinates_bottom_right = float(values[0]), float(values[1])

    return coordinates_top_left, coordinates_top_right, coordinates_bottom_left, coordinates_bottom_right


def _get_bounding_box(path, filename):
    tree = ElementTree.parse(path + "/" + filename + ".svg")
    values = tree.getroot().attrib["viewBox"].split(" ")
    return float(values[2]), float(values[3])
