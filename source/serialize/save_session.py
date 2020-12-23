import json
from typing import List, Dict

from source.data.card import Category, Card
from source.data.knowledge import Knowledge
from source.data.player import Player
from source.data.rumour import Rumour
from source.data.session import Session


def save_session(session: Session, filename: str):
    context = session.context
    config = {
        "players": players_to_json_object(context.players),
        "cards": cards_to_json_object(context.cards),
        "open_cards": [],
        "cards_seen": cards_seen_to_json_object(session.cards_seen),
        "rumours_made": rumours_to_json_object(session.get_rumours())
    }

    with open(filename, 'w') as outfile:
        json.dump(config, outfile, indent=4)


def players_to_json_object(players: List[Player]):
    return [
        player_to_json_object(player)
        for player in players
    ]


def player_to_json_object(player):
    return {
        "name": player.name,
        "character": player.character,
        "card_amount": player.cardAmount
    }


def cards_to_json_object(cards: List[Card]):
    return {
        "Weapon": [c.name for c in cards if c.category == Category.WEAPON],
        "Room": [c.name for c in cards if c.category == Category.ROOM],
        "Character": [c.name for c in cards if c.category == Category.CHARACTER]
    }


def cards_seen_to_json_object(cards_seen: Dict[Player, List[Card]]):
    return {
        player.name: [c.name for c in cards_of_player]
        for player, cards_of_player in cards_seen.items()
    }


def rumours_to_json_object(rumours_made: List[Rumour]):
    json_rumours_object = []

    for rumour in rumours_made:
        positive_repliers = []
        negative_repliers = []
        for p, k in rumour.replies:
            if k == Knowledge.TRUE:
                positive_repliers.append(p)
            elif k == Knowledge.FALSE:
                negative_repliers.append(p)

        json_rumours_object.append({
            "claimer": rumour.claimer.name,
            "cards": [c.name for c in rumour.rumour_cards],
            "replied_yes": [p.name for p in positive_repliers],
            "replied_no": [p.name for p in negative_repliers]
        })

    return json_rumours_object
