import json

from user_io import match_card
from player import Player
from card import Card, Category, cat_from_string
from typing import List, NamedTuple


class GameConfig(NamedTuple):
    players: Player
    open_cards: List[Card]
    your_cards: List[Card]
    all_cards: List[Card]


def load_game_config():
    with open("gameconfig.json", 'r') as file:
        config = json.load(file)

    players_json = config["players"]
    open_cards_json = config["open_cards"]
    your_cards_json = config["your_cards"]
    all_cards_json = config["all_cards"]

    check_if_all_categories_present(all_cards_json)

    all_cards = []
    for category_name, card_names in all_cards_json.items():
        for card_name in card_names:
            category = cat_from_string(category_name)
            all_cards.append(Card(card_name, category))

    players = []
    for player_json in players_json:
        player = Player(
            player_json["name"],
            player_json["character"],
            player_json["card_amount"]
        )
        players.append(player)

    open_cards = []
    for open_card_json in open_cards_json:
        open_card = match_card(open_card_json)
        open_cards.append(open_card)

    your_cards = []
    for your_card_json in your_cards_json:
        your_card = match_card(your_card_json)
        your_cards.append(your_card)

    return GameConfig(players, open_cards, your_cards, all_cards)


def check_if_all_categories_present(all_cards_json) -> None:
    json_categories = set(all_cards_json.keys())
    should_be_categories = set([cat.value for cat in Category])
    if json_categories != should_be_categories:
        raise Exception(f"One or more categories are incorrect."
                        f"Categories found: {json_categories}, should be {should_be_categories}")
