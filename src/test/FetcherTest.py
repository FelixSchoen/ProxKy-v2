import unittest

from src.main.data.fetcher import ScryfallFetcher

VARIETY_CARDS = ["Black Lotus",
                 "Clearwater Pathway",
                 "Treasure Map",
                 "Alive // Well",
                 "Rune-Tail, Kitsune Ascendant",
                 "Bonecrusher Giant",
                 "Wizard Class",
                 "Urza's Saga",
                 "Gisela, the Broken Blade"]


class FetcherTest(unittest.TestCase):

    def test_fetch_variety_of_cards(self):
        fetcher = ScryfallFetcher()

        for card_name in VARIETY_CARDS:
            dictionary = dict()
            dictionary["name"] = card_name
            card = fetcher.fetch_card(dictionary)
            print(card.name)
            self.assertTrue(card_name in card.name)
