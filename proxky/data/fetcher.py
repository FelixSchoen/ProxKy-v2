from __future__ import annotations

import json
import re
import time
import urllib.parse
from abc import ABC, abstractmethod

import requests

from proxky.configuration.config import CONFIG_CARD_DATA_FETCHER, API_URL
from proxky.configuration.variables import CONVENTIONAL_DOUBLE_SIDED_LAYOUTS, Faces, Regex
from proxky.data.card import Card
from proxky.misc.logging import get_logger, format_message_cardname
from proxky.misc.mtg import get_color_array

LOGGER = get_logger()


class Fetcher(ABC):
    """
    Abstract class that fetches information from a specific source, determined by the specific subclass.
    """

    def __init__(self) -> None:
        super().__init__()
        self._time_last_fetched = 0
        self._limit = 0

    def fetch_card(self, dictionary: dict) -> Card:
        """
        Fetches a card from a source using the given information.
        :param dictionary: Contains information about the card to fetch
        :return: The found card
        """
        if (time.perf_counter() - self._time_last_fetched) * 1000 < self._limit:
            time.sleep((time.perf_counter() - self._time_last_fetched))
            self._time_last_fetched = time.perf_counter()
        return self._fetch_card_internal(dictionary)

    @abstractmethod
    def _fetch_card_internal(self, dictionary: dict, fetch_faces: bool = True, fetch_prints: bool = True) -> Card:
        pass

    @classmethod
    def get_standard_fetcher(cls) -> Fetcher:
        """
        Returns the default fetcher.
        :return: The default fetcher
        """
        if CONFIG_CARD_DATA_FETCHER == "scryfall":
            return ScryfallFetcher()
        else:
            raise NotImplementedError

    def fill_card(self, args: dict, fetch_faces: bool = True, fetch_prints: bool = True) -> Card:
        """
        Initialises a card object using the provided dictionary.
        :param args: A dictionary containing relevant card information
        :param recurse: Whether to recursively load included parts such as faces
        """
        card = Card()

        card.id = args.get("id")

        card.cmc = args.get("cmc")
        card.color_identity = args.get("color_identity", [])
        card.color_indicator = args.get("color_indicator", [])
        card.colors = args.get("colors", [])
        card.layout = args.get("layout")
        card.loyalty = args.get("loyalty")
        card.mana_cost = args.get("mana_cost")
        card.name = args.get("name")
        card.oracle_text = args.get("oracle_text")
        card.power = args.get("power")
        card.produced_mana = args.get("produced_mana", [])
        card.toughness = args.get("toughness")
        card.type_line = args.get("type_line")

        card.artist = args.get("artist")
        card.collector_number = args.get("collector_number")
        card.flavor_name = args.get("flavor_name")
        card.flavor_text = args.get("flavor_text")
        card.image_uris = args.get("image_uris", [])
        card.rarity = args.get("rarity")
        card.set = args.get("set")

        card.component = args.get("component")
        card.prints_uri = args.get("prints_search_uri")

        card.prints = []
        card.all_parts = []
        card.card_faces = []

        # Handle faces, parts and prints
        if fetch_faces:
            for face in args.get("card_faces", []):
                card.card_faces.append(self.fill_card(face, False, False))
            for part in args.get("all_parts", []):
                card_part = self._fetch_card_internal({"id": part["id"]}, False, False)
                card_part.component = part["component"]
                card.all_parts.append(card_part)
        if fetch_prints:
            if args.get("prints_search_uri") is not None:
                response = json.loads(requests.get(args.get("prints_search_uri")).text)

                for card_data in response["data"]:
                    card.prints.append(self.fill_card(card_data, False, False))

        # Handle meld cards
        if card.layout == "meld" and any(part.component == "meld_result" for part in card.all_parts):
            meld_result_id = next(part.id for part in card.all_parts if part.component == "meld_result")

            # Check that current card is front side
            if card.id != meld_result_id:
                meld_result = self._fetch_card_internal({"id": meld_result_id}, False, True)
                card.card_faces.append(card)
                card.card_faces.append(meld_result)

        self.manage_card_faces(card)

        return card

    @staticmethod
    def manage_card_faces(card: Card) -> None:
        for i, face in enumerate(card.card_faces):
            # Add face identifier
            if card.layout in CONVENTIONAL_DOUBLE_SIDED_LAYOUTS:
                if i == 0:
                    face.side = Faces.FRONT
                else:
                    face.side = Faces.BACK

            # Fill fields
            if len(face.colors) == 0:
                if card.layout in ["split", "adventure"]:
                    face.colors.extend(get_color_array(face.mana_cost))

            if face.layout is None:
                face.layout = card.layout

            if len(face.produced_mana) == 0:
                # Find all instances of {X}: Add {Y}
                matches = re.finditer(Regex.ADD_MANA, face.oracle_text)
                colors = []

                # For each occurrence, add to produced mana
                for match in matches:
                    produced_mana = match.group("prod")
                    color_matches = re.finditer(Regex.MANA, produced_mana)

                    for color_match in color_matches:
                        colors.append(color_match.group("mana"))

                # Sort and format mana
                face.produced_mana = get_color_array(colors)

            if face.artist is None:
                face.artist = card.artist

            if face.collector_number is None:
                face.collector_number = card.collector_number

            if len(face.image_uris) == 0:
                face.image_uris = card.image_uris

            if face.rarity is None:
                face.rarity = card.rarity

            if face.set is None:
                face.set = card.set


class ScryfallFetcher(Fetcher):

    def __init__(self) -> None:
        super().__init__()
        self._limit = 100

    def _fetch_card_internal(self, dictionary: dict, fetch_faces: bool = True,
                             fetch_prints: bool = True) -> Card | None:
        if "id" in dictionary:
            response = requests.get(API_URL + "/cards/" + urllib.parse.quote(dictionary["id"]))
        elif "cn" in dictionary:
            if "set" not in dictionary:
                LOGGER.error(format_message_cardname(dictionary.get("name", "Unknown"), "Set not provided"))
                return None

            response = requests.get(
                API_URL + "/cards/" + urllib.parse.quote(dictionary["set"].lower()) + "/" + urllib.parse.quote(
                    dictionary["cn"]))
        elif "set" in dictionary:
            response = requests.get(
                API_URL + "/cards/named?exact=" + urllib.parse.quote(dictionary["name"]) + "&set=" + urllib.parse.quote(
                    dictionary["set"]))
        else:
            response = requests.get(
                API_URL + "/cards/named?exact=" + urllib.parse.quote(dictionary["name"]))

        if response.status_code != 200:
            LOGGER.error(format_message_cardname(dictionary.get("name", "Unknown"), "Could not fetch card"))
            return None

        card = self.fill_card(json.loads(response.text), fetch_faces, fetch_prints)

        if dictionary.get("name") is not None and card.name != dictionary.get("name"):
            LOGGER.warn(format_message_cardname(dictionary.get("name") + " / " + card.name,
                                                "Fetched card name differs from specified"))

        return card
