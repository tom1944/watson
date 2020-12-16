import json

from card import Category
from gamestate import GameState
from knowledge import Knowledge
from session import Session


def serialize(game_state: GameState, session: Session, filename: str):
    config = {}
    config["players"] = []
    for player in game_state.players:
        config["players"].append({
            "name": player.name,
            "character": player.character,
            "card_amount": player.cardAmount
        })

    config["cards"] = {
        "Weapon": [c.name for c in game_state.cards if c.category == Category.WEAPON],
        "Room": [c.name for c in game_state.cards if c.category == Category.ROOM],
        "Character": [c.name for c in game_state.cards if c.category == Category.CHARACTER]
    }
    config["open_cards"] = []
    config["cards_seen"] = {}
    for player, cards_seen in session.cards_seen.items():
        config["cards_seen"][player.name] = [c.name for c in cards_seen]

    config["rumours_made"] = []
    for rumour in session.get_rumours():
        positive_repliers = []
        negative_replies = []
        for p, k in rumour.replies:
            if k == Knowledge.TRUE:
                positive_repliers.append(p)
            elif k == Knowledge.FALSE:
                negative_replies.append(p)

        config["rumours_made"].append({
            "claimer": rumour.claimer.name,
            "cards": [c.name for c in rumour.rumour_cards],
            "replied_yes": [p.name for p in positive_repliers],
            "replied_no": [p.name for p in negative_replies]
        })

    with open(filename, 'w') as outfile:
        json.dump(config, outfile, indent=4)
