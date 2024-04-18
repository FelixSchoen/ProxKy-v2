from __future__ import annotations


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

