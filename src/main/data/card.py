from __future__ import annotations

import json
import re

import requests

from src.main.configuration.variables import Faces, Regex, CONVENTIONAL_DOUBLE_SIDED_LAYOUTS
from src.main.utils.mtg import get_color_array


class Card:
    """
    Class representing a Magic: The Gathering card.
    """

    def __init__(self):
        super().__init__()

        # Core Fields
        self.id = None

        # Gameplay Fields
        self.all_parts = None
        self.card_faces = None
        self.cmc = None
        self.color_identity = None
        self.color_indicator = None
        self.colors = None
        self.layout = None
        self.loyalty = None
        self.mana_cost = None
        self.name = None
        self.oracle_text = None
        self.power = None
        self.produced_mana = None
        self.toughness = None
        self.type_line = None

        # Print Fields
        self.artist = None
        self.collector_number = None
        self.flavor_name = None
        self.flavor_text = None
        self.image_uris = None
        self.rarity = None
        self.set = None

        # Additional Fields
        self.component = None
        self.side = None
        self.prints = None

    @staticmethod
    def generate(args: dict, recurse: bool = True) -> Card:
        """
        Initialises a card object using the provided dictionary.
        :param args: A dictionary containing relevant card information
        :param recurse: Whether to recursively load included parts such as prints
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

        # Handle parts and faces
        card.all_parts = []
        for part in args.get("all_parts", []):
            card.all_parts.append(Card.generate(part))

        card.card_faces = []
        for face in args.get("card_faces", []):
            card.card_faces.append(Card.generate(face))

        # Fetch meld card
        if card.layout == "meld":
            meld_result_id = next(part.id for part in card.all_parts if part.component == "meld_result")

            # Check that card is front side
            if card.id != meld_result_id:
                from src.main.data.fetcher import Fetcher
                fetcher = Fetcher.get_standard_fetcher()

                dictionary = dict()
                dictionary["id"] = meld_result_id

                meld_result = fetcher.fetch_card(dictionary)

                card.card_faces.append(card)
                card.card_faces.append(meld_result)

        # Fetch prints
        card.prints = []
        if recurse and args.get("prints_search_uri") is not None:
            response = json.loads(requests.get(args.get("prints_search_uri")).text)

            for card_data in response["data"]:
                card.prints.append(Card.generate(card_data, False))

        card._manage_card_faces()

        return card

    def _manage_card_faces(self) -> None:
        for i, face in enumerate(self.card_faces):
            # Add face identifier
            if self.layout in CONVENTIONAL_DOUBLE_SIDED_LAYOUTS:
                if i == 0:
                    face.side = Faces.FRONT
                else:
                    face.side = Faces.BACK

            # Fill fields
            if len(face.colors) == 0:
                if self.layout in ["split", "adventure"]:
                    face.colors.extend(get_color_array(face.mana_cost))

            if face.layout is None:
                face.layout = self.layout

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
                face.artist = self.artist

            if face.collector_number is None:
                face.collector_number = self.collector_number

            if len(face.image_uris) == 0:
                face.image_uris = self.image_uris

            if face.rarity is None:
                face.rarity = self.rarity

            if face.set is None:
                face.set = self.set
