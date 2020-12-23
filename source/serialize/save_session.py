import json
from typing import List, Dict

from source.data.card import Category, Card
from source.data.knowledge import Knowledge
from source.data.player import Player
from source.data.rumour import Rumour
from source.data.session import Session


def save_session_to_file(session: Session, file_path: str):
    with open(file_path, 'w') as file:
        save_session_to_file_object(session, file)


def save_session_to_file_object(session: Session, file_object):
    context = session.context
    config = {
        "players": players_of_context_to_json_object(context.players),
        "cards": cards_of_context_to_json_object(context.cards + context.open_cards),
        "open_cards": cards_to_json_object(context.open_cards),
        "cards_seen": cards_seen_to_json_object(session.cards_seen),
        "rumours_made": rumours_to_json_object(session.get_rumours())
    }

    json.dump(config, file_object, indent=2)


def players_of_context_to_json_object(players: List[Player]):
    return [
        player_to_json_object(player)
        for player in players
    ]


def player_to_json_object(player: Player):
    return {
        "name": player.name,
        "character": player.character,
        "card_amount": player.cardAmount
    }


def cards_of_context_to_json_object(context_cards: List[Card]):
    weapon_cards = [c for c in context_cards if c.category == Category.WEAPON]
    room_cards = [c for c in context_cards if c.category == Category.ROOM]
    character_cards = [c for c in context_cards if c.category == Category.CHARACTER]

    return {
        "Weapon": cards_to_json_object(weapon_cards),
        "Room": cards_to_json_object(room_cards),
        "Character": cards_to_json_object(character_cards),
    }


def cards_to_json_object(cards: List[Card]):
    card_names = [card.name for card in cards]
    return sorted(card_names)


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
