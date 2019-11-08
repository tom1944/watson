from enum import Enum

from gameconfig import loadGameConfig


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


class Rumour:
    def __init__(self, claimer, weapon, room, suspect):
        self.claimer = claimer  # Degene die de claim doet
        self.weapon = weapon
        self.room = room
        self.suspect = suspect
        self.replies = # List[(Player, Knowledge)]

    def getCards(self):
        return [self.weapon, self.room, self.suspect]

    # Did player have any of the cards in the claim?
    # Returns Knowledge
    def playerReply(self, player):
        if player in self.replies:
            return Knowledge.fromBool(self.replies[player])
        else:
            return Knowledge.maybe


if __name__ == "__main__":
    players, open_card, your_cards = loadGameConfig()
