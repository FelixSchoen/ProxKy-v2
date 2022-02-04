import unittest

from src.main.data.fetcher import ScryfallFetcher
from src.main.pipeline import parse_card_list, process_card

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
            self.assertTrue(card_name in card.name)


class PipelineTest(unittest.TestCase):

    def test_parse_card_list(self):
        card_list = parse_card_list("resources/test_decklist.txt")
        self.assertTrue(len(card_list) == len(VARIETY_CARDS))

    def test_process_card(self):
        fetcher = ScryfallFetcher()
        card = fetcher.fetch_card({"name": "Black Lotus"})
        process_card(card)
        self.assertTrue(card is not None)
