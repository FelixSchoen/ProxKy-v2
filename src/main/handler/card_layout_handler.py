import os

from src.main.configuration.variables import Ids, Paths, Distances
from src.main.handler.xml_handler import set_visibility, get_coordinates, set_coordinates


def layout_single_faced(id_set: dict):
    os.remove(Paths.WORKING_MEMORY_CARD + "/Spreads/Spread_" + id_set[Ids.SPREAD] + ".xml")

    # TODO XML Outside of XML handler
    from xml.etree import ElementTree
    tree = ElementTree.parse(Paths.WORKING_MEMORY_CARD + "/designmap.xml")
    element = tree.getroot().find(".//*[@src='Spreads/Spread_" + id_set[Ids.SPREAD] + ".xml']")
    tree.getroot().remove(element)

    with open(Paths.WORKING_MEMORY_CARD + "/designmap.xml", "wb") as file:
        file.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        file.write(b'<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="16.4(55)" ?>')
        tree.write(file, xml_declaration=False, encoding="utf-8")


def layout_double_faced(id_sets: [dict]):
    for id_set in id_sets:
        set_visibility(id_set[Ids.MODAL_O], id_set[Ids.SPREAD], True)

        shift = Distances.MODAL_HEIGHT

        coordinates = get_coordinates(id_set[Ids.ORACLE_O], id_set[Ids.SPREAD])
        set_coordinates(id_set[Ids.ORACLE_O], id_set[Ids.SPREAD], [(coordinates[0][0], coordinates[0][1] + shift),
                                                                   (coordinates[1][0], coordinates[1][1] + shift),
                                                                   (coordinates[2][0], coordinates[2][1]),
                                                                   (coordinates[3][0], coordinates[3][1])])


def layout_planeswalker(id_set: dict):
    set_visibility(id_set[Ids.GROUP_PLANESWALKER_O], id_set[Ids.SPREAD], True)
