from io import characterNames


class Card:
    def __init__(self, name, category):
        self.name = name
        self.category = category


weaponNames = ['mes', 'kandelaar', 'pistool', 'vergif', 'trofee', 'touw', 'knuppel', 'bijl', 'halter']
roomNames = ['hal', 'eetkamer', 'keuken', 'terras', 'werkkamer', 'theater', 'zitkamer', 'bubbelbad', 'gastenverblijf']
allNames = list(characterNames.keys()) + list(characterNames.values()) + weaponNames + roomNames


def get_category(card_name):
    if card_name in list(characterNames.keys()) + list(characterNames.values()):
        return "Character"
    if card_name in weaponNames:
        return "Weapon"
    if card_name in roomNames:
        return "Room"


characterCards = [Card(c, "Character") for c in list(characterNames.values())]
weaponCards = [Card(c, "Weapon") for c in weaponNames]
roomCards = [Card(c, "Room") for c in roomNames]
allCards = characterCards + weaponCards + roomCards


def match_card(card_name):
    for card in allCards:
        if card_name == card.name:
            return card
