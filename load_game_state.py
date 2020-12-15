import json

from gamestate import GameState
from player import Player
from card import Card, Category, cat_from_string
from typing import List


def load_game_state(filename: str) -> GameState:
    with open(filename, 'r') as file:
        config = json.load(file)

    players_json = config["players"]
    open_cards_json = config["open_cards"]
    all_cards_json = config["cards"]

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
        open_card = find_card_by_name(open_card_json, all_cards)
        open_cards.append(open_card)

    used_cards = [c for c in all_cards if c not in open_cards]

    return GameState(players, used_cards)


def check_if_all_categories_present(all_cards_json) -> None:
    json_categories = set(all_cards_json.keys())
    should_be_categories = set([cat.value for cat in Category])
    if json_categories != should_be_categories:
        raise Exception(f"One or more categories are incorrect."
                        f"Categories found: {json_categories}, should be {should_be_categories}")


def find_card_by_name(card_name: str, cards: List[Card]) -> Card:
    for card in cards:
        if card_name == card.name:
            return card
    raise Exception(f'card {card_name} not found')