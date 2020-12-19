import json

from context import Context
from knowledge import Knowledge
from player import Player
from card import Card, Category, cat_from_string
from typing import List, Dict

from rumour import Rumour
from session import Session


def load_session(filename: str) -> (Context, Session):
    with open(filename, 'r') as file:
        config = json.load(file)

    players_json = config["players"]
    cards_json = config["cards"]
    open_cards_json = config["open_cards"]
    cards_seen_json = config["cards_seen"]
    rumours_json = config["rumours_made"]

    check_if_all_categories_present(cards_json)

    all_cards = retrieve_cards(cards_json)
    players = retrieve_players(players_json)
    open_cards = retrieve_open_cards(all_cards, open_cards_json)

    used_cards = [c for c in all_cards if c not in open_cards]

    cards_seen = retrieve_cards_seen(all_cards, cards_seen_json, players)
    rumours = retrieve_rumours(players, rumours_json, used_cards)
    return Session(Context(players, used_cards), cards_seen, rumours)


def retrieve_rumours(players, rumours_json, used_cards) -> List[Rumour]:
    rumours = []
    for rumour_json in rumours_json:
        claimer = find_player_by_name(rumour_json["claimer"], players)
        rumour_cards = []
        for card_name in rumour_json["cards"]:
            rumour_cards.append(find_card_by_name(card_name, used_cards))
        replies = []
        for player_name in rumour_json["replied_yes"]:
            replies.append((find_player_by_name(player_name, players), Knowledge.TRUE))
        for player_name in rumour_json["replied_no"]:
            replies.append((find_player_by_name(player_name, players), Knowledge.FALSE))
        rumour = Rumour(claimer, rumour_cards, replies)
        rumours.append(rumour)
    return rumours


def retrieve_cards_seen(all_cards, cards_seen_json, players) -> Dict[Player, List[Card]]:
    cards_seen = {}
    for player_name, card_names in cards_seen_json.items():
        cards = []
        for card_name in card_names:
            card = find_card_by_name(card_name, all_cards)
            cards.append(card)
        player = find_player_by_name(player_name, players)
        cards_seen.update({player: cards})
    return cards_seen


def retrieve_open_cards(all_cards, open_cards_json) -> List[Card]:
    open_cards = []
    for open_card_json in open_cards_json:
        open_card = find_card_by_name(open_card_json, all_cards)
        open_cards.append(open_card)
    return open_cards


def retrieve_players(players_json) -> List[Player]:
    players = []
    for player_json in players_json:
        player = Player(
            player_json["name"],
            player_json["character"],
            player_json["card_amount"]
        )
        players.append(player)
    return players


def retrieve_cards(cards_json) -> List[Card]:
    all_cards = []
    for category_name, card_names in cards_json.items():
        for card_name in card_names:
            category = cat_from_string(category_name)
            all_cards.append(Card(card_name, category))
    return all_cards


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


def find_player_by_name(player_name: str, all_players: List[Player]) -> Player:
    for player in all_players:
        if player.name == player_name:
            return player
