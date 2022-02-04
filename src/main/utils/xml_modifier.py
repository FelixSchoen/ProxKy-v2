from xml.etree import ElementTree

from src.main.configuration.variables import Paths


def set_text_field(frame_id: str, data: [([dict], dict)]) -> None:
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/Stories/Story_" + frame_id + ".xml")
    story_element = tree.find(".//Story[1]")
    original_paragraph_element = story_element.find(".ParagraphStyleRange[1]")
    story_element.remove(original_paragraph_element)

    for paragraph in data:
        paragraph_element = ElementTree.Element("ParagraphStyleRange")
        story_element.append(paragraph_element)

        paragraph_dict = paragraph[1] if paragraph[1] is not None else dict()

        if "applied_style" in paragraph_dict:
            pass
        else:
            paragraph_element.set("AppliedParagraphStyle", "ParagraphStyle/$ID/NormalParagraphStyle")

        for character_dict in paragraph[0]:
            character_element = ElementTree.Element("CharacterStyleRange")
            paragraph_element.append(character_element)

            if "applied_style" in character_dict:
                pass
            else:
                character_element.set("AppliedCharacterStyle", "CharacterStyle/$ID/[No character style]")

            if "font" in character_dict:
                properties_element = ElementTree.Element("Properties")
                character_element.append(properties_element)
                applied_font_element = ElementTree.Element("AppliedFont")
                properties_element.append(applied_font_element)

                applied_font_element.set("type", "string")
                applied_font_element.text = character_dict.get("font")
            if "style" in character_dict:
                character_element.set("FontStyle", character_dict.get("style"))
            if "size" in character_dict:
                character_element.set("PointSize", character_dict.get("size"))
            if "content" in character_dict:
                content = character_dict.get("content")
                content.replace("\n", " ")
                content_element = ElementTree.Element("Content")
                character_element.append(content_element)
                content_element.text = content

    tree.write(Paths.WORKING_MEMORY_CARD + "/Stories/Story_" + frame_id + ".xml")
