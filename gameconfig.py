import json

from card import Card, get_category
from main import Player


def loadGameConfig():
    with open("gameconfig.json", 'r') as file:
        config = json.load(file)

    players_json = config["players"]
    open_cards_json = config["open_cards"]
    your_cards_json = config["your_cards"]

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
        open_card = Card(
            open_card_json,
            get_category(open_card_json)
        )
        open_cards.append(open_card)

    your_cards = []
    for your_card_json in your_cards_json:
        your_card = Card(
            your_card_json,
            get_category(your_card_json)
        )
        your_cards.append(your_card)

    return players, open_cards, your_cards