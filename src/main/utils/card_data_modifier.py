from src.main.configuration.variables import Ids, Fonts
from src.main.info.info import show_info
from src.main.utils.xml_modifier import set_text_field


def set_card_name(card, id_set):
    show_info("Processing card name...", prefix=card.name)
    content_dict = {"content": card.name}
    content_dict.update(Fonts.TITLE)
    set_text_field(id_set[Ids.TITLE_T], [([content_dict], None)])
