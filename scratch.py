from enum import Enum
import json

characterNames = {
                    'geel': "Van Geelen",
                    'paars': "Pimpel",
                    'groen': "Groenewoud",
                    'blauw': "Blaauw van Draet",
                    'rood': "Roodhart",
                    'wit': "De Wit"
                    }
weaponNames = ['mes', 'kandelaar', 'pistool', 'vergif', 'trofee', 'touw', 'knuppel', 'bijl', 'halter']
roomNames = ['hal', 'eetkamer', 'keuken', 'terras', 'werkkamer', 'theater', 'zitkamer', 'bubbelbad', 'gastenverblijf']
allNames = list(characterNames.keys()) + list(characterNames.values()) + weaponNames + roomNames

def getCategory(card_name):
    if card_name in list(characterNames.keys()) + list(characterNames.values()):
        return "Character"
    if card_name in weaponNames:
        return "Weapon"
    if card_name in roomNames:
        return "Room"


class Card:
    def __init__(self, name, category):
        self.name = name
        self.category = category


class Player:
    def __init__(self, name, character, card_amount):
        self.name = name
        self.character = character
        self.cardAmount = card_amount


class Knowledge(Enum):
    TRUE = "True"
    FALSE = "False"
    MAYBE = "Maybe"

    @staticmethod
    def fromBool(boolean):
        if boolean:
            return Knowledge.TRUE
        else:
            return Knowledge.FALSE


class Claim:
    def __init__(self, claimer, weapon, room, suspect):
        self.claimer = claimer  # Degene die de claim doet
        self.weapon = weapon
        self.room = room
        self.suspect = suspect
        self.replies = {}  # player -> bool arrray       event.replies[Jan] = False; event.replies[Klaas] = False; event.replies[Mien] = True

    def getCards(self):
        return [self.weapon, self.room, self.suspect]

    # Did player have any of the cards in the claim?
    # Returns Knowledge
    def playerReply(self, player):
        if player in self.replies:
            return Knowledge.fromBool(self.replies[player])
        else:
            return Knowledge.maybe


def getInput(prompt, possibilities):
    userInput = input(prompt)
    """" Suggestie: return een lege array alse de userInput "cancel" is.
         Op die manier kun je een verkeerd getypte outcome cancellen
    """
    if userInput == "cancel":
        return ""

    userInput = userInput.split(", ")
    outcomes = []
    for i in userInput:
        matches = []
        for possibleMatch in possibilities:
            if possibleMatch.lower().startswith(i.lower()):
                matches.append(possibleMatch)
        if len(matches) == 0:
            outcomes.extend(getInput('Could not interpret ' + i + '. Please try again: ', possibilities))
        elif len(matches) == 1:
            outcomes.append(matches[0])
        else:
            found = False
            for possibleMatch in possibilities:
                if possibleMatch.lower() == i.lower():
                    outcomes.append(i)
                    found = True
            if not found:
                outcomes.extend(getInput('Could not interpret ' + i +'. Did you mean: ' + ", ".join(matches) + '? ', possibilities))
    return outcomes

characterCards = [Card(c, "Character") for c in list(characterNames.values())]
weaponCards = [Card(c, "Weapon") for c in weaponNames]
roomCards = [Card(c, "Room") for c in roomNames]
allCards = characterCards + weaponCards + roomCards


def matchCard(cardName):
    for card in allCards:
        if cardName == card.name:
            return card


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
            getCategory(open_card_json)
        )
        open_cards.append(open_card)

    your_cards = []
    for your_card_json in your_cards_json:
        your_card = Card(
            your_card_json,
            getCategory(your_card_json)
        )
        your_cards.append(your_card)

    return players, open_cards, your_cards


if __name__ == "__main__":
    loadGameConfig()
