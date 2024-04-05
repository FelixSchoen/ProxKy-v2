from __future__ import annotations

import json
import time
import urllib.parse
from abc import ABC, abstractmethod

import requests

from proxky.main.configuration.config import CONFIG_CARD_DATA_FETCHER, API_URL
from proxky.main.data.card import Card
from proxky.main.misc.info import show_info
from proxky.main.misc.enumerations import InfoMode


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
    def _fetch_card_internal(self, dictionary: dict) -> Card:
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


class ScryfallFetcher(Fetcher):

    def __init__(self) -> None:
        super().__init__()
        self._limit = 100

    def _fetch_card_internal(self, dictionary: dict) -> Card | None:
        if "id" in dictionary:
            response = requests.get(API_URL + "/cards/" + urllib.parse.quote(dictionary["id"]))
        elif "cn" in dictionary:
            if "set" not in dictionary:
                show_info("Set not provided", prefix=dictionary.get("name", "Unknown"), mode=InfoMode.ERROR)
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
            show_info("Could not fetch card", prefix=dictionary.get("name", "Unknown"), mode=InfoMode.ERROR)
            return None

        card = Card.generate(json.loads(response.text))

        if dictionary.get("name") is not None and card.name != dictionary.get("name"):
            show_info("Fetched card name differs from specified", prefix=dictionary.get("name") + " / " + card.name,
                      mode=InfoMode.WARN, end_line=True)

        return card
